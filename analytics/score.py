#!/usr/bin/env python3
import json, pathlib, argparse
p=argparse.ArgumentParser(); p.add_argument("--input",default="analytics/performance.json"); a=p.parse_args()
d=json.loads(pathlib.Path(a.input).read_text())
def rate(n,d): return round(n/d,6) if d else None
out=[]
for s in d.get("snapshots",[]):
 m=s.get("metrics",{}); imp=m.get("impressions",0)
 out.append({**s,"derived":{
  "save_rate":rate(m.get("saves",0),imp),
  "pin_click_rate":rate(m.get("pin_clicks",0),imp),
  "outbound_click_rate":rate(m.get("outbound_clicks",0),imp),
  "revenue_per_1000_impressions":round((m.get("etsy_revenue_usd",0)/imp)*1000,2) if imp else None
 }})
print(json.dumps({"snapshots":out},indent=2))
