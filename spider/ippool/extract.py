import json

with open('ip.json') as f:
    json_data = json.load(f)

f = open('resource.py', 'w')
result = []
for i in json_data:
    result.append(i['ip'])
str_result = 'PROXIES = ' + json.dumps(result)
f.write(str_result)
f.close()
