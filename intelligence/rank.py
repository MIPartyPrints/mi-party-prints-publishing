#!/usr/bin/env python3
import json,pathlib,datetime
opp=json.loads(pathlib.Path("intelligence/opportunities.json").read_text()).get("opportunities",[])
def evidence(o):
 s=o.get("signals",{}); vals=[s.get("etsy_orders"),s.get("etsy_revenue_usd"),s.get("pinterest_outbound_clicks"),s.get("market_signal")]
 return sum(v is not None for v in vals)
def lane(o):
 if o.get("maturity")=="new": return "exploration"
 if o.get("entity_type")=="product" and o.get("maturity") in ("new","learning"): return "exploration"
 return "established"
out=[]
for o in opp:
 out.append({**o,"planning_lane":lane(o),"evidence_fields_present":evidence(o),
  "guardrail":"Missing history is neutral; compare raw signals and sample size before allocation."})
print(json.dumps({"opportunities":out},indent=2))
