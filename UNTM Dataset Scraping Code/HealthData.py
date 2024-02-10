import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from dateutil.parser import parse

links=[]
Date=[]
Titles=[]
Details=[]
Categories=[]
links_count=1
week_days=["جمعرات","اتوار","بدھ","ہفتہ","جمعہ","پیر","منگل"]
monthly_name1=["دسمبر","نومبر","اکتوبر","ستمبر","اگست","جولائی","جون","مئی","اپریل","مارچ","فروری","جنوری"]
monthly_name2=["December","November","October","September","August","July","June","May","April","March","February","January"]
for i in range(1,81):
    print("Scraping Page No:", i)
    result= requests.get('https://www.urdupoint.com/health/news/' + str(i) + '.html')
    soup = bs(result.text, 'lxml')
    for item in soup.find_all("div", class_="news_list_big"):
         for link in item.find_all('a'):
                #print(link.get('href'))
                links.append(link.get('href'))

print(len(links))
for i in links:
    print("URL:", links_count, "\t", i)
    url=requests.get(i)
    s=bs(url.text, "lxml")
    #Category
    category = s.find("ul", class_="bread_crumb_en")
    cat = category.find_all("a")[1].text
    Categories.append(cat)
    #Title
    title = s.find("div", class_="news_article")
    t = title.find("h1").text.strip()
    Titles.append(t)
    # Article
    Article = title.find("div", class_="detail_txt urdu fs17 lh34 aj rtl").text.strip()
    my_string = Article.replace("\n", "")
    Details.append(my_string)
    # Date
    dat = title.p.span
    x=dat.text
    for i in week_days:
        if i in x:
            n = x.replace(i, '')
    # print(n)
    k=0
    for i in monthly_name1:
        if i in n:
            m=n.replace(i, monthly_name2[k])
        k+=1
    # print(m)
    dat_string=(parse(m))
    After_dateFormat =dat_string.strftime('%d-%m-%Y')
    # print(After_dateFormat)
    Date.append(After_dateFormat)
    links_count+=1

# print(Categories)
# print(Titles)
# print(Details)
# print(Date)
df=pd.DataFrame({"Date": Date,"Title": Titles, "News": Details, "Category": Categories, "Link":links})
df.to_csv("UrduNews Dataset.csv", mode='a', index=False, header=False, encoding="utf-8")
