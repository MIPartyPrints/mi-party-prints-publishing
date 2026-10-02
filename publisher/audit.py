#!/usr/bin/env python3
import argparse,json,pathlib
p=argparse.ArgumentParser(); p.add_argument("--jobs-dir",default="jobs"); p.add_argument("--state",default="state/publishing-state.json"); a=p.parse_args()
s=json.loads(pathlib.Path(a.state).read_text()); out={"approved":0,"blocked":0,"posted":0,"publishing":0,"jobs":[]}
for path in sorted(pathlib.Path(a.jobs_dir).glob("*.json")):
 try:j=json.loads(path.read_text())
 except:continue
 if j.get("job_id","").startswith("EXAMPLE"):continue
 status=j.get("queue",{}).get("status","approved"); out["approved"]+=status in {"approved","scheduled","retry_wait"}
 out["jobs"].append({"job_id":j.get("job_id"),"version":j.get("version"),"queue":status,"board_id":j.get("pin",{}).get("board_id")})
for v in s.get("items",{}).values():
 out["posted"]+=v.get("status")=="posted"; out["publishing"]+=v.get("status")=="publishing"
print(json.dumps(out,indent=2))
