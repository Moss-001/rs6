import requests;
import subprocess
import time
import re
from lxml import etree
def open_file(content,code_func):
    with open('补还镜/rs6.js',"r",encoding="utf-8") as f:
        js_code = f.read().replace("content123",content).replace("'func_code'",code_func)
    return js_code

def writer_file(js_code):
     with open('补还镜/rs6_test.js',"w",encoding="utf-8") as f:
        f.write(js_code)

# 使用正则表达式提取 NfBCSins2OywT 的值
def extract_cookie_value(cookie_string, cookie_name):
    pattern = re.compile(rf'{cookie_name}=([^;]+)')
    match = pattern.search(cookie_string)
    if match:
        return match.group(1)
    return None
def get_cookie():
    result = subprocess.run(['node', '补还镜/rs6_test.js'], capture_output=True, text=True,encoding='utf-8')
    # 输出结果
    result_stdout = result.stdout
    cookie_value = extract_cookie_value(result_stdout, 'NfBCSins2OywT')
    return cookie_value
# def get_cookie():
#     response = requests.get("http://127.0.0.1:3000")
#     return response.text

# def extract_cookie_value(cookie_string, cookie_name):
#     cookies = cookie_string.split('; ')
#     for cookie in cookies:
#         if cookie.startswith(cookie_name + '='):
#             return cookie[len(cookie_name) + 1:]
#     return None
def get_html():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "sec-ch-ua": "Google",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows"
    }
    url = "https://www.nmpa.gov.cn/datasearch/home-index.html"
    response = requests.get(url, headers=headers)
    obj_html = etree.HTML(response.text)
    content_data = obj_html.xpath('//meta[2]/@content')[0]
    func_code=obj_html.xpath('//script[1]/text()')[0]
    js_code = open_file(content_data,func_code)
    writer_file(js_code)
    print("第一次",response.status_code)
    cookie_ = {}
    for cookie in response.cookies:
        cookie_[cookie.name]=cookie.value
    res = get_cookie()
    cookie_["NfBCSins2OywT"] = res
    cookie_string ="enable_NfBCSins2Oyw=true; "+"; ".join([f"{key}={value}" for key, value in cookie_.items()])
    print(cookie_string)

    headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7^",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie":cookie_string,
    "Pragma": "no-cache",
    "Referer": "https://www.nmpa.gov.cn/datasearch/home-index.html",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "sec-ch-ua": "Google",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows"
}
    url = "https://www.nmpa.gov.cn/datasearch/home-index.html"
    response1 = requests.get(url, headers=headers)
    print("第二次",response1.status_code)
    # print(response1.text)
    
get_html()