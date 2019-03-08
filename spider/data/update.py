#coding=utf-8
import json,sys

data_name = sys.argv[1].strip()
with open(data_name + '.json') as f:
    data_ori = json.load(f)
with open(data_name[:-1] + '.json') as f:
    data_inc = json.load(f)
f1 = open(data_name + '.json', 'w')
f2 = open(data_name[:-1] + '.json', 'w')
len_ori = len(data_ori)
data_uni = data_ori + data_inc
for i in range(len(data_uni)):
    data_uni[i] = json.dumps(data_uni[i])
data_new = list(set(data_uni))
data_new.sort(key=data_uni.index)
for i in range(len(data_new)):
    data_new[i] = json.loads(data_new[i])
print str(len(data_new)) + ':' + str(len(data_uni)) + ':' + str(len(data_new) - len_ori)
f1.write(json.dumps(data_new))
f2.write(json.dumps(data_new[len_ori:]))
f1.close()
f2.close()
