#!/usr/bin/env python3
import argparse, hashlib, json, pathlib, sys
REQUIRED=("job_id","version","platform","approval","asset","pin")
PENDING={"","PENDING_PINTEREST_API_RESOLUTION"}
def fail(msg): print(f"ERROR: {msg}", file=sys.stderr); raise SystemExit(2)
def main():
 p=argparse.ArgumentParser(); p.add_argument("job"); p.add_argument("--asset-root",default="."); p.add_argument("--asset-file"); p.add_argument("--allow-external-asset",action="store_true"); a=p.parse_args()
 d=json.loads(pathlib.Path(a.job).read_text(encoding="utf-8"))
 for k in REQUIRED:
  if k not in d: fail(f"missing {k}")
 if d["platform"]!="pinterest": fail("platform must be pinterest")
 if d.get("paid",False): fail("paid publishing is forbidden")
 ap=d["approval"]
 if ap.get("decision")!="Approved": fail("job is not owner-approved")
 if ap.get("exact_version")!=d["version"]: fail("approval version mismatch")
 asset=d["asset"]; asset_file=a.asset_file or asset.get("path")
 if asset_file:
  path=pathlib.Path(a.asset_root)/asset_file
  if not path.is_file(): fail(f"asset not found: {path}")
  if asset.get("expected_bytes") and path.stat().st_size!=int(asset["expected_bytes"]): fail("asset byte-size mismatch")
  digest=hashlib.sha256(path.read_bytes()).hexdigest()
  if digest.lower()!=asset["sha256"].lower(): fail("asset SHA256 mismatch")
 elif not a.allow_external_asset:
  fail("exact asset bytes are required for SHA verification")
 else:
  digest=asset["sha256"]
 pin=d["pin"]
 for k in ("title","description","alt_text","link"):
  if not str(pin.get(k,"")).strip(): fail(f"pin.{k} is required")
 board_ready=str(pin.get("board_id","")).strip() not in PENDING
 state="publish_ready" if board_ready and asset_file else "commissioning_ready"
 print(json.dumps({"valid":True,"state":state,"job_id":d["job_id"],"version":d["version"],"sha256":digest,"board_resolved":board_ready,"asset_bytes_verified":bool(asset_file)},indent=2))
if __name__=="__main__": main()
