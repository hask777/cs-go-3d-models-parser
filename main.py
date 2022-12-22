# from fake_useragent import UserAgent
import requests
import json

# ua = UserAgent()
# print(ua.random)

def collect_data():
    result = []

    offset = 0
    batch_size = 60
    while True:
        for item in range(offset, offset + batch_size, 60):
            url = f'https://cs.money/1.0/market/sell-orders?limit=60&offset={item}&type=2'
            response = requests.get(url)

            offset += batch_size

            data = response.json()
            items = data.get('items')

            for i in items:
                if i.get('pricing').get('discount') is not None and i.get('pricing').get('discount') < -10:
                    try:
                        full_name = i.get('asset').get('names').get('short')
                    except:
                        full_name = None
                    price = i.get('pricing').get('default')
                    discount = i.get('pricing').get('discount')
                    item_3d = i.get('links').get('3d')
                    

                    result.append(
                        {
                            'full_name':full_name,
                            'price':price,
                            'discount':discount,
                            '3d':item_3d
                        }
                    )

            print(len(items))
        if len(items) < 60:
            break


    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

def main():
    collect_data()

if __name__ == "__main__":
    main()