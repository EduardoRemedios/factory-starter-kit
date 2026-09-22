import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from tests.bmad_6121_fixture import seed, runtime

policy = runtime.policy


class CompatibilityTests(unittest.TestCase):
    def root(self, **options):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        root = Path(tmp.name); seed(root, **options); return root

    def test_root_nested_optional_tea_and_shims(self):
        for options in ({}, {'nested':True}, {'tea':True}, {'nested':True,'tea':True,'shims':True}):
            with self.subTest(options=options):
                root = self.root(**options)
                audit = policy.capability_audit(root, 'codex', 'guarded-mcp')
                self.assertEqual('READY',audit['state'],audit['reason_code'])
                for name in ('bmad-spec','bmad-architecture','bmad-ux','bmad-review','bmad-help','bmad-deep-recon'):
                    verdict = policy.solution_context_authorization(root,name)
                    self.assertTrue(verdict['allowed'], verdict)
                self.assertEqual('BLOCKED',policy.capability_audit(root,'codex','native')['state'])

    def test_version_and_tea_commit_must_match(self):
        for old,new in [('6.12.1-next.0','6.12.1'),(policy.profile_6121()['tea_commit'],'0'*40)]:
            root=self.root(tea=True);p=root/'_bmad/_config/manifest.yaml';p.write_text(p.read_text().replace(old,new))
            self.assertEqual('CONDUCTOR_BMAD_VERSION_QUARANTINED',policy.inventory_audit(root,'claude')['reason_code'])

    def test_dependencies_must_match_not_only_skill(self):
        for rel in ['_bmad/scripts/config_utils.py','.claude/skills/bmad-review/references/lens-prose.md','.claude/skills/bmad-spec/customize.toml']:
            root=self.root();p=root/rel;p.write_text(p.read_text()+'\n# drift\n')
            self.assertFalse(policy.solution_context_authorization(root,'bmad-spec')['allowed'])
        root=self.root();(root/'.claude/skills/bmad-review/references/lens-prose.md').unlink()
        self.assertEqual('BLOCKED',policy.inventory_audit(root,'claude')['state'])

    def test_safe_preferences_and_effect_overrides(self):
        root=self.root();p=root/'_bmad/config.user.toml';p.write_text('[core]\nuser_name="Alex"\ncommunication_language="French"\n')
        self.assertTrue(policy.solution_context_authorization(root,'bmad-review')['allowed'])
        for text in ['[workflow]\non_complete="write code"\n','[workflow]\nlenses=[{code="prose",instruction="implement"}]\n','[workflow]\npersistent_facts=["file:unreviewed.md"]\n']:
            q=root/'_bmad/custom/bmad-review.user.toml';q.write_text(text)
            self.assertEqual('CONDUCTOR_BMAD_SOLUTION_PROFILE_OVERRIDE_ACTIVE',policy.solution_context_authorization(root,'bmad-review')['reason_code'])
        q.unlink();p.write_text('[core]\noutput_folder="/tmp/outside"\n')
        self.assertFalse(policy.solution_context_authorization(root,'bmad-review')['allowed'])

    def test_yaml_configuration_not_an_escape(self):
        root=self.root();p=root/'_bmad/bmm/config.yaml';p.write_text(p.read_text().replace('{project-root}/_bmad-output','/tmp/external'))
        self.assertFalse(policy.solution_context_authorization(root,'bmad-architecture')['allowed'])

    def test_alias_escape_and_duplicate_installation(self):
        root=self.root(nested=True);alias=root/'.claude/skills';alias.unlink();alias.symlink_to('/tmp')
        self.assertEqual('BLOCKED',policy.inventory_audit(root,'claude')['state'])
        self.assertFalse(policy.solution_context_authorization(root,'bmad-spec')['allowed'])
        root=self.root(nested=True);(root/'_bmad').mkdir()
        self.assertEqual('BLOCKED',policy.inventory_audit(root,'claude')['state'])

    def test_internal_file_symlink_is_rejected(self):
        root=self.root();p=root/'.claude/skills/bmad-review/references/lens-prose.md';data=p.read_text();p.unlink();target=root/'copy.md';target.write_text(data);p.symlink_to(target)
        self.assertFalse(policy.solution_context_authorization(root,'bmad-review')['allowed'])

    def test_direct_and_model_lane_events(self):
        root=self.root(nested=True)
        for name in ['bmad-review','bmad-spec','bmad-architecture','bmad-ux']:
            for event in [{'hook_event_name':'UserPromptExpansion','command_name':name},{'hook_event_name':'PreToolUse','tool_name':'Skill','tool_input':{'skill':name}}]:
                value=policy.hook_decision(root,event)
                self.assertIn('bmad/_bmad-output',value['hookSpecificOutput']['additionalContext'])
        for name in ['bmad-build','bmad-build-auto','bmad-code-review','bmad-project-context','bmad-walkthrough','bmad-unknown-future']:
            direct=policy.hook_decision(root,{'hook_event_name':'UserPromptExpansion','command_name':name})
            model=policy.hook_decision(root,{'hook_event_name':'PreToolUse','tool_name':'Skill','tool_input':{'skill':name}})
            self.assertEqual('block',direct['decision']);self.assertEqual('deny',model['hookSpecificOutput']['permissionDecision'])
        self.assertIsNone(policy.hook_decision(root,{'hook_event_name':'PreToolUse','tool_name':'Skill','tool_input':{'skill':'unrelated-tool'}}))

    def test_legacy_inventory_still_ready(self):
        from tests.test_conductor_bmad_support import seed_factory,seed_git,seed_bmad
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);r=Path(tmp.name)
        seed_git(r);seed_factory(r);seed_bmad(r,capabilities=True)
        self.assertEqual('READY',policy.inventory_audit(r,'claude')['state'])

    def test_hook_cannot_bypass_inventory_module_or_version_denial(self):
        for replacement in ["    version: unsupported", "    version: main\n  - name: bmad-loop\n    version: 1.0", "    version: main\n  - name: unknown-module\n    version: 1.0"]:
            root=self.root(tea=True);manifest=root/'_bmad/_config/manifest.yaml'
            manifest.write_text(manifest.read_text().replace('    version: main',replacement))
            self.assertFalse(policy.solution_context_authorization(root,'bmad-review')['allowed'])
            for event in [{'hook_event_name':'UserPromptExpansion','command_name':'bmad-review'},{'hook_event_name':'PreToolUse','tool_name':'Skill','tool_input':{'skill':'bmad-review'}}]:
                verdict=policy.hook_decision(root,event)
                self.assertTrue(verdict.get('decision')=='block' or verdict.get('hookSpecificOutput',{}).get('permissionDecision')=='deny')

    def test_yaml_user_overrides_and_root_hook_settings(self):
        root=self.root(nested=True);p=root/'bmad/_bmad/bmm/config.user.yaml';p.write_text('planning_artifacts: /tmp/unreviewed-target\n')
        self.assertFalse(policy.solution_context_authorization(root,'bmad-ux')['allowed'])
        p.unlink();(root/'.claude/settings.json').write_text(json.dumps({'hooks':{'PreToolUse':[{'hooks':[{'type':'command','command':'bmad-custom-hook'}]}]}}))
        self.assertEqual('BLOCKED',policy.inventory_audit(root,'claude')['state'])

    def test_tea_config_and_user_layer_cannot_redirect_writes(self):
        for filename in ['config.yaml','config.user.yaml']:
            root=self.root(tea=True);p=root/'_bmad/tea'/filename
            self.assertTrue(policy.solution_context_authorization(root,'bmad-testarch-test-design')['allowed'])
            p.write_text('test_artifacts: /tmp/unreviewed-tea\n')
            self.assertFalse(policy.solution_context_authorization(root,'bmad-testarch-test-design')['allowed'])
        root=self.root(tea=True);(root/'_bmad/tea/config.yaml').unlink()
        self.assertFalse(policy.solution_context_authorization(root,'bmad-testarch-test-design')['allowed'])

    def test_legacy_declared_nested_root_keeps_existing_root_skills(self):
        from tests.test_conductor_bmad_support import seed_factory,seed_git,seed_bmad
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);r=Path(tmp.name)
        seed_git(r);seed_factory(r);seed_bmad(r,capabilities=True)
        (r/'bmad').mkdir();(r/'_bmad').rename(r/'bmad/_bmad')
        (r/'docs/Conductor/PROJECT_CONFIG.json').write_text(json.dumps({'adapters':{'bmad':{'declared_root':'bmad/_bmad'}}}))
        self.assertEqual('READY',policy.inventory_audit(r,'claude')['state'])
        self.assertEqual(Path('.claude/skills'),policy.skill_directory(r))
        self.assertEqual(Path('_bmad-output'),policy.output_directory(r))

    def test_canonical_optional_tea_descriptor_and_readiness(self):
        import tomllib
        for nested in (False, True):
            root = self.root(tea=True, nested=nested)
            active = root / policy.active_bmad_root(root)
            agents = tomllib.loads((active / 'config.toml').read_text())['agents']
            self.assertEqual(policy.profile_6121()['tea_agents']['bmad-tea'], agents['bmad-tea'])
            for harness, route in [('claude', None), ('codex', 'guarded-mcp')]:
                audit = policy.capability_audit(root, harness, route)
                self.assertEqual('READY', audit['state'], audit['reason_code'])
            for name in ('bmad-help', 'bmad-spec', 'bmad-architecture', 'bmad-ux', 'bmad-review'):
                self.assertTrue(policy.solution_context_authorization(root, name)['allowed'])
                for event in [
                    {'hook_event_name': 'UserPromptExpansion', 'command_name': name},
                    {'hook_event_name': 'PreToolUse', 'tool_name': 'Skill', 'tool_input': {'skill': name}},
                ]:
                    verdict = policy.hook_decision(root, event)
                    self.assertIn('additionalContext', verdict['hookSpecificOutput'])
            for name in ('bmad-build', 'bmad-build-auto', 'bmad-unknown-future'):
                verdict = policy.hook_decision(root, {'hook_event_name': 'PreToolUse', 'tool_name': 'Skill', 'tool_input': {'skill': name}})
                self.assertEqual('deny', verdict['hookSpecificOutput']['permissionDecision'])

    def test_descriptor_drift_blocks_readiness_and_invocation(self):
        cases = [
            ('config.toml', 'Murat', 'Unreviewed agent'),
            ('config.toml', '[agents.bmad-tea]', '[agents.unknown-agent]'),
            ('config.toml', 'module="tea"', 'module="bmm"'),
            ('config.user.toml', '', '[agents.bmad-tea]\nname="Altered"\n'),
        ]
        for filename, old, new in cases:
            with self.subTest(filename=filename, old=old):
                root = self.root(tea=True)
                path = root / '_bmad' / filename
                original = path.read_text() if path.exists() else ''
                self.assertIn(old, original)
                path.write_text(original.replace(old, new) if old else new)
                for harness, route in [('claude', None), ('codex', 'guarded-mcp')]:
                    audit = policy.capability_audit(root, harness, route)
                    self.assertEqual('BLOCKED', audit['state'])
                    self.assertEqual('CONDUCTOR_BMAD_SOLUTION_PROFILE_OVERRIDE_ACTIVE', audit['reason_code'])
                self.assertFalse(policy.solution_context_authorization(root, 'bmad-help')['allowed'])

    def test_tea_descriptor_requires_the_pinned_installed_module(self):
        root = self.root()
        descriptor = policy.profile_6121()['tea_agents']['bmad-tea']
        with (root / '_bmad/config.toml').open('a') as stream:
            stream.write('\n[agents.bmad-tea]\n')
            for key, value in descriptor.items():
                stream.write(key + '=' + json.dumps(value, ensure_ascii=False) + '\n')
        self.assertEqual('CONDUCTOR_BMAD_SOLUTION_PROFILE_OVERRIDE_ACTIVE', policy.capability_audit(root, 'claude')['reason_code'])
        root = self.root(tea=True)
        manifest = root / '_bmad/_config/manifest.yaml'
        manifest.write_text(manifest.read_text().replace(policy.profile_6121()['tea_commit'], '0' * 40))
        self.assertEqual('CONDUCTOR_BMAD_VERSION_QUARANTINED', policy.capability_audit(root, 'claude')['reason_code'])
        self.assertFalse(policy.solution_context_authorization(root, 'bmad-help')['allowed'])

    def test_shared_configuration_failure_is_visible_before_loading(self):
        for filename, data in [('config.user.toml', '[core]\noutput_folder="/tmp/outside"\n'),
                               ('tea/config.user.yaml', 'test_artifacts: /tmp/outside\n'),
                               ('config.user.toml', 'not valid toml = [')]:
            root = self.root(tea=True)
            (root / '_bmad' / filename).write_text(data)
            for harness, route in [('claude', None), ('codex', 'guarded-mcp')]:
                audit = policy.capability_audit(root, harness, route)
                self.assertEqual('BLOCKED', audit['state'], audit)
                self.assertTrue(audit['reason_code'].startswith('CONDUCTOR_BMAD_SOLUTION_PROFILE_'))
            self.assertFalse(policy.solution_context_authorization(root, 'bmad-spec')['allowed'])

    def test_tea_descriptor_matches_pinned_public_module(self):
        import hashlib
        import yaml
        path = Path(__file__).parent / 'fixtures/bmad_6121/tea-module.yaml'
        self.assertEqual('3357b11a2e459a786eecf3f5465f060454361d6a580a443a6372a0a4ef12e834', hashlib.sha256(path.read_bytes()).hexdigest())
        agent = next(a for a in yaml.safe_load(path.read_text())['agents'] if a['code'] == 'bmad-tea')
        expected = {'module': 'tea', **{k: v for k, v in agent.items() if k != 'code'}}
        self.assertEqual({'bmad-tea': expected}, policy.profile_6121()['tea_agents'])

    def test_guarded_mcp_uses_realistic_tea_configuration(self):
        from tests.test_conductor_bmad_enforcement import FactoryBmadEnforcementTests
        loader = FactoryBmadEnforcementTests().loader()
        root = self.root(tea=True, nested=True)
        for name in ('bmad-help', 'bmad-spec'):
            loaded = loader.load_workflow({'root': str(root), 'name': name})
            self.assertEqual('CONDUCTOR_BMAD_GUARDED_LOAD_ALLOWED', loaded['reason_code'])
        (root / 'bmad/_bmad/config.user.toml').write_text('[agents.bmad-tea]\nname="Unreviewed"\n')
        blocked = loader.load_workflow({'root': str(root), 'name': 'bmad-help'})
        self.assertEqual('CONDUCTOR_BMAD_SOLUTION_PROFILE_OVERRIDE_ACTIVE', blocked['reason_code'])

    def test_6121_cannot_use_a_legacy_tea_label_to_skip_the_commit_pin(self):
        for sha in (policy.profile_6121()['tea_commit'], '0' * 40):
            root = self.root(tea=True)
            manifest = root / '_bmad/_config/manifest.yaml'
            manifest.write_text(manifest.read_text().replace('version: main', 'version: ' + policy.SUPPORTED_TEA_VERSION).replace(policy.profile_6121()['tea_commit'], sha))
            for harness, route in [('claude', None), ('codex', 'guarded-mcp')]:
                self.assertEqual('CONDUCTOR_BMAD_VERSION_QUARANTINED', policy.capability_audit(root, harness, route)['reason_code'])
            self.assertFalse(policy.solution_context_authorization(root, 'bmad-help')['allowed'])
