import codecs
from datetime import datetime
import json
import requests
from string import split
import MySQLdb

my_api_key = 'your_api_key'

date_time = datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S')

# Maximum number of calls allowed per day
MAX_CALLS = 50000

response = requests.get('http://api.walmartlabs.com/v1/feeds/items?apiKey=' + my_api_key + '&categoryId=4044_90548_90791')

if response.status_code != 200:
    print '%s' % (response.status_code)

try:
    products_dict = response.json()
    #print json.dumps(products_dict, indent=4)
except:
    pass

all_products = []
unique_upcs = {}

for key in products_dict:
    for index in range(len(products_dict[key])):
        record = [ ]
        if products_dict[key][index]["categoryPath"] == "Home/Appliances/Refrigerators and Freezers":
            name = products_dict[key][index]["name"]
            name_list = name.split()
            if "Refrigerator" in name_list or "refrigerator" in name_list:
                if 'upc' in products_dict[key][index]:
                    record.append(products_dict[key][index]['upc'])
                else:
                    record.append('')

                if 'modelNumber' in products_dict[key][index]:
                    record.append(products_dict[key][index]['modelNumber'])
                else:
                    record.append('')

                if 'msrp' in products_dict[key][index]:
                    record.append(str('%.2f' % float(products_dict[key][index]['msrp'])))
                else:
                    record.append(0.00)

                if 'salePrice' in products_dict[key][index]:
                    record.append(str('%.2f' % float(products_dict[key][index]['salePrice'])))
                else:
                    record.append(0.00)

                if 'customerRating' in products_dict[key][index]:
                    record.append(products_dict[key][index]['customerRating'])
                else:
                    record.append('')

                if 'numReviews' in products_dict[key][index]:
                    record.append(str(products_dict[key][index]['numReviews']))
                else:
                    record.append('')

                record.append('Walmart')

                if 'categoryPath' in products_dict[key][index]:
                    record.append(products_dict[key][index]['categoryPath'].split('/')[-1])
                else:
                    record.append('')

                if 'itemId' in products_dict[key][index]:
                    record.append(str(products_dict[key][index]['itemId']))
                else:
                    record.append('')

                if 'brandName' in products_dict[key][index]:
                    record.append(products_dict[key][index]['brandName'])
                else:
                    record.append('')

                if 'color' in products_dict[key][index]:
                    record.append(products_dict[key][index]['color'])
                else:
                    record.append('')

                if 'name' in products_dict[key][index]:
                    record.append(products_dict[key][index]['name'])
                else:
                    record.append('')

                if 'productUrl' in products_dict[key][index]:
                    record.append(products_dict[key][index]['productUrl'])
                else:
                    record.append('')

                if 'thumbnailImage' in products_dict[key][index]:
                    record.append(products_dict[key][index]['thumbnailImage'])
                else:
                    record.append('')

                if 'mediumImage' in products_dict[key][index]:
                    record.append(products_dict[key][index]['mediumImage'])
                else:
                    record.append('')

                if 'largeImage' in products_dict[key][index]:
                    record.append(products_dict[key][index]['largeImage'])
                else:
                    record.append('')

                if 'longDescription' in products_dict[key][index]:
                    record.append(products_dict[key][index]['longDescription'].encode('ascii', 'ignore'))
                else:
                    record.append('')

                record.append(date_time)

                if (record[0] not in unique_upcs.keys() and record[0] != '') and (record[2] != '0.00' or record[2] != '') and (record[3] != '0.00' or record[3] != ''):
                    all_products.append(record)
                    unique_upcs[record[0]] = 1


connection = MySQLdb.connect(host='localhost', port=3306, db='products_poc', user='your_username', passwd='your_password', use_unicode=True, charset="utf8")
c = connection.cursor()

for row in all_products:
    print row
    c.execute("""INSERT INTO products (upc, model_number, regular_price, sale_price, review_score, review_count, retailer,
                 department, sku, brand, color, name, url, image_small, image_medium, image_large, long_description, date_time)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", row)
connection.commit()