#!/usr/bin/env python3
"""Bounded qualification. Private input paths come from run-local configuration."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import time
import yaml

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tests.bmad_6121_fixture import seed
from scripts.verify_conductor_bmad_6121_qualification import codex


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def metadata(path):
    mode = stat.S_IMODE(path.lstat().st_mode)
    if path.is_symlink():
        return {'type': 'link', 'target': os.readlink(path), 'mode': mode}
    return {'type': 'file', 'sha256': sha(path), 'mode': mode}


def inventory(root):
    rows = {}
    for current, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [d for d in dirs if d != '.git']
        for name in dirs + files:
            path = Path(current) / name
            if path.is_symlink() or path.is_file():
                rows[path.relative_to(root).as_posix()] = metadata(path)
    return rows


def command(argv, cwd, evidence, expected=0, input_value=None):
    done = subprocess.run(argv, cwd=cwd, input=input_value, text=True, capture_output=True)
    save(evidence, {'argv': argv, 'cwd': str(cwd), 'exit': done.returncode, 'stdout': done.stdout, 'stderr': done.stderr})
    assert done.returncode == expected, f'{evidence}: exit {done.returncode}'
    try:
        return json.loads(done.stdout)
    except ValueError:
        return done.stdout


def cli(package, root, args, evidence):
    script = ROOT / f'plugins/{package}/scripts/' / ('conductor_plugin.py' if package == 'conductor' else 'conductor_bmad.py')
    return command([str(ROOT/'scripts/conductor-python'), str(script), '--root', str(root), '--json', *args], root, evidence)


def candidate_identity():
    return {p.relative_to(ROOT).as_posix(): metadata(p)
            for package in ['conductor', 'conductor-claude', 'conductor-bmad', 'conductor-bmad-claude']
            for p in sorted((ROOT/'plugins'/package).rglob('*')) if p.is_file() or p.is_symlink()}


def routes(notes):
    lane = notes / 'fixtures' / ('routes-' + str(time.time_ns()))
    lane.mkdir(parents=True)
    codex(lane)
    fixture = lane / 'hook-project'; fixture.mkdir(); seed(fixture, nested=True)
    before = inventory(fixture)
    hook = ROOT / 'plugins/conductor-bmad-claude/scripts/conductor_bmad.py'
    results = []
    for name in ['bmad-spec', 'bmad-review', 'bmad-architecture', 'bmad-ux', 'bmad-build', 'bmad-build-auto', 'bmad-code-review', 'bmad-unknown-future']:
        allowed = name in ['bmad-spec', 'bmad-review', 'bmad-architecture', 'bmad-ux']
        for event in [{'hook_event_name': 'UserPromptExpansion', 'command_name': name},
                      {'hook_event_name': 'PreToolUse', 'tool_name': 'Skill', 'tool_input': {'skill': name}}]:
            result = command([str(ROOT/'scripts/conductor-python'), str(hook), '--root', str(fixture), 'hook'], fixture,
                             lane/f'hook-{name}-{event["hook_event_name"]}.json', input_value=json.dumps(event))
            if allowed:
                assert 'bmad/_bmad-output' in result['hookSpecificOutput']['additionalContext'], result
            elif event['hook_event_name'] == 'PreToolUse':
                assert result['hookSpecificOutput']['permissionDecision'] == 'deny', result
            else:
                assert result['decision'] == 'block', result
            results.append({'workflow': name, 'event': event['hook_event_name'], 'allowed': allowed})
    assert inventory(fixture) == before
    save(notes/'routes-result.json', {'state': 'PASS', 'evidence_directory': str(lane), 'checks': results, 'candidate': candidate_identity(),
                                     'scope': 'Actual stdio MCP and deterministic hook subprocesses; no live Claude model or desktop activation'})


def readiness(notes):
    config = json.loads((notes/'readiness-input.json').read_text())
    original = Path(config['original_root']); pilot = Path(config['pilot_root'])
    before = inventory(pilot)
    lane = notes/'fixtures'/('readiness-'+str(time.time_ns())); lane.mkdir(parents=True)
    fixture = lane/'project'
    shutil.copytree(pilot, fixture, symlinks=True, ignore=shutil.ignore_patterns('.git'))
    command(['git', 'init', '-q'], fixture, lane/'git-init.json')
    # No private model session is started. Sanitised settings are explicit fixture data.
    for relative in config['sanitize_settings']:
        save(fixture/relative, {})
    for operation in json.loads((notes/'dependency-repair-plan.json').read_text()):
        source = notes/'proposed-dependency-restoration'/operation['path']
        assert sha(source) == operation['sha256']
        target = fixture/operation['path']; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    for relative, addition in config['append_files'].items():
        path = fixture/relative
        path.write_bytes(path.read_bytes()+addition.encode())
    core = cli('conductor', fixture, ['brownfield', '--harness', 'claude'], lane/'core-preview.json')
    assert core['state'] == 'PLAN_READY', core
    applied = cli('conductor', fixture, ['brownfield', '--harness', 'claude', '--apply', '--approve-plan', core['plan_id']], lane/'core-apply-synthetic.json')
    assert applied['state'] == 'APPLIED', applied
    project_config = fixture/'docs/Conductor/PROJECT_CONFIG.json'
    value = json.loads(project_config.read_text())
    value['adapters'] = {'bmad': {'declared_root': config['declared_root'], 'legacy_evidence_root': 'docs/adapters/bmad/legacy-evidence'}}
    save(project_config, value)
    for operation in ['seed-contracts', 'intake']:
        args = [operation] + (['--harness', 'claude'] if operation == 'intake' else [])
        plan = cli('conductor-bmad', fixture, args, lane/f'{operation}-preview.json')
        assert plan['state'] == 'PLAN_READY', plan
        applied = cli('conductor-bmad', fixture, args+['--approve-plan', plan['plan']['plan_id']], lane/f'{operation}-apply-synthetic.json')
        assert applied['state'] == 'APPLIED', applied
    doctor = cli('conductor', fixture, ['doctor', '--harness', 'claude'], lane/'doctor.json')
    assert doctor['state'] == 'READY', doctor
    audit = cli('conductor-bmad', fixture, ['audit', '--harness', 'claude'], lane/'audit.json')
    assert audit['state'] == 'READY', audit
    promotion = cli('conductor-bmad', fixture, config['promotion_argv'], lane/'real-spec-preview-only.json')
    assert promotion['state'] == 'PLAN_READY', promotion
    plan = promotion['plan']
    selected = json.loads((notes/'selected-inputs.json').read_text())
    expected = {x['path']: x['sha256'] for x in selected if x['path'] != config['bmad_manifest']}
    artifacts = {v['source_path']: v['sha256'] for v in plan['source_artifacts'].values()}
    assert artifacts == expected, {'expected': sorted(expected), 'actual': sorted(artifacts)}
    for path, digest in expected.items():
        assert sha(fixture/path) == sha(original/path) == digest
    assert not (fixture/plan['destination']).exists(), 'Private real Spec must remain preview only'
    # Prepare ALL proposed bytes, but never copy a fixture installation receipt/state.
    after = inventory(fixture)
    modified_existing = {path for path in before if before[path] != after.get(path)}
    expected_modified = set(config['sanitize_settings']) | set(config['append_files']) | {'CLAUDE.md'}
    expected_modified |= {item['path'] for item in json.loads((notes/'dependency-repair-plan.json').read_text()) if item['path'] in before}
    assert modified_existing == expected_modified, 'Unexpected project source mutation'
    # Git must retain the repaired dependencies and original CSV bytes on a future clone.
    references = [item['path'] for item in json.loads((notes/'dependency-repair-plan.json').read_text()) if item['operation'] == 'add']
    ignored = command(['git', 'check-ignore', '--no-index', *references], fixture, lane/'references-ignore-check.json', expected=1)
    assert not ignored
    csv_path = next(item['path'] for item in json.loads((notes/'dependency-repair-plan.json').read_text()) if item['path'].endswith('brain-methods.csv'))
    attr = command(['git', 'check-attr', 'text', '--', csv_path], fixture, lane/'csv-attribute-check.json')
    assert attr.strip().endswith(': text: unset'), attr
    proposed = notes/'pilot-proposed-files'
    if proposed.exists(): shutil.rmtree(proposed)
    changes = []
    generated = []
    for path in sorted(set(before) | set(after)):
        if before.get(path) == after.get(path): continue
        if path not in after: raise AssertionError('Unexpected deletion: '+path)
        if path.startswith('.git/'): continue
        if path.startswith(('docs/Conductor/installation/', 'docs/adapters/bmad/receipts/')):
            generated.append(path); continue
        destination = proposed/path; destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(fixture/path, destination)
        changes.append({'path': path, 'before': before.get(path), 'after': after[path]})
    assert not (proposed/'docs/Conductor/installation').exists()
    assert not (proposed/'docs/adapters/bmad/receipts').exists()
    native = cli('conductor', pilot, ['brownfield', '--harness', 'claude'], lane/'pilot-core-preview.json')
    assert native['state'] == 'PLAN_READY' and native['plugin_version'] == '0.3.7', native
    packet = {'target_root': str(pilot), 'baseline': before, 'changes': changes, 'generated_on_apply_only': generated,
              'native_core_plan_id': native['plan_id'], 'candidate_versions': '0.3.7', 'candidate': candidate_identity(),
              'conditional_steps': 'After separately approved preparations/core apply, declare root then re-preview seed-contracts and intake at the real target. Fixture IDs are not real-pilot approvals.',
              'authority': 'PREVIEW_ONLY; fixture setup used SYNTHETIC technical approvals only'}
    packet['review_sha256'] = hashlib.sha256(json.dumps(packet, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    save(notes/'pilot-setup-review.json', packet)
    assert inventory(pilot) == before
    walkthrough = notes/config['walkthrough']
    text = walkthrough.read_text()
    for phrase in config['walkthrough_required_text']:
        assert phrase in text, 'Walkthrough missing: '+phrase
    save(notes/'readiness-result.json', {'state': 'PASS', 'evidence_directory': str(lane), 'real_spec_artifacts': artifacts,
         'pilot_review_sha256': packet['review_sha256'], 'walkthrough_sha256': sha(walkthrough),
         'pilot_mutations': [], 'real_spec_promotion': 'PREVIEW_ONLY', 'fixture_approvals': 'SYNTHETIC TEST ONLY',
         'product_tests': 'NOT_RUN', 'candidate_versions': '0.3.7', 'candidate': candidate_identity()})


def boundaries(notes):
    config = json.loads((notes/'readiness-input.json').read_text())
    baseline = json.loads((notes/'source-baseline.json').read_text())
    old = Path(baseline['source_root'])
    for name, expected in baseline['files'].items():
        assert metadata(old/name) == expected, 'Original candidate changed: '+name
    project = json.loads((notes/'checkout-baseline.json').read_text())
    for key in ['original_root', 'pilot_root']:
        assert inventory(Path(config[key])) == project, key+' changed'
    result = subprocess.run(['git', 'ls-files', '-co', '--exclude-standard', '-z'], cwd=ROOT, capture_output=True, check=True)
    names = set(result.stdout.decode().split('\0')) - {''}
    delta = []
    allowed = set(config['allowed_source_paths'])
    for name in sorted(names | set(baseline['files'])):
        actual = metadata(ROOT/name) if (ROOT/name).exists() or (ROOT/name).is_symlink() else None
        if actual != baseline['files'].get(name):
            assert name in allowed or name.startswith('plugins/'), 'Unapproved delta: '+name
            delta.append({'path': name, 'before': baseline['files'].get(name), 'after': actual})
    for result_name in ['routes-result.json', 'readiness-result.json']:
        evidence = json.loads((notes/result_name).read_text())
        assert evidence['candidate'] == candidate_identity(), result_name + ': stale package identity'
    definitions = json.loads((notes.parent/'verification_definitions.json').read_text())
    manifest = yaml.safe_load((notes.parent/'verification_manifest.yaml').read_text())
    for check in manifest['checks']:
        check.pop('result', None)
    assert definitions == manifest, 'Verification definitions changed'
    # Private run excluded from Git listing; forbid private identifiers in changed deliverables.
    for row in delta:
        path = ROOT/row['path']
        if not path.is_file(): continue
        data = path.read_bytes().lower()
        prior_path = old/row['path']
        prior = prior_path.read_bytes().lower() if prior_path.is_file() else b''
        for marker in config['private_markers']:
            token = marker.encode().lower()
            assert data.count(token) <= prior.count(token), 'New private marker in distributable: '+row['path']
    lint = command(['bash', 'scripts/knowledge_lint.sh'], ROOT, notes/'knowledge-lint-final.json')
    save(notes/'boundaries-result.json', {'state': 'PASS', 'prior_candidate_entries_checked': len(baseline['files']),
         'project_entries_checked_per_root': len(project), 'delta': delta,
         'coverage': 'Recorded source files/links and complete original/pilot non-Git inventories, bytes/modes/link targets. Not a whole-machine or all-Git-metadata audit.',
         'knowledge_lint': lint})


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--case', choices=['routes', 'readiness', 'boundaries'], required=True); parser.add_argument('--run', required=True)
    args = parser.parse_args()
    if Path(args.run).name != args.run: parser.error('Run must be a single directory name')
    notes = ROOT/'docs/Conductor/runs'/args.run/'notes'
    globals()[args.case](notes)
    print(json.dumps({'state': 'PASS', 'case': args.case, 'evidence': str(notes/(args.case+'-result.json'))}))


if __name__ == '__main__':
    main()
