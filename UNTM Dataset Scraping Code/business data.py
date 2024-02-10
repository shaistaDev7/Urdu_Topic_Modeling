import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


links=[]
Date=[]
Titles=[]
Details=[]
Categories=[]
links_count=1
for i in range(1,81):
    print("Scraping Page No:", i)
    result= requests.get('https://www.urdupoint.com/business/news/' + str(i) + '.html')
    soup = bs(result.text, 'lxml')
    for item in soup.find_all("li", class_="item_shadow"):
         for link in item.find_all('a'):
                #print(link.get('href'))
                links.append(link.get('href'))
         for date in item.a.p.span:
                #print(date.text)
                Date.append(date.text)
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
    title = s.find("div", class_="main_bar fl")
    try:
        t = title.find("h1").text.strip()
        Titles.append(t)
    except:
        t = title.find("h2").text.strip()
        t= t.replace("\n", "")
        Titles.append(t)

    # Article
    Article = title.find("span", class_="fs17 mr10 aj rtl db urdu lh40").text.strip()
    my_string = Article.replace("\n", "")
    Details.append(my_string)
    links_count+=1
# print(Categories)
# print((Titles))
# print((Details))
#print((Date))
df=pd.DataFrame({"Date": Date,"Title": Titles, "News": Details, "Category": Categories, "Link":links})
df.to_csv("UrduNews Dataset.csv", mode='a', index=False, header=False, encoding="utf-8")