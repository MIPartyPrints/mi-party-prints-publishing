#!/usr/bin/env python3
import argparse, datetime as dt, hashlib, json, pathlib
p=argparse.ArgumentParser(); p.add_argument("job"); p.add_argument("--pin-id",required=True); p.add_argument("--pin-url",required=True); p.add_argument("--verified",action="store_true"); p.add_argument("--output",required=True); a=p.parse_args()
if not a.verified: raise SystemExit("Verification required before Posted receipt.")
j=json.loads(pathlib.Path(a.job).read_text())
r={"job_id":j["job_id"],"version":j["version"],"platform":"pinterest","pin_id":a.pin_id,"pin_url":a.pin_url,"verified":True,"published_at":dt.datetime.now(dt.timezone.utc).isoformat(),"asset_sha256":j["asset"]["sha256"],"destination":j["pin"]["link"],"board_id":j["pin"]["board_id"]}
r["receipt_sha256"]=hashlib.sha256(json.dumps(r,sort_keys=True,separators=(",",":")).encode()).hexdigest()
pathlib.Path(a.output).parent.mkdir(parents=True,exist_ok=True); pathlib.Path(a.output).write_text(json.dumps(r,indent=2)+"\n"); print(json.dumps(r,indent=2))
