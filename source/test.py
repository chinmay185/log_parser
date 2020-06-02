import sys
import pandas as pd
import json
from logfmt import parse
from io import StringIO

x = sys.stdin.readlines()
x = json.dumps(x)
df = pd.read_json(x)

message = StringIO(df[0][0])
for ele in parse(message):
    for k, v in ele.items():
        print(k, v)

# for ele in x:
#     print(ele)
#     break
# print((pd.DataFrame([x][0])))
