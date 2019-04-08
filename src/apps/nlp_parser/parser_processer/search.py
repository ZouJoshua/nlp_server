# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render_to_response
from requests.exceptions import ReadTimeout
from urllib.parse import urlparse
import lxml.html
import requests, json, random
from .user_agents import user_agent_list


etree = lxml.html.etree
file1 = open("/home/zhujianan/tar/auto_parse/auto_parse/rule.json")
dic_read = file1.read()
dic1 = json.loads(dic_read)


# 表单
def search_form(request):
    return render_to_response('search_form.html')


# 从网站中抓取数据
def get_html(url1):
    header = random.choice(user_agent_list)
    try:
        requests.packages.urllib3.disable_warnings()
        r1 = requests.get(url1, headers=header, timeout=5, verify=False)
        html = r1.text
    except ReadTimeout:
        print("Readtimeout")
        html = 'timeout'
    except Exception:
        print("Others error")
        html = "Others error"
    return html


def parse(url):
    url = url.strip()
    result = {"category": [], "title": [], "tag": [], "hyperlink_text": [], "hyperlink_url": []}
    html = get_html(url)
    if html == "timeout": 
        return HttpResponse(status=408)
    elif html == "Others error":
        result["title"] = ""
        return JsonResponse(result)
    # urlparse,可以解析出url中的scheme,netloc,path,params,query,fragment
    domain = urlparse(url).netloc
    # rule.json中的属性，可更新
    if domain not in dic1:
        with open("/home/zhujianan/tar/auto_parse/auto_parse/change_rule.txt","a") as f:
            f.writelines(url)
            f.writelines("\n")
        result["title"] = ""
        return JsonResponse(result)
    p = list()
    title_join = ""
    for i in ["category", "title", "tag", "hyperlink_text", "hyperlink_url"]:
        try:
            lst = list()
            xp = dic1.get(domain).get(i)
            pt = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
            j = pt.xpath(xp)
            if len(j) > 0:
                for n in j:
                    p = n.strip().strip("\n\t")
                    lst.append(p)
                result[i] = lst
        except Exception:
            pt = ''
            print("unable to parse")
            print(url)
    result['title'] = " ".join(result.get("title"))
    return JsonResponse(result)

def search(request):
    request.encoding = 'utf-8'
    if request.method == 'POST':
        return parse(request.POST.get("website", "nothing"))
    else:
        return 'Please use the POST request'
