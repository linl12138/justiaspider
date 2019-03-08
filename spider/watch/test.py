import json
filename1 = input("please input the origin filename:")
filename2 = input("please input the refilename:")
with open (filename1+'.json','r')as f:
   json_data = json.load(f)
print(len(json_data))
for i in range(len(json_data)):
    json_data[i] = json.dumps(json_data[i])
#onlydata = list(set(json_data))#顺序会变化
onlydata = []
for item in json_data:
    if item not in onlydata:
        onlydata.append(item)
print(len(onlydata))
f = open(filename2+'.json','a')
result = []
for i in range(len(onlydata)):
    temp = json.loads(onlydata[i])#for hash
    temp['country'] = temp['country']
    temp['title'] = temp['title']
    temp['link'] = temp['link']
    result.append(temp)
redata = json.dumps(result)
f.write(redata)
f.close()

