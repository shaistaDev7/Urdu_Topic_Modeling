import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json

links=[]
Date=[]
Titles=[]
Details=[]
Categories=[]
links_count=1
for i in range(1,76):
    print("Scraping Page No:", i)
    result= requests.get('https://www.urdupoint.com/technology/news/' + str(i) + '.html')
    soup = bs(result.text, 'lxml')
    for item in soup.find_all("div", class_="sharp_box_wrap"):
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
    try:
        data = s.find_all("script", type="application/ld+json")[3]
        da = json.loads(str(data.text),strict=False)
        d=(da['headline'])
        Titles.append(d.replace("\r", ""))
    except:
        data=s.find("h2", class_="urdu fs24 lh48 ar rtl txt_blue").text.strip()
        print(data)
        Titles.append(data)

    # Article
    Article = s.find("div", class_="txt_detail urdu ar rtl").text.strip()
    my_string = Article.replace("\n", "")
    Details.append(my_string)
    # Date
    dat = s.find("span", class_="arial").text.strip()
    Date.append(dat)
    links_count+=1

# print(Categories)
# print(Titles)
# print(Details)
# print(Date)
df=pd.DataFrame({"Date": Date,"Title": Titles, "News": Details, "Category": Categories, "Link":links})
df.to_csv("UrduNews Dataset.csv", mode='a', index=False, header=False, encoding="utf-8")
