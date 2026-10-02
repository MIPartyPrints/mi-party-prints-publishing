#!/usr/bin/env python3
import argparse, json
RETRYABLE={408,429,500,502,503,504}
DELAYS=[15,60,240]
p=argparse.ArgumentParser(); p.add_argument("--http-status",type=int,required=True); p.add_argument("--attempt",type=int,required=True); a=p.parse_args()
retry=a.http_status in RETRYABLE and 1<=a.attempt<=len(DELAYS)
print(json.dumps({"retry":retry,"attempt":a.attempt,"delay_minutes":DELAYS[a.attempt-1] if retry else None,"action":"retry" if retry else "hold_for_review"},indent=2))
