import requests
# urlparse return
#   scheme='https', netloc='www.geeksforgeeks.org', path='/data-structure', params='', query='', fragment='fragment'
from urllib.parse import urlparse
import os
from datetime import datetime
import pytz
import sys
import re
from bs4 import BeautifulSoup

# url validation regex
regex = re.compile(
  r'^(?:http|ftp)s?://' # http:// or https://
  r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
  r'localhost|' #localhost...
  r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
  r'(?::\d+)?' # optional port
  r'(?:/?|[/?]\S+)$', re.IGNORECASE)

argv = sys.argv[1:]
urls = []
params = []
for arg in argv:
  if (arg.startswith('--')):
    params.append(arg)
  else:
    urls.append(arg)

metadata = '--metadata' in params

def scrapeUrl(url, trying = 1):
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
  }
  try:
    r = requests.get(url=URL, headers=headers)
    return r.content
  except requests.exceptions.Timeout:
    # Maybe set up for a retry, or continue in a retry loop
    if trying < 5:
      print('Trying again ' + trying)
      scrapeUrl(url=url, trying=trying + 1)
    else:
      print('Failed: Timeout issue')
      return ''
  except requests.exceptions.TooManyRedirects as e:
    # Tell the user their URL was bad and try a different one
    print(e)
    return ''
  except requests.exceptions.RequestException as e:
    # catastrophic error. bail.
    # raise SystemExit(e)
    print(e)
    return ''

def getEncoding(soup):
  encod = 'utf-8'
  if soup and soup.meta:
    encod = soup.meta.get('charset')
    if encod == None:
      encod = soup.meta.get('content-type')
      if encod == None:
        content = soup.meta.get('content')
        match = re.search('charset=(.*)', content)
        if match:
          encod = match.group(1)
        else:
          encod = 'utf-8'
  else:
    encod = 'utf-8'
  return encod

if len(urls) == 0:
  print('Input the valid urls as params')
else:
  for URL in urls:
    if re.match(regex, URL) is not None:
      content = scrapeUrl(url=URL)
      if content != '':
        now = datetime.now(pytz.utc)
        lastFetched = now.strftime("%Y%m%d-%H%M%S")

        urlObj = urlparse(URL)

        if not os.path.exists('results'):
          os.mkdir('results')

        path1_tmp = os.path.join('results', urlObj.netloc)
        if not os.path.exists(path1_tmp):
          os.mkdir(path1_tmp)

        path2_tmp = os.path.join('results', urlObj.netloc, lastFetched)
        os.mkdir(path2_tmp)

        filename = 'index.html' if urlObj.path == '/' or urlObj.path == '' else urlObj.path[1:] + '.html'

        soup = BeautifulSoup(content, 'html5lib')
        encod = getEncoding(soup)

        imgs = soup.select('img')
        imgUrls = []
        for img in imgs:
          if re.match(regex, img['src']) is not None:
            imgUrls.append(img['src'])
          else:
            imgUrls.append(urlObj.netloc + img['src'])

        aTags = soup.select('a[href]')
        hrefs = []
        for aTag in aTags:
          if re.match(regex, aTag['href']) is not None:
            hrefs.append(aTag['href'])
          else:
            hrefs.append(urlObj.netloc + aTag['href'])

        with open(os.path.join('results', urlObj.netloc, lastFetched, filename), 'wb') as f:
          f.write(content)

        with open(urlObj.netloc + '.html', 'wb') as f:
          f.write(content)
        if metadata:
          print(
            """
  site: """ + urlObj.netloc + """
  num_links: """ + str(len(hrefs)) + """
  images: """ + str(len(imgUrls)) + """
  last_fetch: """ + now.strftime('%a %b %d %Y %H:%M UTC') + """
            """
          )
    else:
      print(URL + ' is invalid url')
