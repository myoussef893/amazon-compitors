from bs4 import BeautifulSoup
import requests
import gspread
from datetime import datetime


def info_finder(tag_,class_): 
  """a quicker method to try finding an element and get it's text, and override with None Value incase element not found"""
  try: 
    result =  s.find(tag_,class_=class_).get_text()
  except: 
    result= None 
  return result



w = 'https://www.amazon.eg' # Website name
h = {'User-Agent':'https://explore.whatismybrowser.com/useragents/parse/?analyse-my-user-agent=yes'}

# google sheets configuration
gc = gspread.service_account('bot_creds.json')
sh = gc.open('amazon-scrapped-data by python')

# Google Worksheets (products, sellers)
worksheet = sh.worksheet('Sheet3')
sellers = sh.worksheet('sellers')

# Queried records of the seller sheet.
sellers_records = sellers.get_all_values()[1::]
print(sellers_records)

# Links of products. 
link_list=[]


# Looping into all the seller front urls that was added in the sheet, getting the products urls that will be scrapped. 
for row in sellers_records: 
    print('Loading:Sellers Storefronts...')
    seller_store_front= row[0]
    store_pages = row[1]
    for page_number in range(int(store_pages)):
        main_page = seller_store_front+str(page_number)
        r = requests.get(main_page,headers=h).content
        s = BeautifulSoup(r,'html.parser')
        link_graper = s.find_all('a',class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
        linkappender = [link_list.append(w+i.get('href')) for i in link_graper]




counter = 0 # a counter that was created just to log what the code is doing when in the CDL

for link in link_list:
    
    print(f'working on product url :{counter} ')
    r = requests.get(link,headers=h).content
    s = BeautifulSoup(r,'html.parser')

    title = info_finder('span',"a-size-large product-title-word-break")

    price = info_finder('span','a-price-whole').replace('.\u200e','')
    
    # print(price.split())
    
    seller_2 = s.find('a',id='sellerProfileTriggerId').get_text()
    
    image = s.find('div',class_='imgTagWrapper').find_next('img')['src'].replace('AC_SY300_SX300','AC_SY900_SX900')# fetch the image src and make it bigger by changing the dimensions. 

    description = s.find('div' ,id='productDescription').get_text()

    short_description = s.find('div',id='featurebullets_feature_div').find('ul',class_='a-unordered-list a-vertical a-spacing-mini')
    
    counter +=1 # a counter to get how many products have been scrapped. 
    
    print(f'getting link number:{counter}')
    
    worksheet.append_row([
                          str(datetime.now().today()),
                          link,
                          title,
                          image,
                          int(price),
                          seller_2,
                          description,
                          str(short_description)
                          ])
    

print(f'Python finished scrapping {len(link_list)} products')