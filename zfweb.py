# -*- coding: utf-8 -*-
#_*_ conding:gbk _*_
import requests
import re

title_pattern = re.compile("信件名称\s+</div>\s+<div class=\"item-content col-8 col-md-10\">(.+?)</div>",re.S)
mail_pattern = re.compile("<div class=\"item-content col-8 col-md-10\">"
                          "\s+<pre style=\"font-size: 14px\">\s+(.+?)\s+</pre>",re.S)
requests.adapters.DEFAULT_RETRIES = 5

def getinfo(instid):
    print instid
    try:
        r = requests.get("http://111.21.38.68:65511/gzweb12345/webAppealServlet/myAffairDetail", params={'instId': instid}, stream=False)
    except requests.HTTPError as e:
        print e.message
        return False

    try:
        items=re.findall(title_pattern,r.text.encode('utf-8'))
        if len(items) == 0:
            r.close()
            return False
        title=""
        for item in items:
            for content in item:
                title = title + content
        if "无效电话" in title:
            r.close()
            return True
        if "咨询工单" in title:
            r.close()
            return True
        if "噪音" in title:
            r.close()
            return True
        print "    题目：", title
        items2=re.findall(mail_pattern,r.text)
        r.close()
        contents =""
        for item in items2:
            for content in item:
                contents= contents + content.encode('utf-8')
                #print content,
        with open('data.txt','a+') as f:
            f.write("题目："+ title +"\n内容:\n"+contents.replace(" ","") +'\n\n')
            f.close()
    except Exception as e:
        print e
        return False
    return True

start = 2018050102002000
end= 2018070102002000
print "开始时间：",int(start/100000000) ,"  结束时间",int(end/100000000)
isnull=0
for m in range(start, end, 10000000000):
    for d in range(m, m+29000000000, 100000000):
        for i in range(999):
            if getinfo(d+i):
                isnull = 0
            else:
                isnull += 1
            if isnull == 10:
                break