import argparse
import json
import tempfile
import unittest
from pathlib import Path
from tests.bmad_6121_fixture import seed, runtime


def source(root):
    project=seed(root,nested=True)
    directory=project/'_bmad-output/specs/session-error';directory.mkdir(parents=True)
    shared=project/'_bmad-output/planning';shared.mkdir()
    (shared/'architecture.md').write_text('# Shared context\nNo new services.\n')
    (directory/'SPEC.md').write_text('---\ncompanions: ["details.md", "../../planning/architecture.md"]\n---\n# Session error\nShow a recoverable error when logout fails.\n')
    (directory/'details.md').write_text('# Detail\nKeep the user signed in until logout succeeds.\n')
    (directory/'.memlog.md').write_text('---\ntopic: Synthetic decision history\n---\nApproved input: retain the existing session on logout error.\n')
    return directory


def arguments(directory,root,snapshot='synthetic-first',approval=None,**extra):
    return argparse.Namespace(source=directory.relative_to(root).as_posix(),snapshot_id=snapshot,workflow='spec',reviewer='SYNTHETIC TEST ONLY',review_ref='synthetic review; no real approval',review_qualifier=None,evidence_type='SOLUTION_CONTEXT',authority='EVIDENCE_ONLY',plan_identity='synthetic-fixture-only',supersedes_snapshot_id=extra.get('supersedes_snapshot_id'),supersedes_sha256=extra.get('supersedes_sha256'),approve_plan=approval)


class IntakeTests(unittest.TestCase):
    def root(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);r=Path(tmp.name);return r,source(r)

    def test_complete_roundtrip_reuse_supersession_and_tamper(self):
        root,directory=self.root();before={str(p.relative_to(directory)):p.read_bytes() for p in directory.iterdir()}
        args=arguments(directory,root);preview=runtime.promote(root,args);self.assertEqual('PLAN_READY',preview['state'])
        plan=preview['plan'];self.assertEqual(4,len(plan['source_artifacts']))
        args.approve_plan=plan['plan_id'];result=runtime.promote(root,args);self.assertEqual('APPLIED',result['state'])
        self.assertEqual('REUSABLE',runtime.promote(root,args)['state'])
        snap=root/plan['destination'];manifest=json.loads((snap/'SNAPSHOT_MANIFEST.json').read_text())
        self.assertEqual('6.12.1-next.0',manifest['provenance']['bmad_version'])
        for key,artifact in plan['source_artifacts'].items():
            self.assertEqual((snap/key).read_bytes(),(root/plan['source_base']/artifact['source_path']).read_bytes())
        next_args=arguments(directory,root,'synthetic-second',supersedes_snapshot_id=args.snapshot_id,supersedes_sha256=result['aggregate_sha256'])
        preview2=runtime.promote(root,next_args);next_args.approve_plan=preview2['plan']['plan_id'];self.assertEqual('APPLIED',runtime.promote(root,next_args)['state'])
        self.assertEqual(before,{str(p.relative_to(directory)):p.read_bytes() for p in directory.iterdir()})
        next((snap/'content').rglob('details.md')).write_text('tamper')
        self.assertEqual('BLOCKED',runtime.promote(root,args)['state'])

    def test_reference_resolution_and_missing_ambiguous_unsafe(self):
        for ref,mode in [('_bmad-output/planning/architecture.md','valid'),('missing.md','missing'),('../../../outside.md','escape'),('linked.md','symlink'),('details.md','ambiguous')]:
            root,d=self.root();(d/'SPEC.md').write_text('---\ncompanions: ['+repr(ref)+']\n---\n# Spec\n')
            if mode=='symlink':(d/'linked.md').symlink_to(d/'details.md')
            if mode=='ambiguous':(root/'bmad/details.md').write_text('other')
            value=runtime.promote(root,arguments(d,root))
            # A project-relative alternate outside the output root must never be copied.
            if mode in ('valid','ambiguous'):
                self.assertEqual('PLAN_READY',value['state'],value)
            else:self.assertEqual('BLOCKED',value['state'],value)

    def test_ambiguous_bases_inside_output_are_rejected(self):
        root,d=self.root();(d/'_bmad-output/planning').mkdir(parents=True);(d/'_bmad-output/planning/architecture.md').write_text('alternative')
        (d/'SPEC.md').write_text('---\ncompanions: [_bmad-output/planning/architecture.md]\n---\n')
        self.assertEqual('CONDUCTOR_BMAD_COMPANION_AMBIGUOUS',runtime.promote(root,arguments(d,root))['reason_code'])

    def test_stale_approval_covers_external_companion(self):
        root,d=self.root();args=arguments(d,root);p=runtime.promote(root,args)['plan'];args.approve_plan=p['plan_id']
        (root/'bmad/_bmad-output/planning/architecture.md').write_text('changed')
        self.assertEqual('CONDUCTOR_BMAD_PLAN_APPROVAL_MISMATCH',runtime.promote(root,args)['reason_code'])
        self.assertFalse((root/p['destination']).exists())

    def test_companion_transitive_closure_and_cycles(self):
        root,d=self.root();(d/'details.md').write_text('---\ncompanions: [SPEC.md]\n---\n')
        self.assertEqual(4,len(runtime.promote(root,arguments(d,root))['plan']['source_artifacts']))

    def test_companion_yaml_variants_cannot_omit_dependencies(self):
        for front in ['companions:\n- missing.md', 'title: before---after\ncompanions: [missing.md]', '"companions": [missing.md]', "companions: [missing.md]\n<<: *hidden"]:
            root,d=self.root();(d/'SPEC.md').write_text('---\n'+front+'\n---\n# Spec\n')
            self.assertEqual('BLOCKED',runtime.promote(root,arguments(d,root))['state'])

    def test_new_version_architecture_directory_has_correct_provenance(self):
        root,d=self.root();(d/'SPEC.md').unlink();args=arguments(d,root);args.workflow='architecture'
        preview=runtime.promote(root,args);manifest=runtime.snapshot_manifest(preview['plan'])
        self.assertEqual('6.12.1-next.0',manifest['provenance']['bmad_version'])

    def test_synthetic_cli_lifecycle(self):
        from tests.bmad_6121_lifecycle import exercise
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        self.assertEqual('PASS',exercise(Path(tmp.name))['state'])
