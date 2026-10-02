#!/usr/bin/env python3
import argparse, hashlib, json, pathlib, sys
REQUIRED=("job_id","version","platform","approval","asset","pin")
def fail(msg): print(f"ERROR: {msg}", file=sys.stderr); raise SystemExit(2)
def main():
 p=argparse.ArgumentParser(); p.add_argument("job"); p.add_argument("--asset-root",default="."); a=p.parse_args()
 d=json.loads(pathlib.Path(a.job).read_text(encoding="utf-8"))
 for k in REQUIRED:
  if k not in d: fail(f"missing {k}")
 if d["platform"]!="pinterest": fail("platform must be pinterest")
 ap=d["approval"]
 if ap.get("decision")!="Approved": fail("job is not owner-approved")
 if ap.get("exact_version")!=d["version"]: fail("approval version mismatch")
 asset=d["asset"]; path=pathlib.Path(a.asset_root)/asset["path"]
 if not path.is_file(): fail(f"asset not found: {path}")
 digest=hashlib.sha256(path.read_bytes()).hexdigest()
 if digest.lower()!=asset["sha256"].lower(): fail("asset SHA256 mismatch")
 pin=d["pin"]
 for k in ("board_id","title","description","alt_text","link"):
  if not str(pin.get(k,"")).strip(): fail(f"pin.{k} is required")
 if d.get("paid",False): fail("paid publishing is forbidden")
 print(json.dumps({"valid":True,"job_id":d["job_id"],"version":d["version"],"sha256":digest},indent=2))
if __name__=="__main__": main()
