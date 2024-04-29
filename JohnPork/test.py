import time
import json

with open("avicii.json") as avc:
    a = dict(json.loads(avc.read()))
    m = int(time.strftime("%M")) % 10
    dt = int(time.strftime("%d"))
    mod = len(a) - 1
    res = list(a.keys())[((m + dt) * 12 + 7) % mod]
    print(res)