#!/usr/bin/env python3
import argparse,json,pathlib
p=argparse.ArgumentParser(); p.add_argument("--state",default="state/publishing-state.json"); a=p.parse_args()
s=json.loads(pathlib.Path(a.state).read_text()); unresolved=[]
for k,v in s.get("items",{}).items():
 if v.get("status")=="publishing": unresolved.append({"identity":k,**v})
print(json.dumps({"unresolved_count":len(unresolved),"items":unresolved},indent=2))
raise SystemExit(1 if unresolved else 0)
