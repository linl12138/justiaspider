import json
import re
with open('court.json', 'r') as f:
    json_data = json.load(f)

f = open('court2.json', 'a')
result = []
for json_index in range(len(json_data)):
    item = {}
    data ={}
    for key in json_data[json_index]:
        json_data[json_index][key] = re.sub(r'[^\x00-\x7f]', r'', json_data[json_index][key])
        json_data[json_index][key] = re.sub(r'\'[s] ', r'', json_data[json_index][key]).replace("'", "")
    if not json_data[json_index].has_key('title') or len(json_data[json_index]['title']) < 2:
        continue
    if json_data[json_index].has_key('plaintiff') and len(json_data[json_index]['plaintiff'])>150:
        continue
    if json_data[json_index].has_key('defendant') and len(json_data[json_index]['defendant'])>150:
        continue
    if json_data[json_index].has_key('counsel_for_plaintiff') and len(json_data[json_index]['counsel_for_plaintiff'])>150:
        continue
    if json_data[json_index].has_key('counsel_for_defendant') and len(json_data[json_index]['counsel_for_defendant'])>150:
        continue
    if not json_data[json_index].has_key('plaintiff') or not json_data[json_index].has_key('defendant'):
        continue
    item['title'] = json_data[json_index]['title'].replace('\r', '').replace('\n', '').strip(')').strip('(')
    item['country'] = json_data[json_index]['country']
    item['link'] = json_data[json_index]['link']
    if json_data[json_index].has_key('case_num'):
        item['case_num'] = json_data[json_index]['case_num']
    if json_data[json_index].has_key('plaintiff') and json_data[json_index].has_key('defendant'):
        item['plaintiff'] = json_data[json_index]['plaintiff'].replace('\r', '').replace('\n', '').strip(')').strip('(')
        item['defendant'] = json_data[json_index]['defendant'].replace('\r', '').replace('\n', '').strip(')').strip('(')
    if json_data[json_index].has_key('counsel_for_plaintiff'):
        data['counsel_for_plaintiff'] = json_data[json_index]['counsel_for_plaintiff'].replace('\r', '').replace('\n', '').strip(')').strip('(')
    if json_data[json_index].has_key('counsel_for_defendant'):
        data['counsel_for_defendant'] = json_data[json_index]['counsel_for_defendant'].replace('\r', '').replace('\n', '').strip(')').strip('(')
    if len(data) > 0:
        item['data'] = data
    result.append(item)
print len(result)
json = json.dumps(result)
f.write(json)
f.close()
