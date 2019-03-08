# 爬取Seair Exim Solutions (https://www.seair.co.in/)进出口交易信息
## 爬虫工具
```
pip install scrapy
```
使用scrapy/quotesbot `https://github.com/scrapy/quotesbot.git`作为初始项目环境, 在spideris件夹下编写自己的爬虫文件
## 编写爬虫文件
```
import scrapy
class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'seair'
    start_urls = [
        "https://www.seair.co.in/global-trade-data/argentina-import-data.aspx"
    ]

    def parse(self, response):
        yield {
            'url': response.url,
            'hd': response.xpath('//tr/th/text()|//tr/td/text()').extract()
        }
        next_page_urls = response.xpath("//a/@href").extract()
        for next_page_url in next_page_urls:
            if next_page_url is not None:
                yield scrapy.Request(response.urljoin(next_page_url))
```
代码定义了spider name为'seair',爬虫程序起始url，针对爬取网页的response，进行html语法分析。
由于在response中使用XPath、CSS查询十分普遍，因此，Scrapy提供了两个实用的快捷方式: `response.xpath()` 及 `response.css()`。
我使用的是xpath（`https://www.w3schools.com/xml/xpath_intro.asp`）
### Selector调试
为方便在response中查询，可在安装`ipython`后运行:

```
scrapy shell https://www.seair.co.in
```

爬取目标url，使用命令：

```
response.headers
response.body
```

可查看爬取结果，抓取成功后便可在ipython中进行selector调试：

```
response.xpath('...').extract()
```
爬取数据的同时也要搜集下一级url，scrapy针对加入的url会自动去重，所以此处我简单地把所有页面的上的url都加入其中：

```
reponse.xpath('//a/@href').extract()
```

##运行爬虫
```
scrapy crawl seair -o data.json
```
##暂停重启命令,remain为存储requests文件夹路径
'''
scrapy crawl spider_name -s JOBDIR=remain
'''
爬虫名称及存储文件名自定义
##数据清洗
爬取117m数据后开始清理，scrapy文件写得比较简易，数据格式比较杂乱，但也有数据全面的优势，存在潜在价值。针对捕捉到可用数据，分析数据格式，利用正则表达式进行匹配、分析、重组。

```
"Argentina Import Sample 1", "IMPORTER NAME ", "PEPSICO DE ARGENTINA SRL,JULIO A ROCA 4735 FLORIDA", " Product Description", " IITRIC ACID.CARBOXYLIC ACIDS WITH ALCOHOL FUNCTION, BUT WITHOUT ANOTHER FUNCTION OX", "CURRENCY NAME FOB", "US Dollar", "TYPE OF OPERATION DESCRIPTION", "Import for Consumption", "FOB VALUE TOTAL IN US CURENCY", "213177.95999999999", "EXPORTER NAME", "PEPSI-COLA MANUFACTURING CO.OF URUGUAY SRL"
```

```
"Date", "Indian Port", "CTH", "Item Description", "Quantity", "UQC", "U.P.USD", "FOB USD", "Destination Port", "Country", "Duty", "23-Nov-2016", "tughlakabad", "piston rings    ", "96  ", "NOS  ", "4.78  ", "459.29  ", "colombo  ", "23-Nov-2016", "tughlakabad", "piston ring- tractor spare parts    ", "996  ", "SET  ", "1.59  ", "1580.37  ", "yangon  ", "23-Nov-2016", "tughlakabad", "piston rings    ", "696  ", "NOS  ", "3.04  ", "2115.84  ", "bandar abbas  ", "23-Nov-2016", "tughlakabad", "piston rings    ", "400  ", "NOS  ", "3.10  ", "1240.00  ", "bandar abbas  ", "23-Nov-2016", "tughlakabad", "piston rings    ", "168  ", "NOS  ", "46.52  ", "7815.83  ", "hamburg  ", "23-Nov-2016", "tughlakabad", "piston rings    ", "63  ", "NOS  ", "175.47  ", "11054.58  ", "hamburg  ", "23-Nov-2016", "nhava sheva sea", "motor vehicle spare parts a.c. piston ring kit   ", "15  ", "PCS  ", "14.56  ", "218.40  ", "durban  ", "23-Nov-2016", "nhava sheva sea", "motor vehicle spare parts a.c. piston kit   ", "15  ", "PCS  ", "14.02  ", "210.30  ", "durban  ", "23-Nov-2016", "mundra", "piston ring (parts suitable for use solely or principally with the engines) (asper invoice)  ", "20  ", "SET  ", "79.90  ", "1598.00  ", "durban  ", "23-Nov-2016", "ludhiana", "diesel engine spare parts piston ring 102mm 3+2 tc 3171cp   ", "274  ", "KGS  ", "10.79  ", "2956.20  ", "mersin  "
```

对于上述两种格式的数据分别进行清洗：

```
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
```

```
import re
f = open("seair.json", 'r')
data2 = open("data2.txt", 'ab')
count = 0
for line in f:
    searchVol = re.findall(r'"hd": \["(Date".*?)", "[0-9]{2}-[a-yA-S]{3,4}-[0-9]{4}', line, re.M|re.I)
    searchItem = re.findall(r'([0-9]{2}-[a-yA-S]{3,4}-[0-9]{4}.*)]', line, re.M|re.I)
    if len(searchVol) == 0:
        continue
    spVol =  searchVol[0].replace('"CTH", ', '').replace(', "Country", "Duty', '').replace(', "C O O", "Duty', '').split('", "')
    spItem = searchItem[0].split('", "')
    volNum = len(spVol)
    itemNum = len(spItem)
    for i in range(itemNum):
        if i % volNum == 0:
            writeLine = '{'
            if len(re.findall(r'([0-9]{2}-[a-yA-S]{3,4}-[0-9]{4})', spItem[i])) == 0:
                break
        writeLine = writeLine + "\"" + spVol[i % volNum] + "\": "
        if re.match(r'\A([0-9]+(\.[0-9]+)?)\Z', spItem[i], re.M|re.I):
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
```
整理出59w条数据后去重，由于python的set的元素具有唯一性，set在cpython解释器的实现用了hashtable，效率奇高，可用来去重：

```
#coding=utf-8
import sys, re, os
def getDictList(dict):
    regx = '\{.*\}'
    with open(dict) as f:
        data = f.read()
        return re.findall(regx, data)
def rmdp(dictList):
    return list(set(dictList))
def fileSave(dictRmdp, out):
    with open(out, 'a') as f:
        for line in dictRmdp:
            f.write(line + '\n')
def main():
    try:
        dict = sys.argv[1].strip()
        out = sys.argv[2].strip()
    except Exception, e:
        print 'error:', e
        me = os.path.basename(__file__)
        print 'usage: %s <input> <output>' %me
        print 'example: %s dict.txt dict_rmdp.txt' %me
        exit()
    dictList = getDictList(dict)
    dictRmdp = rmdp(dictList)
    fileSave(dictRmdp, out)
if __name__ == '__main__':
    main()
```

最后清理得到45w条交易数据
