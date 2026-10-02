#!/usr/bin/env python3
import argparse, hashlib, json, pathlib, sys
def identity(job):
 raw=(job["platform"]+"|"+job["job_id"]+"|"+job["version"]+"|"+job["asset"]["sha256"]).encode()
 return hashlib.sha256(raw).hexdigest()
def main():
 p=argparse.ArgumentParser(); p.add_argument("job"); p.add_argument("--state-dir",default="state"); p.add_argument("--acquire",action="store_true"); a=p.parse_args()
 j=json.loads(pathlib.Path(a.job).read_text()); key=identity(j); root=pathlib.Path(a.state_dir); root.mkdir(parents=True,exist_ok=True)
 posted=root/(key+".posted.json"); lock=root/(key+".lock.json")
 if posted.exists(): print(json.dumps({"allowed":False,"reason":"already_posted","key":key})); raise SystemExit(3)
 if lock.exists(): print(json.dumps({"allowed":False,"reason":"lock_exists","key":key})); raise SystemExit(4)
 if a.acquire:
  lock.write_text(json.dumps({"key":key,"job_id":j["job_id"],"version":j["version"]},indent=2)+"\n")
 print(json.dumps({"allowed":True,"key":key,"lock_acquired":bool(a.acquire)},indent=2))
if __name__=="__main__": main()
