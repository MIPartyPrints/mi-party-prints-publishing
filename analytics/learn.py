#!/usr/bin/env python3
import json,pathlib,collections
p=pathlib.Path("analytics/performance.json"); d=json.loads(p.read_text())
groups=collections.defaultdict(lambda:{"impressions":0,"saves":0,"outbound_clicks":0,"n":0})
for s in d.get("snapshots",[]):
 dim=s.get("dimensions",{}); m=s.get("metrics",{})
 key=(dim.get("theme"),dim.get("marketing_job"),dim.get("creative_concept"))
 g=groups[key]; g["n"]+=1
 for x in ("impressions","saves","outbound_clicks"): g[x]+=m.get(x,0) or 0
obs=[]
for k,g in groups.items():
 imp=g["impressions"]; obs.append({"theme":k[0],"marketing_job":k[1],"creative_concept":k[2],"sample_size":g["n"],
 "impressions":imp,"save_rate":round(g["saves"]/imp,6) if imp else None,
 "outbound_click_rate":round(g["outbound_clicks"]/imp,6) if imp else None})
print(json.dumps({"observations":obs,"note":"Descriptive evidence only. Do not auto-promote a creative strategy from small samples."},indent=2))
