#!/usr/bin/env python3
import argparse, datetime as dt, hashlib, json, pathlib, sys
def key(j):
 raw=(j["platform"]+"|"+j["job_id"]+"|"+j["version"]+"|"+j["asset"]["sha256"]).encode()
 return hashlib.sha256(raw).hexdigest()
def load(path):
 p=pathlib.Path(path)
 return json.loads(p.read_text()) if p.exists() else {"schema_version":1,"items":{}}
def save(path,s):
 p=pathlib.Path(path); p.parent.mkdir(parents=True,exist_ok=True)
 tmp=p.with_suffix(p.suffix+".tmp"); tmp.write_text(json.dumps(s,indent=2,sort_keys=True)+"\n"); tmp.replace(p)
def main():
 p=argparse.ArgumentParser(); p.add_argument("action",choices=["check","acquire","posted","release"]); p.add_argument("job"); p.add_argument("--state",default="state/publishing-state.json"); p.add_argument("--pin-id"); p.add_argument("--pin-url"); p.add_argument("--verified",action="store_true"); a=p.parse_args()
 j=json.loads(pathlib.Path(a.job).read_text()); s=load(a.state); k=key(j); item=s["items"].get(k); now=dt.datetime.now(dt.timezone.utc).isoformat()
 if a.action=="check":
  print(json.dumps({"key":k,"state":item or "clear","allowed":not item},indent=2)); return
 if a.action=="acquire":
  if item: print(json.dumps({"allowed":False,"key":k,"state":item},indent=2)); raise SystemExit(4)
  s["items"][k]={"status":"publishing","job_id":j["job_id"],"version":j["version"],"acquired_at":now}; save(a.state,s); print(json.dumps({"allowed":True,"key":k},indent=2)); return
 if a.action=="posted":
  if not a.verified or not a.pin_id or not a.pin_url: raise SystemExit("Verified Pin ID and URL required.")
  if not item or item.get("status")!="publishing": raise SystemExit("Active publishing lock required.")
  s["items"][k]={"status":"posted","job_id":j["job_id"],"version":j["version"],"posted_at":now,"pin_id":a.pin_id,"pin_url":a.pin_url}; save(a.state,s); print(json.dumps(s["items"][k],indent=2)); return
 if a.action=="release":
  if item and item.get("status")=="posted": raise SystemExit("Posted state is terminal.")
  s["items"].pop(k,None); save(a.state,s); print(json.dumps({"released":True,"key":k},indent=2))
if __name__=="__main__": main()
