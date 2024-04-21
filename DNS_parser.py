import pickle
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, Side
from tqdm import tqdm
from random import randint
from datetime import datetime
from time import sleep as pause
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import sqlite3
import logging
import psycopg2


def parse_characteristics_page(driver, url):
    """ Парсит страницу товара по ссылке."""
    global category
    driver.get(url)
    pause(randint(7, 11))
    soup = BeautifulSoup(driver.page_source, 'lxml')
    # print(soup.prettify())

    name = soup.find('div', class_="product-card-description__title")
    price = soup.find('div', class_="product-buy__price")
    desc = soup.find('div', class_="product-card-description-text")
    avail = soup.find('a', class_="order-avail-wrap__link ui-link ui-link_blue")
    charcs = soup.find_all('div', class_="product-characteristics__spec-title")
    cvalue = soup.find_all('div', class_="product-characteristics__spec-value")
    main_picture = soup.find('img', class_="product-images-slider__main-img")
    pictures_soup = soup.find_all('img', class_="product-images-slider__img loaded tns-complete")

    pictures_list = []
    for i in pictures_soup:
        _ = pictures_list.append(i.get('data-src'))
        if _ is not None:
            pictures_list.append(_)

    span_tags = soup.find_all('span')
    for i in span_tags:
        if bool(str(i).find('data-go-back-catalog') != -1):
            category = i

    tech_spec = {}
    for f1, f2 in zip(charcs, cvalue):
        tech_spec[f1.text.rstrip().lstrip()] = f2.text.rstrip().lstrip()

    notebook = {}

    notebook["Категория"] = category.text.lstrip(': ')
    notebook["Наименование"] = name.text[15:]
    notebook["Цена"] = int(price.text.replace(' ', '')[:-1])
    notebook["Доступность"] = avail.text if avail is not None else 'Товара нет в наличии'
    notebook["Ссылка на товар"] = url
    notebook["Описание"] = desc.text
    notebook["Главное изображение"] = main_picture.get('src') if main_picture is not None else 'У товара нет картинок'
    notebook["Лист с картинками"] = pictures_list
    notebook["Характеристики"] = list(tech_spec.items())

    # for i, j in notebook.items():
    #     print(i, j)
    return notebook


def get_all_category_page_urls(driver, url_to_parse):
    """ Получаем URL категории и парсим ссылки с неё."""
    global number_of_pages
    page = 1
    url = url_to_parse.format(page=page)
    driver.get(url=url)
    pause(10)

    soup = BeautifulSoup(driver.page_source, 'lxml')

    span_tags = soup.find_all('span')
    for i in span_tags:
        if bool(str(i).find('data-role="items-count"') != -1):
            number_of_pages = [int(x) for x in str(i) if x.isdigit()]

    res = int(''.join(map(str, number_of_pages)))
    pages_total = ((res // 18) + 1)
    logging.warning(f'Всего в категории {pages_total} страницы')

    urls = []

    while True:
        page_urls = get_urls_from_page(driver)
        urls += page_urls

        if page >= pages_total:
            break

        page += 1
        url = url_to_parse.format(page=page)
        driver.get(url)
        pause(randint(6, 9))

    return urls


def get_urls_from_page(driver):
    """ Собирает все ссылки на текущей странице. """
    soup = BeautifulSoup(driver.page_source, 'lxml')
    elements = soup.find_all('a', class_="catalog-product__name ui-link ui-link_black")
    return list(map(
        lambda element: 'https://www.dns-shop.ru' + element.get("href") + 'characteristics/',
        elements
    ))


def to_db(data, driver, file_name="db"):
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # print(soup.prettify())

    name = soup.find('div', class_="product-card-description__title")
    price = soup.find('div', class_="product-buy__price")

    id = 100
    id += 1

    notebook = {}

    notebook["Категория"] = category.text.lstrip(': ')
    notebook["Наименование"] = name.text[15:]
    notebook["Цена"] = int(price.text.replace(' ', '')[:-1])



    conn = psycopg2.connect(dbname="postgres", user="postgres", password="Log680968amr", host="127.0.0.1")
    cursor = conn.cursor()

    query = """ CREATE TABLE IF NOT EXISTS DNS(id INTEGER, price INT, name TEXT, category TEXT) """
    cursor.execute(query)
    # добавляем строку в таблицу people
    query1 = """INSERT INTO DNS(price, name, category) VALUES (%s, %s, %s)"""
    cursor.execute(query1,
                    ((int(price.text.replace(' ', '')[:-1])), str(name.text[15:]), str(category.text.lstrip(': '))))
    # выполняем транзакцию
    conn.commit()
    print("Данные добавлены")

    cursor.close()
    conn.close()


def main():
    driver = uc.Chrome()
    urls_to_parse = [
        'https://www.dns-shop.ru/catalog/17a9db2916404e77/ofisnye-prilozheniya/?p={page}',
    ]

    urls = []
    for index, url in enumerate(urls_to_parse):
        logging.warning(f'Получение списка всех ссылок из {index + 1} категории:')
        parsed_url = get_all_category_page_urls(driver, url)
        urls.append(parsed_url)

    logging.warning("Запись всех ссылок в файл url.txt:")
    with open('urls.txt', 'w') as file:
        for url in urls:
            for link in url:
                file.write(link + "\n")

    with open('urls.txt', 'r') as file:
        urls = list(map(lambda line: line.strip(), file.readlines()))
        logging.warning(urls)
        for url in tqdm(urls, ncols=70, unit='товаров',
                        colour='blue', file=sys.stdout):
            to_db(parse_characteristics_page(driver, url), driver)


if __name__ == '__main__':
    main()
    logging.warning('=' * 20)
    logging.warning('А когда не делали да же!')
