import json

json_data = json.load(open('bailii.json'))
f = open('bailii2.json', 'a')
result = []
for i in range(len(json_data)):
    json_data[i] = json.dumps(json_data[i])

b = list(set(json_data))
for j in range(len(b)):
    tmp = json.loads(b[j])
    if tmp['title'] != "Redirection" and not "BAILII - All Cases page" in tmp['title']:
        tmp['country'] = 'UK'
        result.append(tmp)
json = json.dumps(result)
f.write(json)
f.close()
