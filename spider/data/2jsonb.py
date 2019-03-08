import sys,json

with open(sys.argv[1] + '.json','r') as f:
    json_data = json.load(f)

f = open(sys.argv[1] + '2.json', 'a')
result = []

for i in range(len(json_data)):
    json_data[i] = json.dumps(json_data[i])
hashed_data = list(set(json_data))

for i in range(len(hashed_data)):
    hashed_data[i] = json.loads(hashed_data[i])
json_data = hashed_data

if sys.argv[1] == 'just':
    for json_index in range(len(json_data)):
        item = {}
        data = {}
        item['country'] = json_data[json_index]['country']
        item['title'] = json_data[json_index]['title'].replace('\n', '').strip()
        if not 'v.' in item['title']:
            continue
    item['plaintiff'] = json_data[json_index]['plaintiff']
    item['defendant'] = json_data[json_index]['defendant']
    item['case_num'] = json_data[json_index]['case_num']
    data['filed'] = json_data[json_index]['filed']
    data['court'] = json_data[json_index]['court']
    data['Presiding_Judge'] = json_data[json_index]['Presiding_Judge']
    data['nature_suit'] = json_data[json_index]['nature_suit']
    data['cause_action'] = json_data[json_index]['cause_action']
    for idx, val in enumerate(json_data[json_index]['jury_demanded']):
        json_data[json_index]['jury_demanded'][idx] = val.replace('\n', '').strip()
        data['jury_demanded'] = json_data[json_index]['jury_demanded']
        item['data'] = data
        result.append(item)
elif sys.argv[1] == 'singapore':
    for json_index in range(len(json_data)):
        item = {}
        data = {}
        item['country'] = json_data[json_index]['country']
        item['title'] = json_data[json_index]['title']
        item['link'] = json_data[json_index]['link']
        data['court'] = json_data[json_index]['court']
        item['data'] = data
        result.append(item)
elif sys.argv[1] == 'newzealand':
    for json_index in range(len(json_data)):
        item = {}
        data = {}
        item['country'] = json_data[json_index]['country']
        item['title'] = json_data[json_index]['title']
        item['case_num'] = json_data[json_index]['case_num']
        data['summary'] = json_data[json_index]['summary']
        item['data'] = data
        result.append(item)
elif sys.argv[1] == 'kr':
    for json_index in range(len(json_data)):
        item = {}
        item['country'] = json_data[json_index]['country']
        item['title'] = json_data[json_index]['title'].strip()
        item['link'] = json_data[json_index]['link']
        result.append(item)
else:
    result = json_data
json = json.dumps(result)
f.write(json)
f.close()
