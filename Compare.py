import psycopg2

import Citilink_parser
import DNS_parser


def main():
    TitleName = str(input())
    print("Введите название товара:", TitleName)

    conn = psycopg2.connect(dbname="postgres", user="postgres", password="Log680968amr", host="127.0.0.1")
    cursor = conn.cursor()

    query = """ SELECT * FROM DNS WHERE name LIKE '%s'""" % "%{}%".format((TitleName))
    query1 = """ SELECT * FROM citilink WHERE name LIKE '%s'""" % "%{}%".format((TitleName))

    cursor.execute(query)
    result = cursor.fetchall()
    print(result)
    cursor.execute(query1)
    result1 = cursor.fetchall()
    print(result1)
    # выполняем транзакцию
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()