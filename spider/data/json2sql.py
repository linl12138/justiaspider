import json, re, sys

with open(sys.argv[1].strip()) as f:
    json_data = json.load(f)

if sys.argv[2].strip() == 'companies':
    cols = ["physical_address", "mailing_address", "phone", "name", "capabilities", "brands", "sic"]
    cols_str = ', '.join(cols)
    file_name = 'companies.sql'
    table_name = 'COMPANIES'
elif sys.argv[2].strip() == 'bailiis':
    cols = ['title', 'link', 'country']
    cols_str = ', '.join(cols)
    file_name = 'bailiis.sql'
    table_name = 'CASES'
elif sys.argv[2].strip() == 'BritishColumbias':
    cols = ['title', 'link', 'case_num', 'plaintiff', 'defendant', 'country', 'data']
    cols_str = ', '.join(cols)
    file_name = 'BritishColumbias.sql'
    table_name = 'CASES'
elif sys.argv[2].strip() == 'hkliis':
    cols = ['title', 'link', 'case_num', 'plaintiff', 'defendant', 'country']
    cols_str = ', '.join(cols)
    file_name = 'hkliis.sql'
    table_name = 'CASES'
elif sys.argv[2].strip() == 'justs':
    cols = ['title', 'case_num', 'plaintiff', 'defendant', 'country', 'data']
    cols_str = ', '.join(cols)
    file_name = 'justs.sql'
    table_name = 'CASES'
elif sys.argv[2].strip() == 'austliis':
    cols = ['title', 'link', 'country']
    cols_str = ', '.join(cols)
    file_name = 'austliis.sql'
    table_name = 'CASES'
elif sys.argv[2].strip() == 'sccs':
    cols = ['title', 'link', 'country']
    cols_str = ', '.join(cols)
    file_name = 'sccs.sql'
    table_name = 'CASES'
elif sys.argv[2].strip() == 'singapores':
    cols = ['title', 'link', 'country', 'data']
    cols_str = ', '.join(cols)
    file_name = 'singapores.sql'
    table_name = 'CASES'
elif sys.argv[2].strip() == 'newzealands':
    cols = ['title', 'case_num', 'country', 'data']
    cols_str = ', '.join(cols)
    file_name = 'newzealands.sql'
    table_name = 'CASES'
elif sys.argv[2].strip() == 'jps':
    cols = ['title', 'country', 'link']
    cols_str = ', '.join(cols)
    file_name = 'jps.sql'
    table_name = 'CASES'
elif sys.argv[2].strip() == 'krs':
    cols = ['title', 'country', 'link']
    cols_str = ', '.join(cols)
    file_name = 'krs.sql'
    table_name = 'CASES'
else:
    cols = ["Date", "Indian Port", "Item Description", "Quantity", "UQC", "U.P.USD", "FOB USD", "Assess USD", "Destination Port", "Country"]
    cols_str = ''
    for c in cols:
        cols_str += re.sub('[ . ]', '_', c).lower() + ', '
    cols_str = cols_str[:-2]
    file_name = 'seairs.sql'
    table_name = 'SEAIRS'

res = ''
f = open(file_name, 'a', encoding='utf-8')
for idx, j in enumerate(json_data):
    values = ''
    for key in cols:
        value = 'DEFAULT'
        if key in j:
            if key == 'data':
                value = '\'' + json.dumps(j[key]).replace("\'", "\'\'") + '\''
            else:
                value = '\'' + re.sub('[\'\"]', '_', j[key].replace("\'", "\'\'")) + '\'' if isinstance(j[key], str) else str(j[key]).replace("\'", "\'\'")
        values += value + ', '

    res += '(' + values[:-2] + ')' + ',\n'
    if idx % 100000 == 99999:
        f.write('INSERT INTO ' + table_name + ' (' + cols_str + ') VALUES\n')
        f.write(res[:-2] + ';')
        res = ''


if res != '':
    f.write('INSERT INTO ' + table_name + ' (' + cols_str + ') VALUES\n')
    f.write(res[:-2] + ';')

f.close()
