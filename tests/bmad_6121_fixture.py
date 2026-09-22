"""Materialize exact public-source fixtures without network or installer execution."""
import io
import csv
import json
import tarfile
from pathlib import Path
from tests.test_conductor_bmad_support import runtime, seed_factory, seed_git


def seed(root: Path, *, nested=False, tea=False, shims=False):
    seed_git(root); seed_factory(root)
    project = root / 'bmad' if nested else root
    active = project / '_bmad'
    active.mkdir(parents=True)
    if nested:
        (root / 'docs/Conductor/PROJECT_CONFIG.json').write_text(json.dumps({'adapters': {'bmad': {'declared_root': 'bmad/_bmad'}}}))
    with tarfile.open(Path(__file__).parent / 'fixtures/bmad_6121/public-skills.tar.gz') as archive:
        for member in archive.getmembers():
            parts = Path(member.name).parts
            section = parts[0]
            if section == 'skills' or section == 'tea_skills' and tea or section == 'shims' and shims:
                target = project / '.claude/skills' / Path(*parts[1:])
            elif section == 'scripts':
                target = active / member.name
            else:
                continue
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(archive.extractfile(member).read())
    (active / '_config').mkdir()
    manifest = 'installation:\n  version: 6.12.1-next.0\nmodules:\n  - name: core\n    version: 6.12.1-next.0\n  - name: bmm\n    version: 6.12.1-next.0\n'
    if tea:
        manifest += '  - name: tea\n    version: main\n    sha: '+runtime.policy.profile_6121()['tea_commit']+'\n'
    (active/'_config/manifest.yaml').write_text(manifest)
    rows=[row for module in (['core','bmm','tea'] if tea else ['core','bmm']) for row in runtime.policy.profile_6121()['catalog'][module] if row['skill']=='_meta' or (project/'.claude/skills'/row['skill']).is_dir()]
    with (active/'_config/bmad-help.csv').open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (active/'config.toml').write_text('[core]\nproject_name="Public fixture"\nuser_name="Test reviewer"\ncommunication_language="English"\ndocument_output_language="English"\noutput_folder="{project-root}/_bmad-output"\n[modules.bmm]\nplanning_artifacts="{project-root}/_bmad-output/planning-artifacts"\nimplementation_artifacts="{project-root}/_bmad-output/implementation-artifacts"\nproject_knowledge="{project-root}/docs"\n')
    # Real installer output includes agent descriptors, including the optional TEA agent.
    agents = dict(runtime.policy.profile_6121()['agents'])
    if tea:
        agents.update(runtime.policy.profile_6121()['tea_agents'])
    with (active/'config.toml').open('a') as stream:
        for name, descriptor in agents.items():
            stream.write('\n[agents.' + name + ']\n')
            for key, value in descriptor.items():
                stream.write(key + '=' + json.dumps(value, ensure_ascii=False) + '\n')
    for module in ['core','bmm']:
        (active/module).mkdir()
        (active/module/'config.yaml').write_text('user_name: Test reviewer\nproject_name: Public fixture\ncommunication_language: English\ndocument_output_language: English\noutput_folder: "{project-root}/_bmad-output"\nplanning_artifacts: "{project-root}/_bmad-output/planning-artifacts"\nimplementation_artifacts: "{project-root}/_bmad-output/implementation-artifacts"\n')
    if tea:
        (active/'tea').mkdir()
        (active/'tea/config.yaml').write_text('test_artifacts: "{project-root}/_bmad-output/test-artifacts"\nuser_name: Test reviewer\ncommunication_language: English\ndocument_output_language: English\noutput_folder: "{project-root}/_bmad-output"\n')
    (active/'custom').mkdir()
    if nested:
        (root/'.claude').mkdir()
        (root/'.claude/skills').symlink_to('../bmad/.claude/skills')
    return project
