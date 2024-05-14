from random import randint
import random

import psycopg2
import requests
import json

url = "https://www.citilink.ru/graphql/"

payload = "{\"query\":\"query GetSubcategoryProductsFilter($subcategoryProductsFilterInput:CatalogFilter_ProductsFilterInput!,$categoryFilterInput:Catalog_CategoryFilterInput!,$categoryCompilationFilterInput:Catalog_CategoryCompilationFilterInput!)\\n{productsFilter(\\n    filter:$subcategoryProductsFilterInput)\\n    {record{...SubcategoryProductsFilter}},\\n    category(filter:$categoryFilterInput){...SubcategoryCategoryInfo}}\\n    fragment SubcategoryProductsFilter on CatalogFilter_ProductsFilter{products{...ProductSnippetFull}}\\n    fragment ProductSnippetFull on Catalog_Product{...ProductSnippetShort}\\n    fragment ProductSnippetShort on Catalog_Product{...ProductSnippetBase}\\n    fragment ProductSnippetBase on Catalog_Product{id,name,shortName,slug,images{citilink{...Image}},price{...ProductPrice},category{name},brand{name}}\\n    fragment Image on Image{sources{url}}\\n    fragment ProductPrice on Catalog_ProductPrice{current}\\n    fragment SubcategoryCategoryInfo on Catalog_CategoryResult{... on Catalog_Category{...Category,compilation(filter:$categoryCompilationFilterInput){... on Catalog_CategoryCompilation{name},... on Catalog_CategoryCompilationIncorrectArgumentError{__typename,message},... on Catalog_CategoryCompilationNotFoundError{__typename,message}}},... on Catalog_CategoryIncorrectArgumentError{__typename,message},... on Catalog_CategoryNotFoundError{__typename,message}}\\n    fragment Category on Catalog_Category{slug}\",\"variables\":{\"subcategoryProductsFilterInput\":{\"categorySlug\":\"smartfony\",\"compilationPath\":[],\"pagination\":{\"page\":1,\"perPage\":900},\"conditions\":[],\"sorting\":{\"id\":\"\",\"direction\":\"SORT_DIRECTION_DESC\"},\"popularitySegmentId\":\"THREE\"},\"categoryFilterInput\":{\"slug\":\"smartfony\"},\"categoryCompilationFilterInput\":{\"slug\":\"\"}}}"
headers = {
  'accept': '*/*',
  'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
  'content-type': 'application/json',
  'cookie': '_tuid=b40c0afc0ed12a2687a65766315012d83b0339e5; _space=msk_cl; _city_guessed=1; __exponea_etc__=409da980-4d43-493f-a674-4685989c3d5e; tmr_lvid=cd7917f49485c3a10fe106d69152f685; tmr_lvidTS=1714893030512; _ym_uid=171489303112196563; _ym_d=1714893031; flocktory-uuid=01b65e32-29e9-450c-8717-473235364684-7; advcake_session_id=ac6aaafd-d2c9-648f-ecb9-d982eb84814f; advcake_track_url=https%3A%2F%2Fwww.citilink.ru%2F; advcake_utm_partner=; advcake_utm_webmaster=; advcake_click_id=; adrcid=AtXGB0Fr34gpjdp7p-dUjPw; ab_test=90x10v4%3A1%7Creindexer%3A2%7Cdynamic_yield%3A3%7Cwelcome_mechanics%3A4%7Cdummy%3A20; ab_test_analytics=90x10v4%3A1%7Creindexer%3A2%7Cdynamic_yield%3A3%7Cwelcome_mechanics%3A4%7Cdummy%3A20; _rc_uid=db50d6cb2914c1692b16b86d03d6add7; ab_test_segment=7; _sp_ses.faaa=*; _ym_isad=2; __exponea_time2__=0.11838626861572266; advcake_track_id=17eb93a1-b646-a895-2312-889d77412106; AMP_TOKEN=%24NOT_FOUND; _gid=GA1.2.1626164255.1715591865; _clck=ro53km%7C2%7Cflq%7C0%7C1586; domain_sid=mG4ef_Xd4goenTDWJA61u%3A1715591865139; adrdel=1; _rc_sess=d6f5411f-bbdb-47b0-b343-63a3ef2e2ea3; _clsk=8bf7b4%7C1715591885775%7C3%7C0%7Cv.clarity.ms%2Fcollect; tmr_detect=0%7C1715591889695; _ga_DDRSRL2E1B=GS1.1.1715591864.2.1.1715592074.60.0.0; _dc_gtm_UA-5582449-1=1; _sp_id.faaa=7f631de3-e0b3-476a-b31a-a3dec2053687.1714893031.2.1715592075.1714893087.34b2fd7c-2865-4eb3-b20e-fd79e5d1c6e4.b68e033c-da6c-4f44-a17e-ed12c1b75037.630da8bd-d9a2-40dc-8a9e-d7ec91ef4a6a.1715591864770.44; _ga_DDRSRL2E1B-DG=GS1.1.1715591864.2.1.1715592074.0.0.675230236; _ga=GA1.1.1767515422.1714893030',
  'origin': 'https://www.citilink.ru',
  'priority': 'u=1, i',
  'referer': 'https://www.citilink.ru/catalog/smartfony/',
  'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

response = requests.request("POST", url, headers=headers, data=payload).json()

#Проверка response.status_code=200
#Откат в файл


products = response['data']['productsFilter']['record']['products']
for product in products:
  price = product['price']['current']
  if price == '0' or price == 'None' or price == '' or price == 'none' or price == 0:
    price = '0'
  name = product['name']
  category = product['category']['name']
  brand = product['brand']['name']
  image = product['images']['citilink'][0]['sources'][0]['url']

  #запись в бд

  conn = psycopg2.connect(dbname="postgres", user="postgres", password="Log680968amr", host="127.0.0.1")
  cursor = conn.cursor()

  query = """ CREATE TABLE IF NOT EXISTS citilink(id INTEGER, price INT, name TEXT, category TEXT, brand TEXT, image TEXT) """
  cursor.execute(query)
  # добавляем строку в таблицу
  query1 = """INSERT INTO citilink(price, name, category, brand, image) VALUES (%s, %s, %s, %s, %s)"""
  cursor.execute(query1,((price,name,category,brand,image)))
  # выполняем транзакцию
  conn.commit()
  cursor.close()
  conn.close()








  print(price, name, category, brand, image)

print(len(products))
