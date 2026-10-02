#!/usr/bin/env python3
import argparse, datetime as dt, json, pathlib
from zoneinfo import ZoneInfo
def main():
 p=argparse.ArgumentParser(); p.add_argument("--config",default="config/schedule.json"); p.add_argument("--date"); p.add_argument("--count",type=int,default=3); a=p.parse_args()
 c=json.loads(pathlib.Path(a.config).read_text()); z=ZoneInfo(c["timezone"])
 day=dt.date.fromisoformat(a.date) if a.date else dt.datetime.now(z).date()
 lo,hi=c["daily_target"]["minimum"],c["daily_target"]["maximum"]; count=max(lo,min(hi,a.count))
 slots=[]
 for s in c["slots"][:count]:
  h,m=map(int,s.split(":")); slots.append(dt.datetime.combine(day,dt.time(h,m),tzinfo=z).isoformat())
 print(json.dumps({"date":str(day),"timezone":c["timezone"],"count":count,"slots":slots},indent=2))
if __name__=="__main__": main()
