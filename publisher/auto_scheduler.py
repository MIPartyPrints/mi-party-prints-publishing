#!/usr/bin/env python3
import argparse, datetime as dt, hashlib, json, pathlib
from zoneinfo import ZoneInfo

def ident(j):
 raw=(j["platform"]+"|"+j["job_id"]+"|"+j["version"]+"|"+j["asset"]["sha256"]).encode()
 return hashlib.sha256(raw).hexdigest()

def main():
 p=argparse.ArgumentParser(); p.add_argument("--config",required=True); p.add_argument("--jobs-dir",required=True); p.add_argument("--state",required=True); p.add_argument("--output",required=True); p.add_argument("--now"); a=p.parse_args()
 cfg=json.loads(pathlib.Path(a.config).read_text()); tz=ZoneInfo(cfg["timezone"])
 now=dt.datetime.fromisoformat(a.now).astimezone(tz) if a.now else dt.datetime.now(tz)
 state_path=pathlib.Path(a.state); state=json.loads(state_path.read_text()) if state_path.exists() else {"items":{}}
 slots=cfg["slots"][:cfg["daily_target"]["minimum"]]
 due=[]
 for s in slots:
  h,m=map(int,s.split(":")); t=now.replace(hour=h,minute=m,second=0,microsecond=0)
  # Hourly runner may claim a slot during the following 70 minutes.
  if t <= now < t+dt.timedelta(minutes=70): due.append(t)
 if not due:
  result={"action":"none","reason":"no_due_slot","local_time":now.isoformat()}
 else:
  candidates=[]
  for path in pathlib.Path(a.jobs_dir).glob("*.json"):
   try: j=json.loads(path.read_text())
   except Exception: continue
   q=j.get("queue",{})
   if j.get("paid",False) or j.get("platform")!="pinterest": continue
   if j.get("approval",{}).get("decision")!="Approved" or j.get("approval",{}).get("exact_version")!=j.get("version"): continue
   if q.get("status","approved") not in {"approved","scheduled","retry_wait"}: continue
   nb=q.get("not_before")
   if nb and dt.datetime.fromisoformat(nb).astimezone(tz)>now: continue
   k=ident(j)
   if k in state.get("items",{}): continue
   candidates.append((q.get("priority",100),q.get("approved_at","9999"),str(path),j,k))
  candidates.sort(key=lambda x:(x[0],x[1],x[2]))
  if not candidates:
   result={"action":"none","reason":"no_eligible_approved_job","slot":due[-1].isoformat()}
  else:
   _,_,path,j,k=candidates[0]
   result={"action":"selected","slot":due[-1].isoformat(),"job_path":path,"job_id":j["job_id"],"version":j["version"],"identity":k,"commissioning_only":True}
 pathlib.Path(a.output).write_text(json.dumps(result,indent=2)+"\n"); print(json.dumps(result,indent=2))
if __name__=="__main__": main()
