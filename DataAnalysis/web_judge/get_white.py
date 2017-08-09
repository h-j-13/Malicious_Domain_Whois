# coding:utf-8
import requests
import re

pattern = re.compile(r'<a target=\"_blank\" href=\"(.*?)\">')
string = ''
for page_index in range(200, 501):
    print page_index
    r = requests.get("http://www.alexa.cn/siterank/" + str(page_index))
    domains = re.findall(pattern, r.text)
    for domain in domains:
        domain = domain[domain.find("//") + 2:]
        if domain.find("www.") == 0:
            domain = domain[domain.find("www.") + 4:]
        string = string + domain + '\n'
print string
w = open('white_list', 'a')
w.write(string)
w.close()
