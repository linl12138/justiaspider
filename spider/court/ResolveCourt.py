import json
import re

json_data = json.load(open('test.json'))
f = open('court.json', 'a')
result = []
noplaintiff = 0
nocounsel = 0
for json_index in range(len(json_data)):
    txt = json_data[json_index]['txt']
    item = {}

    date = re.findall(r'date:\s*([0-9]{8})', txt, re.M|re.I)
    docket = re.findall(r'docket:\s*(.*)Registry', txt, re.M|re.I)
    if date and docket:
        item['date'] = date[0]
        item['case_num'] = docket[0]

    plaintiff = re.findall(r'between:(.*?)Plaintiff', txt, re.S|re.I)
    if not plaintiff:
        plaintiff = re.findall(r'between:(.*?)Respondent', txt, re.S|re.I)
    defendant = re.findall(r'Plaintiff.*?And(.*?)Defendant.*?before', txt, re.S|re.I)
    if not defendant:
        defendant = re.findall(r'Respondent.*?And(.*?)Appellant.*?before', txt, re.S|re.I)
    if plaintiff and defendant:
        item['plaintiff'] = plaintiff[0].strip(':')
        item['defendant'] = defendant[0].strip(':')
    else:
        noplaintiff += 1

    counsel_for_plaintiff = re.findall(r'Counsel for.*?Plaintiff(.*?)Counsel for.*?Defendant', txt, re.S|re.I)
    counsel_for_defendant = re.findall(r'Counsel for.*?defendant(.*?)[(Date and Place)|(Place and Date)]', txt, re.S|re.I)
    if not counsel_for_defendant and not counsel_for_plaintiff:
        counsel_for_plaintiff = re.findall(r'Counsel for.*?Respondent(.*?)Counsel for.*?Appellant', txt, re.S|re.I)
        counsel_for_defendant = re.findall(r'Counsel for.*?Appellant(.*?)[(Date and Place)|(Place and Date)]', txt, re.S|re.I)
    if counsel_for_plaintiff and counsel_for_defendant:
        item['counsel_for_plaintiff'] = counsel_for_plaintiff[0].strip(':')
        item['counsel_for_defendant'] = counsel_for_defendant[0].strip(':')
    else:
        nocounsel += 1

    item['country'] = 'Canada'
    item['link'] = json_data[json_index]['url']
    item['title'] = json_data[json_index]['title']
    result.append(item)
    print str(len(result)) + ' nopliantiff' + str(noplaintiff) + ' nocounsel' + str(nocounsel)
json = json.dumps(result)
f.write(json)
f.close()
