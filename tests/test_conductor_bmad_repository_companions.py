"""Repository companion permissions and frozen snapshot lifecycle (synthetic only)."""
import copy
import importlib.machinery
import importlib.util
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from tests.test_conductor_bmad_6121_intake import source, arguments, runtime

ROOT = Path(__file__).resolve().parents[1]
loader = importlib.machinery.SourceFileLoader('repo_preflight', str(ROOT / 'plugin-src/conductor-bmad/project-adapter/conductor_project_preflight'))
spec = importlib.util.spec_from_loader(loader.name, loader)
preflight = importlib.util.module_from_spec(spec)
loader.exec_module(preflight)


def external_source(root):
    directory = source(root)
    standards = root / 'docs/standards.md'
    standards.parent.mkdir(parents=True, exist_ok=True)
    standards.write_bytes(b'# Standards\r\nHuman review before merge.\r\n')
    p = directory / 'SPEC.md'
    p.write_text(p.read_text().replace('"details.md",', '"../../../../docs/standards.md", "details.md",'))
    args = arguments(directory, root)
    args.repo_companion = ['docs/standards.md']
    return directory, args


def validate_snapshot(root, plan, manifest):
    """Real schema/content validator; synthetic claim disposition, no human authority."""
    snapshot = root / plan['destination']
    digest = manifest['aggregate_sha256']
    claim = {'schema_version': 1, 'receipt_type': 'BMAD_CLAIM_DISPOSITIONS',
             'snapshot': {'snapshot_id': plan['snapshot_id'], 'aggregate_sha256': digest, 'path': plan['destination']},
             'claims': [{'claim_id': 'SYNTHETIC-1', 'outcome': 'ACCEPTED', 'rationale': 'Test fixture',
                         'intent_reference': 'R-001', 'reviewer': 'SYNTHETIC TEST', 'conflict_or_supersession': 'NONE'}]}
    claim['aggregate_sha256'] = runtime.digest_bytes(runtime.canonical(claim))
    claim_path = root / 'docs/Conductor/runs/SYNTHETIC/claims.json'
    claim_path.parent.mkdir(parents=True, exist_ok=True)
    claim_path.write_text(json.dumps(claim))
    fields = {'BMAD Evidence Type': 'SOLUTION_CONTEXT', 'BMAD Policy Version': manifest['policy_version'],
              'BMAD Promotion Plan ID': plan['plan_id'], 'BMAD Solution Plan Identity': plan['plan_identity'],
              'BMAD Claim Receipt': claim_path.relative_to(root).as_posix()}
    text = ''.join(f'- {key}: `{value}`\n' for key, value in fields.items())
    return preflight.validate_solution_context(root, 'SYNTHETIC', manifest, snapshot, text, digest, runtime.policy, [])


class RepositoryCompanionTests(unittest.TestCase):
    def fixture(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name).resolve()
        directory, args = external_source(root)
        return root, directory, args

    def apply(self, root, args):
        preview = runtime.promote(root, args)
        self.assertEqual('PLAN_READY', preview['state'], preview)
        args.approve_plan = preview['plan']['plan_id']
        result = runtime.promote(root, args)
        self.assertEqual('APPLIED', result['state'], result)
        return preview['plan'], result

    def test_complete_lifecycle_and_consumer(self):
        root, directory, args = self.fixture()
        plan, result = self.apply(root, args)
        self.assertEqual(5, len(plan['source_artifacts']))
        self.assertEqual(str(root), plan['repository_companions']['target_root'])
        snapshot = root / plan['destination']
        for name, artifact in plan['source_artifacts'].items():
            self.assertEqual((root / artifact['source_path']).read_bytes(), (snapshot / name).read_bytes())
            self.assertEqual((root / artifact['source_path']).stat().st_mode & 0o7777, (snapshot / name).stat().st_mode & 0o7777)
        manifest = json.loads((snapshot / 'SNAPSHOT_MANIFEST.json').read_text())
        self.assertIsNone(validate_snapshot(root, plan, manifest))
        self.assertEqual('REUSABLE', runtime.promote(root, args)['state'])
        # Source edits do not change an already frozen snapshot or its validation.
        (root / 'docs/standards.md').write_text('# Revised input\n')
        self.assertIsNone(validate_snapshot(root, plan, manifest))
        args.snapshot_id = 'synthetic-reconciled'
        args.supersedes_snapshot_id = plan['snapshot_id']
        args.supersedes_sha256 = result['aggregate_sha256']
        args.approve_plan = None
        second, applied = self.apply(root, args)
        self.assertIsNone(validate_snapshot(root, second, runtime.snapshot_manifest(second)))
        preview = runtime.rollback(root, applied['receipt'], None)
        self.assertEqual('PLAN_READY', preview['state'])
        self.assertEqual('APPLIED', runtime.rollback(root, applied['receipt'], preview['plan']['plan_id'])['state'])
        self.assertTrue(snapshot.exists())

    def test_permissions_are_exact_and_reached(self):
        for permissions in [[], ['docs'], ['docs/*.md'], ['../standards.md'], ['/tmp/standards.md'],
                            ['docs/standards.md', 'docs/standards.md'], ['docs/missing.md'],
                            ['bmad/_bmad-output/specs/session-error/details.md'], ['docs/unused.md'], ['.hidden/config.md']]:
            with self.subTest(permissions=permissions):
                root, _, args = self.fixture()
                (root / 'docs/unused.md').write_text('# Unused\n')
                (root / '.hidden').mkdir(); (root / '.hidden/config.md').write_text('# Hidden\n')
                args.repo_companion = permissions
                self.assertEqual('BLOCKED', runtime.promote(root, args)['state'])
                self.assertFalse((root / 'docs/upstream').exists())

    def test_approval_binds_root_permissions_bytes_and_modes(self):
        for change in ['root', 'bytes', 'mode', 'permission']:
            with self.subTest(change=change):
                root, directory, args = self.fixture()
                plan = runtime.promote(root, args)['plan']; args.approve_plan = plan['plan_id']
                if change == 'root':
                    other = root.parent / (root.name + '-copy')
                    shutil.copytree(root, other, symlinks=True); self.addCleanup(shutil.rmtree, other)
                    root = other
                elif change == 'bytes': (root / 'docs/standards.md').write_text('changed')
                elif change == 'mode': (root / 'docs/standards.md').chmod(0o600)
                else:
                    (root / 'docs/other.md').write_text('other')
                    args.repo_companion.append('docs/other.md')
                self.assertEqual('BLOCKED', runtime.promote(root, args)['state'])
                self.assertFalse((root / plan['destination']).exists())

    def test_symlinks_special_files_and_normalized_symlink_hops(self):
        for kind in ['file', 'ancestor', 'fifo', 'hidden-hop']:
            with self.subTest(kind=kind):
                root, directory, args = self.fixture()
                path = root / 'docs/standards.md'
                if kind == 'file':
                    path.unlink(); path.symlink_to(directory / 'details.md')
                elif kind == 'ancestor':
                    (root / 'docs').rename(root / 'real-docs'); (root / 'docs').symlink_to(root / 'real-docs', target_is_directory=True)
                elif kind == 'fifo': path.unlink(); os.mkfifo(path)
                else:
                    (directory / 'linked').symlink_to(root / 'docs', target_is_directory=True)
                    p = directory / 'SPEC.md'; p.write_text(p.read_text().replace('../../../../docs/standards.md', 'linked/../../../../../docs/standards.md'))
                self.assertEqual('BLOCKED', runtime.promote(root, args)['state'])

    def test_transitive_permissions_and_ambiguity(self):
        root, directory, args = self.fixture()
        (root / 'docs/other.md').write_text('# Other\n')
        (root / 'docs/standards.md').write_text('---\ncompanions: [other.md]\n---\n')
        self.assertEqual('BLOCKED', runtime.promote(root, args)['state'])
        args.repo_companion.append('docs/other.md')
        self.assertEqual('PLAN_READY', runtime.promote(root, args)['state'])
        # Both existing paths are authorised; do not select one arbitrarily.
        (root / 'bmad/other.md').write_text('different')
        self.assertEqual('CONDUCTOR_BMAD_COMPANION_AMBIGUOUS', runtime.promote(root, args)['reason_code'])
        args.repo_companion.append('bmad/other.md')
        self.assertEqual('CONDUCTOR_BMAD_COMPANION_AMBIGUOUS', runtime.promote(root, args)['reason_code'])

    def test_non_spec_and_wrong_evidence_modes_rejected(self):
        root, directory, args = self.fixture()
        args.evidence_type = None
        self.assertEqual('BLOCKED', runtime.promote(root, args)['state'])
        args.evidence_type = 'SOLUTION_CONTEXT'; args.workflow = 'architecture'
        (directory / 'SPEC.md').unlink()
        self.assertEqual('BLOCKED', runtime.promote(root, args)['state'])

    def test_consumer_rejects_provenance_and_artifact_tampering(self):
        root, _, args = self.fixture(); plan, result = self.apply(root, args)
        original = runtime.snapshot_manifest(plan)
        for field, value in [('paths', []), ('paths', ['docs/unused.md']), ('target_root', '/different/root'),
                             ('output_root', 'docs'), ('selected_source', '../SPEC.md')]:
            manifest = copy.deepcopy(original); manifest['provenance']['repository_companions'][field] = value
            self.assertIsNotNone(validate_snapshot(root, plan, manifest))
        manifest = copy.deepcopy(original)
        manifest['artifacts']['content/docs/standards.md']['source_path'] = 'docs/unapproved.md'
        manifest['provenance']['source_aggregate_sha256'] = runtime.digest_bytes(runtime.canonical(manifest['artifacts']))
        self.assertIsNotNone(validate_snapshot(root, plan, manifest))
        frozen = root / plan['destination'] / 'content/docs/standards.md'
        frozen.write_text('tampered')
        self.assertEqual('CONDUCTOR_BMAD_ARTIFACT_HASH_MISMATCH', validate_snapshot(root, plan, original))
        self.assertEqual('BLOCKED', runtime.promote(root, args)['state'])
        self.assertEqual('BLOCKED', runtime.rollback(root, result['receipt'], None)['state'])
