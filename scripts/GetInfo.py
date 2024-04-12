
from bs4 import BeautifulSoup
import requests

url = 'https://support.huaweicloud.com/distributed-devg-v3-gaussdb/gaussdb-12-1217.html'

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

print(soup.body.descendants)
for url in soup.body.descendants:
    if "ulchildlink" in url:
        print(url.content)









