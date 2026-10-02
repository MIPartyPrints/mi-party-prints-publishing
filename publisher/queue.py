#!/usr/bin/env python3
import argparse, datetime as dt, json, pathlib
def eligible(j,now):
 q=j.get("queue",{})
 if j.get("paid") or j.get("approval",{}).get("decision")!="Approved": return False
 if j.get("approval",{}).get("exact_version")!=j.get("version"): return False
 if q.get("status") in {"publishing","posted","cancelled","hold"}: return False
 n=q.get("not_before")
 return not n or dt.datetime.fromisoformat(n).astimezone(dt.timezone.utc)<=now
def main():
 p=argparse.ArgumentParser(); p.add_argument("jobs_dir"); p.add_argument("--now"); a=p.parse_args()
 now=dt.datetime.fromisoformat(a.now).astimezone(dt.timezone.utc) if a.now else dt.datetime.now(dt.timezone.utc)
 found=[]
 for path in pathlib.Path(a.jobs_dir).glob("*.json"):
  try: j=json.loads(path.read_text())
  except Exception: continue
  if eligible(j,now):
   q=j.get("queue",{}); found.append((q.get("priority",100),q.get("approved_at","9999"),str(path),j))
 if not found: print(json.dumps({"selected":None})); return
 found.sort(key=lambda x:(x[0],x[1],x[2])); _,_,path,j=found[0]
 print(json.dumps({"selected":path,"job_id":j["job_id"],"version":j["version"]},indent=2))
if __name__=="__main__": main()
