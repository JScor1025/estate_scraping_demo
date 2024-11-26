from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint
from time import sleep

import requests
url = "https://suumo.jp/chintai/tokyo/sc_shinjuku/?page={}"
target_url = url.format(1)

r = requests.get(target_url)
soup = BeautifulSoup(r.text)

contents = soup.find_all("div", class_="cassetteitem")
content = contents[0]

# 物件・建物情報を格納
detail = content.find("div", class_="cassetteitem-detail")
# 各部屋情報を格納
table = content.find("table", class_="cassetteitem_other")

# 物件名
title = detail.find("div", class_="cassetteitem_content-title").text
# 住所
address = detail.find("li", class_="cassetteitem_detail-col1").text
# アクセス
access = detail.find("li", class_="cassetteitem_detail-col2").text
# 築年数
age = detail.find("li", class_="cassetteitem_detail-col3").text

# trタグを取得
tr_tags = table.find_all("tr", class_="js-cassette_link")
# 最初のtrタグ
tr_tag = tr_tags[0]

# ４つの情報を取得
floor, price, first_fee, capacity = tr_tag.find_all("td")[2:6]

# 賃料と管理費を格納
fee, management_fee = price.find_all("li")
# 敷金と礼金を格納
deposit, gratuity = first_fee.find_all("li")
# 間取りと面積を格納
madori, menseki = capacity.find_all("li")

# 11項目を格納
d = {"title": title,
    "address": address,
    "age": age,
    "floor": floor.text,
    "fee": fee.text,
    "management_fee": management_fee.text,
    "deposit": deposit.text,
    "gratuity": gratuity,
    "moadori": madori.text,
    "menseki": menseki.text
}

# 空のリストを作成
d_list = []

# 全ての物件情報を取得
contents = soup.find_all("div", class_="cassetteitem")
# forループで取得
for content in contents:

    # 物件・建物情報
    detail = content.find("div", class_="cassetteitem-detail")
    # 各部屋情報
    table = content.find("table", class_="cassetteitem_other")

    # 物件名
    title = detail.find("div", class_="cassetteitem_content-title").text
    # 住所
    address = detail.find("li", class_="cassetteitem_detail-col1").text
    # アクセス
    access = detail.find("li", class_="cassetteitem_detail-col2").text
    # 築年数
    age = detail.find("li", class_="cassetteitem_detail-col3").text

    # trタグを取得
    tr_tags = table.find_all("tr", class_="js-cassette_link")
    # forループで取得
    for tr_tag in tr_tags:

        # ４つの情報を取得
        floor, price, first_fee, capacity = tr_tag.find_all("td")[2:6]

        # 賃料と管理費を格納
        fee, management_fee = price.find_all("li")
        # 敷金と礼金を格納
        deposit, gratuity = first_fee.find_all("li")
        # 間取りと面積を格納
        madori, menseki = capacity.find_all("li")

        # 11項目を格納
        d = {"title": title,
            "address": address,
            "age": age,
            "floor": floor.text,
            "fee": fee.text,
            "management_fee": management_fee.text,
            "deposit": deposit.text,
            "gratuity": gratuity,
            "moadori": madori.text,
            "menseki": menseki.text
        }

        # d_listに格納
        d_list.append(d)

# ----複数ページの取得----

url = "https://suumo.jp/chintai/tokyo/sc_shinjuku/?page={}"

d_list = []

for i in range(1,4):
    # print("d_listの大きさ:",len(d_list))

    #1 アクセス先のurlを取得
    target_url = url.format(i)

    sleep(1)

    #2 1で取得したurlにアクセス
    r = requests.get(target_url)

    #3 取得したHTMLを解析
    soup = BeautifulSoup(r.text)

    #4 全ての物件情報を取得
    contents = soup.find_all("div", class_="cassetteitem")
    #5 forループで取得
    for content in contents:

        #6 それぞれを解析
        # 物件・建物情報
        detail = content.find("div", class_="cassetteitem-detail")
        # 各部屋情報
        table = content.find("table", class_="cassetteitem_other")

        # 物件名
        title = detail.find("div", class_="cassetteitem_content-title").text
        # 住所
        address = detail.find("li", class_="cassetteitem_detail-col1").text
        # アクセス
        access = detail.find("li", class_="cassetteitem_detail-col2").text
        # 築年数
        age = detail.find("li", class_="cassetteitem_detail-col3").text

        # trタグを取得
        tr_tags = table.find_all("tr", class_="js-cassette_link")
        # forループで取得
        for tr_tag in tr_tags:

            # ４つの情報を取得
            floor, price, first_fee, capacity = tr_tag.find_all("td")[2:6]

            # 賃料と管理費を格納
            fee, management_fee = price.find_all("li")
            # 敷金と礼金を格納
            deposit, gratuity = first_fee.find_all("li")
            # 間取りと面積を格納
            madori, menseki = capacity.find_all("li")

            # 11項目を格納
            d = {"title": title,
                "address": address,
                "age": age,
                "floor": floor.text,
                "fee": fee.text,
                "management_fee": management_fee.text,
                "deposit": deposit.text,
                "gratuity": gratuity.text,
                "moadori": madori.text,
                "menseki": menseki.text
            }

            # d_listに格納
            d_list.append(d)

# pprint(d_list[:2])

# ----CSVに保存----

# d_listを使って、データフレームを作成
df = pd.DataFrame(d_list)

# データフレームの先頭５行を確認
# print(df.head())

# 物件名の重複を削除して、大きさを確認
# print(df.title.unique())
# print(len(df.title.unique()))

# 表形式の取得結果をCSVに出力
df.to_csv("test.csv", index=None, encoding="utf-8-sig")