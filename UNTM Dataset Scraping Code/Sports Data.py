import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
s=Service("D:/MSCS data/web scraping/chromedriver.exe")
driver=webdriver.Chrome(service=s)
driver.get("https://www.urdupoint.com/sports/news.html")
count = 1
max_click_SHOW_MORE = 83
while count<=max_click_SHOW_MORE:
   try:
        loadMoreButton = driver.find_element_by_xpath("""/html/body/div[2]/div[10]/div[1]/div[9]/span""")
        time.sleep(2)
        loadMoreButton.click()
        time.sleep(10)
        print("Button clicked #", count)
        count += 1
   except Exception as e:
           print(e)
           break

print("Complete Job to click on load more button")
time.sleep(20)
links=[]
Date=[]
Titles=[]
Details=[]
Categories=[]
ch='-'
links_count=1
soap = bs(driver.page_source, 'lxml')
for item in soap.find_all("div", class_="news_list_big"):
    for link in item.find_all('a'):
            #print(link.get('href'))
            links.append(link.get('href'))
print(len(links))
for i in links:
    print("URL:",links_count,"\t", i)
    r=requests.get(i)
    s=bs(r.text, "lxml")
    #Category
    category = s.find("ul", class_="bread_crumb_en")
    cat = category.find_all("a")[1].text
    Categories.append(cat)
    #Title
    title = s.find("div", class_="news_article")
    t = title.find("h1").text.strip()
    Titles.append(t)
    # News
    Article = title.find("div", class_="detail_txt urdu fs17 lh34 aj rtl").text.strip()
    Article_val = Article.replace("\n", "")
    Details.append(Article_val)
    # Date
    dat = s.find("span", class_="arial fs13").text
    dat = dat.split(ch, 1)[0]
    Date.append(dat)
    links_count+=1

df=pd.DataFrame({"Date": Date,"Title": Titles, "News": Details, "Category": Categories, "Link":links})
df.to_csv("UrduNews.csv", encoding="utf-8")
driver.quit()