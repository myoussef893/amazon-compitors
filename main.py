from bs4 import BeautifulSoup
import requests
import gspread
from pprint import pprint
w = 'https://www.amazon.eg'
seller_store_front = 'https://www.amazon.eg/s?i=merchant-items&me=A15ZDSUA9CKGMX&page=2&marketplaceID=ARBP9OOSHTCHU&qid=1707914569&ref=sr_pg_'
h = {'User-Agent':'https://explore.whatismybrowser.com/useragents/parse/?analyse-my-user-agent=yes'}

# Where did you stop ? 

# كنت حعمل الجوجل شيت
# و كنت عايز اعمل الباقي بالكلاسز 
#محتاج اعمل السؤال اللي حيحدد الـ pagination

gc = gspread.service_account('bot_creds.json')
sh = gc.open('amazon-scrapped-data by python')
worksheet = sh.worksheet('Sheet1')

link_list=[]

r = requests.get(seller_store_front,headers=h).content
s = BeautifulSoup(r,'html.parser')

with open('index.html','wb') as file: 
    file.write(r)

link_graper = s.find_all('a',class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
linkappender = [link_list.append(w+i.get('href')) for i in link_graper]




def info_finder(tag_,class_): 
    try: 
      result =  s.find(tag_,class_=class_).get_text()
    except: 
        result= None 
    return result


counter = 0

for link in link_list:
    
    print('working on it ')
    r = requests.get(link,headers=h).content
    s = BeautifulSoup(r,'html.parser')

    title = info_finder('span',"a-size-large product-title-word-break")

    price = info_finder('span','a-price-whole')
    # seller_2 = s.find('a',id='sellerProfileTriggerId').get_text()
    image = s.find('img',class_='a-dynamic-image a-stretch-horizontal')
    description = s.find('div' ,id='productDescription').get_text()
    short_description = s.find('ul',class_='a-unordered-list a-vertical a-spacing-mini')
    counter +=1
    product_list = {
        'title':title,
        'price':price,
        'seller': seller_2,
        'short_description':short_description,
        # 'description': description
    }
    print('getting it')
    worksheet.append_row([link,
                          title,
                          price,
                        #   seller_2,
                          description,
                          image])

