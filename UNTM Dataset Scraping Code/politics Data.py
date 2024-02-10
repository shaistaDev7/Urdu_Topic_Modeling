import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from datetime import datetime
import re


links=[]
Date=[]
Titles=[]
Details=[]
Categories=[]
links_count=1
base_url="https://www.siasat.pk"
for i in range(1,56):
    print("Scraping Page No:", i)
    result= requests.get('https://www.siasat.pk/forums/%D8%B3%DB%8C%D8%A7%D8%B3%DB%8C.73/page-' + str(i))
    soup = bs(result.text, 'lxml')
    for item in soup.find_all("h2", class_="articlePreview-title"):
         for link in item.find_all('a'):
                #print(base_url+link.get('href'))
                links.append(base_url+link.get('href'))

print(len(links))
for i in links:
    print("URL:", links_count, "\t", i)
    url=requests.get(i)
    s=bs(url.text, "lxml")
    #Category
    category = s.find("ul", class_="p-breadcrumbs")
    cat = category.find_all("a")[3].text.strip()
    t1 = cat.replace("سیاسی", "Politics")
    Categories.append(t1)
    #Title
    title = s.find("div", class_="p-title")
    t = title.find("h1").text.strip()
    Titles.append(t)
    # Article
    AR=s.find("div",class_="bbWrapper")
    try:
            Article = AR.find("span").text.strip()
            my_string = Article.replace("\n", "")
            result = re.sub(r"http\S+", "", my_string)
            print(result)
            Details.append(result)
    except:
            Article1=AR.text.strip()
            my_string1 = Article1.replace("\n", "")
            result = re.sub(r"http\S+", "", my_string1)
            print(result)
            Details.append(result)
    # Date
    dat = s.find("time", class_="u-dt")
    Before_dateFormat=(dat["data-date-string"])
    After_dateFormat=datetime.strptime(Before_dateFormat, '%b %d, %Y').strftime('%d-%m-%Y')
    Date.append(After_dateFormat)
    links_count+=1

# print(Categories)
# print(Titles)
# print(Details)
# print(Date)
df=pd.DataFrame({"Date": Date,"Title": Titles, "News": Details, "Category": Categories, "Link":links})
df.to_csv("UrduNews.csv", mode='a', index=False, header=False, encoding="utf-8")
