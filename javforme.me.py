# -*- coding: UTF-8 -*-

import io
import sys
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import requests
from loguru import logger
import logging
import os.path
import subprocess
import mmap
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
}
proxies = {}
logging.basicConfig(filename='logger.log', level=logging.INFO)
# 如果代理不稳定，不推荐使用
# local showdowsocks service
# proxies example:
# proxies = {
#     "http": "socks5://127.0.0.1:1080",
#     "https": "socks5://127.0.0.1:1080",
# }
def download_file(url):
  local_filename = url.split('/')[-1]
  r = requests.get(url, stream=True)
  with open(local_filename, 'wb') as f:
    for chunk in r.iter_content(chunk_size=1024):
      if chunk:
        f.write(chunk)
        f.flush()

  return local_filename

def download(url, name, filetype):
  path = os.path.abspath(os.path.dirname(__file__)) + "/"+filetype+"/" + name
  cmd = 'wget  %s -O %s' % (url,path)
  subprocess.call(cmd, shell=True)
  return True

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
opt = Options()

opt.add_argument("--headless")
opt.add_argument('--disable-gpu')
opt.add_argument('--no-sandbox')    # 禁止沙箱模式，否则肯能会报错遇到chrome异常
# opt.add_argument('--headless')
# print(re.match(r'href="(.*?)"',r.content).span())
totalPage = []
for num in range(49):
  if(num<10):
      continue;
  logging.info("正在采集第"+str(num))
  logging.info("URL "+'http://javforme.me/studio/asian-sex-diary/page-'+str(num))

  r = requests.get('http://javforme.me/studio/asian-sex-diary/page-'+str(num))
  pattern = r'<a href="/mo(.*?)"'
  match = re.findall(pattern, r.text)
  for _dict in match:
    pageUrl = "http://javforme.me/mo" + _dict
    f = open('./logger.log')
    s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    if s.find(str.encode(pageUrl),1) != -1:
      logContent = "file exit:" + pageUrl + " jump"
      # 校验重复
      logging.info(logContent)
      continue
    f.close()

    logging.info("get " + pageUrl)
    totalPage.append(pageUrl)
    # 爬取每个分页的视频地址
    browser = webdriver.Chrome(executable_path="./chromedriver",options=opt)
    browser.get(pageUrl)
    mp4 = browser.execute_script('var mp4 = $(".jw-video").attr("src");return mp4')
    desc = browser.execute_script('var text="";$("p",".desc").each(function(){text+=$(this).text()+"\\r\\n";});return text;')
    title = browser.title

    filename = os.path.basename(mp4)


    with open(os.path.abspath(os.path.dirname(__file__))+"/mp4/"+filename+".log", 'a') as file:
      logContent = "title:" + title + "\r\n" + "content:" + desc
      file.write(logContent)
      #写入标题和内容
      file.close()

    browser.close()
    browser.quit()

    print(mp4)

    # 下载文件
    logging.info("start Download mp4:" + mp4+" title:"+title)
    download(mp4,filename,"mp4")
    # 切片
    time.sleep(10) # 休眠1秒
