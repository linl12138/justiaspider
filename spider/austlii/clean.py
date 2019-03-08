import json

with open('austlii.json') as f:
    json_data = json.load(f)

f = open('austlii2.json', 'a')
result = []
for i in range(len(json_data)):
    json_data[i]['country'] = 'Australia'
    result.append(json_data[i])
json = json.dumps(result)
f.write(json)
f.close()
