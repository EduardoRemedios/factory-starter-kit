"""Synthetic CLI lifecycle; approvals here are test data, never human authority."""
import datetime
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from tests.test_conductor_bmad_6121_intake import source, arguments, runtime

ROOT=Path(__file__).resolve().parents[1]
RUN='RUN_20260917_1200_synthetic_handoff'


def exercise(root):
    directory=source(root)
    shutil.copytree(ROOT/'plugins/conductor/payload',root,dirs_exist_ok=True)
    # Payload carries an existing root config seed; preserve the fixture's declared nested root.
    config=json.loads((root/'docs/Conductor/PROJECT_CONFIG.json').read_text())
    config['adapters']={'bmad':{'declared_root':'bmad/_bmad','legacy_evidence_root':'docs/adapters/bmad/legacy-evidence'}}
    (root/'docs/Conductor/PROJECT_CONFIG.json').write_text(json.dumps(config))
    seed_plan=runtime.seed_contracts(root,None)
    assert seed_plan['state']=='PLAN_READY',seed_plan
    assert runtime.seed_contracts(root,seed_plan['plan']['plan_id'])['state']=='APPLIED'
    intake_plan=runtime.intake(root,'claude',None)
    assert intake_plan['state']=='PLAN_READY',intake_plan
    assert runtime.intake(root,'claude',intake_plan['plan']['plan_id'])['state']=='APPLIED'
    run=root/'docs/Conductor/runs'/RUN;(run/'notes').mkdir(parents=True)
    transcript=[]
    def command(argv, expected=0):
        completed=subprocess.run(argv,cwd=root,capture_output=True,text=True)
        transcript.append({'argv':argv,'exit':completed.returncode,'stdout':completed.stdout,'stderr':completed.stderr})
        assert completed.returncode==expected,transcript[-1]
        try:return json.loads(completed.stdout)
        except ValueError:return completed.stdout
    def ctl(*args,expected=0):return command(['./scripts/conductorctl',*args,'--run',RUN,'--json'],expected)
    def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
    def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
    def sign(kind,subject):
        save(run/'countersign'/f'{kind}.json',{'schema_version':1,'kind':kind,'subject_path':subject,'subject_sha256':sha(run/subject),'decision':'GO','signer':'SYNTHETIC FIXTURE - NOT A REAL HUMAN','utc':datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z'),'note':'Schema/protocol simulation only; parent run authority is separate.'})
    def promote(snapshot,**extra):
        args=arguments(directory,root,snapshot,**extra);plan=runtime.promote(root,args)
        assert plan['state']=='PLAN_READY',plan
        args.approve_plan=plan['plan']['plan_id'];result=runtime.promote(root,args)
        assert result['state']=='APPLIED',result
        return result
    first=promote('synthetic-v1')
    # Hardening feedback goes to the memlog. Regenerate the whole fixture Spec from its
    # explicit input; this deterministic renderer stands in for BMAD authorship, not AI-quality proof.
    command(['./scripts/conductor-python','bmad/_bmad/scripts/memlog.py','append','--workspace',str(directory),'--type','decision','--text','SYNTHETIC BA decision: error copy is Logout failed; please retry.'])
    (directory/'SPEC.md').write_text('---\ncompanions: [details.md, ../../planning/architecture.md]\n---\n# Session error\nShow a recoverable error when logout fails.\n## Success\nExact copy: Logout failed; please retry.\n')
    second=promote('synthetic-v2',supersedes_snapshot_id='synthetic-v1',supersedes_sha256=first['aggregate_sha256'])
    snapshot=root/'docs/upstream/bmad/synthetic-v2/SNAPSHOT_MANIFEST.json'
    manifest_data=json.loads(snapshot.read_text());provenance=manifest_data['provenance']
    claim={'schema_version':1,'receipt_type':'BMAD_CLAIM_DISPOSITIONS','snapshot':{'snapshot_id':'synthetic-v2','aggregate_sha256':second['aggregate_sha256'],'path':'docs/upstream/bmad/synthetic-v2'},'claims':[{'claim_id':'CAP-1','outcome':'ACCEPTED','rationale':'Synthetic reviewer accepts the reconciled error copy','intent_reference':'R-001','reviewer':'SYNTHETIC FIXTURE','conflict_or_supersession':'NONE'}]}
    claim['aggregate_sha256']=runtime.digest_bytes(runtime.canonical(claim));save(run/'BMAD_CLAIM_DISPOSITIONS.json',claim)
    fields={'BMAD Evidence Type':'SOLUTION_CONTEXT','BMAD Snapshot ID':'synthetic-v2','BMAD Snapshot SHA-256':second['aggregate_sha256'],'BMAD Policy Version':manifest_data['policy_version'],'BMAD Promotion Plan ID':provenance['promotion_plan_id'],'BMAD Solution Plan Identity':provenance['plan_identity'],'BMAD Claim Receipt':(run/'BMAD_CLAIM_DISPOSITIONS.json').relative_to(root).as_posix(),'BMAD Authority':'EVIDENCE_ONLY','BMAD Context Freeze':'Brief Purple PASS'}
    (run/'raw_brief.md').write_text('# Synthetic handoff brief\n'+''.join(f'- {k}: `{v}`\n' for k,v in fields.items()))
    preflight=command(['./scripts/conductor-python','scripts/conductor_project_preflight','--run',RUN,'--json']);assert preflight['status']=='PASS',preflight
    check={'id':'VM-001','tier':'V2','type':'test','requirement_ids':['R-001'],'description':'Delivered copy matches the reconciled requirement','command':['./scripts/conductor-python','-c',"from pathlib import Path; assert Path('delivery.txt').read_text() == 'Logout failed; please retry.\\n'"],'expected_exit':0,'halt_on_failure':True,'evidence_path':'receipts/VM-001.json'}
    manifest={'schema_version':2,'run_id':RUN,'execution_mode':'EXECUTION_ENABLED','execution_order':['VM-001'],'checks':[check]}
    save(run/'verification_manifest.yaml',manifest);save(run/'verification_definitions.json',manifest)
    intent={'schema_version':1,'run_id':RUN,'goal':'Synthetic handoff protocol: deliver the reconciled error copy','requirements':[{'id':'R-001','statement':'Use the reconciled logout error message','acceptance':'Exact reviewed message matches delivered bytes','severity':'blocking'}],'constraints':[],'scope_in':['One disposable text delivery'],'scope_out':['Real customer work and real approval'],'sources':[{'kind':'upstream_snapshot','ref':snapshot.relative_to(root).as_posix(),'sha256':sha(snapshot)},{'kind':'spec','ref':(run/'verification_definitions.json').relative_to(root).as_posix(),'sha256':sha(run/'verification_definitions.json')}],'verification_requirements':[{'id':'VM-001','requirement_ids':['R-001'],'tier':'V2','description':'Message byte comparison'}],'budget':{'model':'synthetic protocol fixture','effort_g2':'high','effort_g3':'high'},'execution_mode':'EXECUTION_ENABLED','done_definition':'Runner check and synthetic completion protocol pass'}
    save(run/'intent_pack.json',intent);(run/'EXECUTION_MODE.txt').write_text('EXECUTION_ENABLED\n')
    assert ctl('contract-lint','intent')['state']=='INTENT_DRAFT'
    sign('INTENT_LOCK','intent_pack.json');sign('EXECUTION_GO','intent_pack.json')
    assert ctl('contract-lint','intent')['state']=='INTENT_LOCKED'
    ctl('postimage','capture','--root','docs/upstream/bmad')
    (root/'delivery.txt').write_text('Logout failed; please retry.\n')
    ctl('receipts','run');ctl('postimage','compare')
    assert ctl('contract-lint','execution','--require-complete')['status']=='PASS'
    report=run/'notes/synthetic-review.md';report.write_text('# Synthetic reviewer fixture\nThe protocol simulator checked exact message bytes, runner receipt and snapshot preservation. This is not a real fresh-context human or AI review and authorizes no customer work.\n')
    receipt=run/'receipts/VM-001.json'
    statement={'schema_version':1,'run_id':RUN,'intent_pack_sha256':sha(run/'intent_pack.json'),'rows':[{'requirement_id':'R-001','status':'verified','evidence':[{'check_id':'VM-001','receipt_path':'receipts/VM-001.json','receipt_sha256':sha(receipt)}]}],'verifier':{'report_path':'notes/synthetic-review.md','report_sha256':sha(report),'fresh_context':True},'derived_state':'READY','handoff_state':'REVIEW_READY'}
    save(run/'statement_of_completion.json',statement)
    assert ctl('contract-lint','completion')['state']=='COMPLETION_DRAFT'
    sign('COMPLETION','statement_of_completion.json')
    final=ctl('contract-lint','completion');assert final['state']=='COMPLETION_COUNTERSIGNED'
    save(run/'notes/cli-transcript.json',transcript)
    return {'state':'PASS','scope':'Synthetic protocol and data flow only; no model authorship or independent-review quality claim','run':str(run),'first_snapshot':first,'reconciled_snapshot':second,'transcript':transcript,'completion':final}
