#!/usr/bin/env python3
"""Pinterest publisher boundary. Defaults to dry-run and refuses paid actions."""
import argparse, json, os, pathlib, urllib.request, urllib.error
API="https://api.pinterest.com/v5"
def request(method,path,token,payload=None):
 data=None if payload is None else json.dumps(payload).encode()
 req=urllib.request.Request(API+path,data=data,method=method,headers={"Authorization":f"Bearer {token}","Content-Type":"application/json"})
 try:
  with urllib.request.urlopen(req,timeout=30) as r: return json.loads(r.read().decode())
 except urllib.error.HTTPError as e:
  raise RuntimeError(f"Pinterest API HTTP {e.code}: {e.read().decode(errors='replace')}")
def payload(job,media_source):
 p=job["pin"]
 return {"board_id":p["board_id"],"title":p["title"],"description":p["description"],"alt_text":p["alt_text"],"link":p["link"],"media_source":media_source}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("job"); ap.add_argument("--media-url"); ap.add_argument("--execute",action="store_true"); a=ap.parse_args()
 job=json.loads(pathlib.Path(a.job).read_text())
 if job.get("paid",False): raise SystemExit("Paid actions are forbidden.")
 if job["approval"]["decision"]!="Approved" or job["approval"]["exact_version"]!=job["version"]: raise SystemExit("Exact owner approval required.")
 if not a.media_url: raise SystemExit("A stable HTTPS media URL is required at publish time.")
 body=payload(job,{"source_type":"image_url","url":a.media_url})
 if not a.execute:
  print(json.dumps({"mode":"DRY_RUN","endpoint":"/pins","payload":body},indent=2)); return
 token=os.environ.get("PINTEREST_ACCESS_TOKEN")
 if not token: raise SystemExit("PINTEREST_ACCESS_TOKEN secret is missing.")
 created=request("POST","/pins",token,body)
 pin_id=str(created.get("id",""))
 if not pin_id: raise SystemExit("Pinterest response did not contain a Pin ID.")
 verified=request("GET",f"/pins/{pin_id}",token)
 print(json.dumps({"mode":"EXECUTED","created":created,"verified":verified},indent=2))
if __name__=="__main__": main()
