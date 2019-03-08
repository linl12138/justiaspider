import re
f = open("seair.json", 'r')
data2 = open("data2.txt", 'ab')
count = 0
for line in f:
    searchVol = re.findall(r'"hd": \["(Date".*?)", "[0-9]{2}-[a-yA-S]{3,4}-[0-9]{4}', line, re.M|re.I)
    searchItem = re.findall(r'([0-9]{2}-[a-yA-S]{3,4}-[0-9]{4}.*)"]', line, re.M|re.I)
    if len(searchVol) == 0:
        continue
    spVol =  searchVol[0].replace('"CTH", ', '').replace('", "Country", "Duty', '').replace('", "C O O", "Duty', '').replace(', "C O O"', '').split('", "')
    spItem = searchItem[0].split('", "')
    volNum = len(spVol)
    itemNum = len(spItem)
    for i in range(itemNum):
        dis = -2
        spItem[i] = spItem[i].strip()
        if i % volNum == 0:
            writeLine = '{'
            if len(re.findall(r'([0-9]{2}-[a-yA-S]{3,4}-[0-9]{4})', spItem[i])) == 0:
                break
        writeLine = writeLine + "\"" + spVol[i % volNum] + "\": "
        if re.match(r'\A([0-9]+(\.[0-9]+)?)\s*\Z', spItem[i], re.M|re.I):
            writeLine = writeLine + spItem[i] + ', '
        else:
            writeLine = writeLine + "\"" + spItem[i] + "\", "
        if i % volNum == volNum - 1:
            writeLine = writeLine[0:-2] + '}\n'
            data2.write(writeLine)
            count += 1
print count
f.close()
data2.close()
