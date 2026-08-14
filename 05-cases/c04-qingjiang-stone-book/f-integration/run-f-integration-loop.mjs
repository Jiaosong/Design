import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import process from 'node:process';
import { fileURLToPath } from 'node:url';

const root=path.dirname(fileURLToPath(import.meta.url));
const state=JSON.parse(fs.readFileSync(path.join(root,'runtime-state.json'),'utf8'));
const schema=JSON.parse(fs.readFileSync(path.join(root,'runtime-state.schema.json'),'utf8'));
const errors=[];const checks=[];const warnings=[];
const check=(id,pass,detail)=>{checks.push({id,pass,detail});if(!pass)errors.push(`${id}: ${detail}`)};
const resolveRef=ref=>schema.$defs[ref.slice('#/$defs/'.length)];
function validate(v,r,p='$'){
 if(!r)return;if(r.$ref)return validate(v,resolveRef(r.$ref),p);
 if(r.const!==undefined&&v!==r.const)errors.push(`${p}: expected ${JSON.stringify(r.const)}, got ${JSON.stringify(v)}`);
 if(r.enum&&!r.enum.includes(v))errors.push(`${p}: invalid enum ${JSON.stringify(v)}`);
 if(r.type==='object'){if(typeof v!=='object'||v===null||Array.isArray(v)){errors.push(`${p}: expected object`);return;}for(const k of r.required||[])if(!(k in v))errors.push(`${p}.${k}: required`);for(const[k,c]of Object.entries(r.properties||{}))if(k in v)validate(v[k],c,`${p}.${k}`)}
 if(r.type==='array'){if(!Array.isArray(v)){errors.push(`${p}: expected array`);return;}if(r.minItems!==undefined&&v.length<r.minItems)errors.push(`${p}: minItems ${r.minItems}`);if(r.maxItems!==undefined&&v.length>r.maxItems)errors.push(`${p}: maxItems ${r.maxItems}`);if(r.items)v.forEach((x,i)=>validate(x,r.items,`${p}[${i}]`))}
 if(r.type==='string'&&typeof v!=='string')errors.push(`${p}: expected string`);if(r.type==='boolean'&&typeof v!=='boolean')errors.push(`${p}: expected boolean`);if(r.type==='integer'&&!Number.isInteger(v))errors.push(`${p}: expected integer`);
}
validate(state,schema);
check('SCHEMA_ENFORCEMENT',errors.length===0,errors.length?'schema validation failed':'runtime schema enforced');
check('LATEST_GOVERNANCE',state.governance.authority==='Governance v1.1.1','Governance v1.1.1 required');
check('F_OVERLAY_ONLY',state.overlay.kind==='P2_TEMPORARY_INTEGRATION_OVERLAY'&&!state.overlay.creates_p3_namespace&&state.overlay.authority_state==='NOT_AUTHORITY','F remains P2 temporary overlay');
check('G1F_HOLD',state.evidence_state.G1F==='IMPLEMENTATION_HOLD'&&state.evidence_state.field_observed===0&&state.evidence_state.field_measured===0&&state.evidence_state.field_pass==='NONE','no field truth may be inferred');
check('NO_PHYSICAL_SELECTION',state.evidence_state.physical_selected_or_located==='NONE','no physical candidate selected or located');
for(const [lane,r] of Object.entries(state.lane_receipts)){
 check(`RECEIPT_${lane}_OWNER`,Boolean(r.owner&&r.source_revision&&r.authority_state),'receipt binds owner/revision/authority');
 check(`IDENTITY_${lane}`,/^PRJ-C04-/.test(r.owner),'Current owner identity must use PRJ-C04-*');
 if(r.receipt_type==='DIRECT'){check(`RECEIPT_${lane}_HASH`,Boolean(r.payload_hash_algo&&r.payload_hash),'DIRECT receipt requires payload hash');if(r.payload_hash_algo==='GIT_BLOB_SHA1')check(`RECEIPT_${lane}_BLOB_SHA`,/^[a-f0-9]{40}$/i.test(r.payload_hash||''),'Git blob SHA must be 40 hex')}
}
check('C19_CURRENT',state.current_C_authority.semantic_stage==='C19'&&state.lane_receipts.C.semantic_stage==='C19','C19 is current cross-line state contract');
check('C17_ROUTE_RETAINED',state.current_C_authority.route_stage==='C17','C17 remains macro route contract under C19 state handoff');
const expectedSegments=['M0_PREP','M1_ARRIVAL','M2_CROSS_RIVER_CABLE','M3_SOUTH_BANK_WALKING_NETWORK','M4_OBSERVE_READ_RECOVER','M5_NATURAL_CLOSURE_WITHDRAW','M6_RETURN','M7_EXIT_MEMORY'];
check('C17_SEGMENTS',JSON.stringify(state.current_C_authority.segments)===JSON.stringify(expectedSegments),'F route diagrams retain M0-M7');
for(const invariant of ['BOAT_NEVER_UNSKIPPABLE','CABLE_SAFETY_FLOW_RETURN_GT_OBSERVATION','READING_PAGES_NO_ROUTE_SOVEREIGNTY','SINGLE_POINT_FAILURE_CANNOT_CUT_JOURNEY','NO_PHONE_RETAINS_ROUTE_SAFETY_RETURN','NATURAL_CLOSURE_DEFAULTS_WITHDRAWAL','RETURN_PRIORITY_CLOSES_NEW_CONTENT','REMOTE_SOURCE_NEVER_FIELD_VERIFIED'])check(`INV_${invariant}`,state.current_C_authority.invariants.includes(invariant),'C17 invariant must be retained');
check('MICRO_ROUTE_OPEN',state.current_C_authority.micro_route==='A_G1F_OPEN'&&state.current_C_authority.field_pass==='NONE','micro route/field remain open');
check('B_GOVERNANCE_CORRECTED',state.lane_receipts.B.owner==='PRJ-C04-EXPERIENCE-SPATIAL'&&state.lane_receipts.B.receipt_type==='DIRECT','B is owner-lane receipt inside Experience P3; no new P3');
check('B_R1_CLOSED',/B_R1_CLOSED/.test(state.lane_receipts.B.status),'B-R1 owner-lane receipt is closed at receipt scope');
check('D_R2_R3_CLOSED',/D_R2_R3_CLOSED/.test(state.lane_receipts.D.status),'D state/evidence contract consumed');
check('E_R1_R2_CLOSED',/E_R1_R2_CLOSED/.test(state.lane_receipts.E.status),'E degraded/offline and Digital-OFF contract consumed');
check('UNKNOWN_FAIL_CLOSED',state.control_sources.C19_state_contract.includes('fa7786e5'),'C19 UNKNOWN != NORMAL/OPEN contract is pinned');
check('R01_DIRECT_CLOSED',state.control_sources.R01_alignment.includes('5f02d48'),'R01 mode conflict remains closed');
check('R06_SEARCH_STOP',state.search_stop.R06.status==='PUBLIC_WEB_SEARCH_STOP_EXACT_SCIENCE_HERO_HOLD','R06 repeated public search is stopped; exact hero remains HOLD');
check('R13_SEARCH_STOP',/IMAGE_ASSET_IDENTITY_TECH_HOLD_FINAL_HERO_HOLD/.test(state.search_stop.R13.status),'R13 page evidence cannot become image-asset/final hero PASS');
for(const item of ['NEW_DIGITAL_FEATURES','NEW_PAPER_EXPANSION','NARRATIVE_EXPANSION','SYSTEM_LEVEL_PROMOTION'])check(`STOP_${item}`,state.stop_rule.active&&state.stop_rule.forbidden_progress.includes(item),'Validation Stop Rule blocks expansion/promotion');
check('NO_REPEAT_SEARCH_PROGRESS',state.stop_rule.forbidden_progress.includes('REPEATED_PUBLIC_KEYWORD_SEARCH_AS_PROGRESS'),'repeated keyword search is not project progress');
check('NO_AUTO_PROMOTION',state.decision.promote_P2===false&&state.decision.reopen_C===false,'F cannot auto-promote P2 or reopen design decisions');
check('MACHINE_CEILING',state.promotion_transition.machine_ceiling==='READY_FOR_HUMAN_DECISION'&&state.promotion_transition.human_decision_required,'machine output stops before promotion');
const ac=Object.fromEntries(state.f_acceptance_audit.map(x=>[x.id,x]));for(let i=1;i<=10;i++){const id=`F-AC${String(i).padStart(2,'0')}`;check(`AC_${id}`,Boolean(ac[id]),'all F acceptance criteria require explicit audit state')}
check('AC07_OWNER_CONTRACTS_CLOSED',ac['F-AC07']?.status==='PASS_OWNER_CONTRACTS_CLOSED_ARCHITECTURE_ONLY','D/E state contract revisions closed at architecture scope');
check('AC08_B_RECEIPT_CLOSED',ac['F-AC08']?.status==='PASS_B_OWNER_LANE_RECEIPT','B semantics are owner-receipt bound');
const rr=Object.fromEntries(state.revision_requests.map(x=>[x.id,x]));
for(const id of ['B-R1','D-R1','D-R2','D-R3','E-R1','E-R2'])check(`CLOSED_${id}`,/CLOSED_BY_DIRECT/.test(rr[id]?.status||''),`${id} closed by direct current owner receipt`);
check('FR1_MAIN_READBACK',rr['F-R1']?.status==='CLOSED_BY_MAIN_INTEGRATION_READBACK','F-R1 closed only after main integration readback');
check('FR2_MAIN_INTEGRATION',rr['F-R2']?.status==='CLOSED_IN_MAIN_INTEGRATION','F-R2 closed in merged integration overlay');
check('FR3_ACTIVE',rr['F-R3']?.status==='ENFORCED_CONTINUOUSLY'&&state.final_wording_blockers.length>0,'Final wording blocker remains active');
for(const resolved of ['B_OWNER_CANONICAL','B_LANE_RECEIPT_OWNER_READBACK','R01_MODE_ALIGNMENT','D_STATE_VOCABULARY','D_EVIDENCE_STYLING','E_DEGRADED_OFFLINE_OWNER_CONTRACT','E_DIGITAL_OFF_COMPLETENESS','F_MAIN_READBACK'])check(`RESOLVED_BLOCKER_REMOVED_${resolved}`,!state.final_wording_blockers.includes(resolved),`${resolved} must not remain after verified closure`);
for(const open of ['A_G1F','R02_EXPERT_EVIDENCE','R06_EXACT_SCIENCE_HERO_AND_FIELD_GEOMETRY','R07_FIELD_NAME_AUTHORITY','R13_IMAGE_ASSET_AND_FIELD_SAFETY'])check(`OPEN_BLOCKER_${open}`,state.final_wording_blockers.includes(open),`${open} remains promotion blocker`);
const result={loop:'C04-F-INTEGRATION',schema_version:state.schema_version,run_at:new Date().toISOString(),input_sha256:crypto.createHash('sha256').update(JSON.stringify(state)).digest('hex'),current_C_stage:state.current_C_authority.semantic_stage,route_stage:state.current_C_authority.route_stage,research_overlay_status:state.decision.research_overlay_status,decision:state.decision.result,open_owner_revisions:state.revision_requests.filter(x=>/OPEN/.test(x.status)).map(x=>x.id),closed_by_direct_receipt:state.revision_requests.filter(x=>/CLOSED_BY_DIRECT/.test(x.status)).map(x=>x.id),search_stops:state.search_stop,final_wording_blockers:state.final_wording_blockers,checks,warnings,errors,status:errors.length?'FAIL':'PASS'};
fs.writeFileSync(path.join(root,'loop-result.json'),JSON.stringify(result,null,2)+'\n');
const summary=['# C04 F Integration Loop','',`- Status: **${result.status}**`,`- Current C state contract: ${result.current_C_stage}`,`- Route contract: ${result.route_stage}`,`- Overlay: ${result.research_overlay_status}`,`- Decision: ${result.decision}`,`- Closed by DIRECT receipt: ${result.closed_by_direct_receipt.join(', ')||'none'}`,`- Open owner revisions: ${result.open_owner_revisions.join(', ')||'none'}`,`- Final wording blockers: ${result.final_wording_blockers.join(', ')}`,'','## Checks',...checks.map(c=>`- ${c.pass?'PASS':'FAIL'} — ${c.id}: ${c.detail}`),...(errors.length?['','## Errors',...errors.map(e=>`- ${e}`)]:[])].join('\n');
console.log(summary);if(process.env.GITHUB_STEP_SUMMARY)fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY,summary+'\n');if(errors.length)process.exit(1);
