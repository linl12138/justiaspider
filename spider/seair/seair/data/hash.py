#coding=utf-8
import sys, re, os
def getDictList(dict):
    regx = '\{.*\}'
    with open(dict) as f:
        data = f.read()
        return re.findall(regx, data)
def rmdp(dictList):
    return list(set(dictList))
def fileSave(dictRmdp, tar):
    first = 1
    with open(tar, 'a') as f:
        f.write('[\n')
        for line in dictRmdp:
            if first == 1:
                f.write(line)
            else:
                f.write(',\n' + line)
            first = 0
        f.write('\n]\n')
def main():
    try:
        dict = sys.argv[1].strip()
        tar = sys.argv[2].strip()
    except Exception, e:
        print 'error:', e
        me = os.path.basename(__file__)
        print 'usage: %s <input> <output>' %me
        print 'example: %s dict.txt dict_rmdp.txt' %me
        exit()
    dictList = getDictList(dict)
    dictRmdp = rmdp(dictList)
    fileSave(dictRmdp, tar)
if __name__ == '__main__':
    main()
