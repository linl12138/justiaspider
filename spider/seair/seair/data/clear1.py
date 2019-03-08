import re
f = open("seair.json", 'r')
data1 = open("data1.txt", 'ab')
for line in f:
    subLine = re.sub(r'("Argentina Import Sample [0-9]+", )', '', line)
    searchObj = re.findall( r'(IMPORTER NAME.*?"PAYMENT VALUE_USD6", ".*?")', subLine, re.M|re.I )
    for item in searchObj:
        item = item[0:-1]
        writeLine = '{'
        sp = item.split('", "')
        for i in range(0, len(sp), 2):
            if i == len(sp) - 1:
                break
            if sp[i] == 'IMPORTER NAME ' and writeLine != '{':
                writeLine = writeLine[0:-2] + '}\n'
                data1.write(writeLine)
                writeLine = '{"IMPORTER NAME": '
            else:
                writeLine = writeLine + "\"" + sp[i] + "\": "
            if re.match(r'\A([0-9]+(\.[0-9]+)?)\Z', sp[i + 1], re.M|re.I):
                writeLine = writeLine + sp[i + 1] + ', '
            else:
                writeLine = writeLine + "\"" + sp[i + 1] + "\", "
        writeLine = writeLine[0:-2] + '}\n'
        data1.write(writeLine)
f.close()
data1.close()

