import datetime
import requests
import csv


from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def collect_data(city_code="1761"):
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    user_agent = UserAgent()
    
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": user_agent.random,
        "X-Requested-With": "XMLHttpRequest"
    }
    
    cookies = {
        "mg_geo_id": f"{city_code}"
    }
    
    response = requests.get(url="https://magnit.ru/promo/", headers=headers, cookies=cookies) 
    soup = BeautifulSoup(response.text, "lxml")
    city = soup.find("a", class_="header__contacts-link_city").text.strip()
    
    with open(f"{city}_{cur_time}.csv", 'w', encoding="cp1251") as file:
            writer = csv.writer(file, delimiter=";")
            
            writer.writerow(
                (
                    "Продукт", 
                    "Старая цена", 
                    "Новая цена", 
                    "Процент скидки", 
                    "Время проведение акции", 
                )
            )
    
    page = 1
    
    while response:
        data = {
            "page":f'{page}'
        }
        
        response = requests.post(url="https://magnit.ru/promo/", cookies=cookies, headers=headers, data=data)
        soup = BeautifulSoup(response.text, "lxml")
        cards = soup.find_all("a", class_="card-sale_catalogue")

        for card in cards:
            
            try:
                card_title = card.find("div", class_="card-sale__title").text.strip()
                card_discount = card.find("div", class_="card-sale__discount").text.strip()
            except AttributeError:
                continue
            
            card_price_old_integer = card.find("div", class_="label__price_old").find("span", class_="label__price-integer").text.strip()
            card_price_old_decimal = card.find("div", class_="label__price_old").find("span", class_="label__price-decimal").text.strip()
            card_old_price = f"{card_price_old_integer},{card_price_old_decimal}"
            
            card_price_integer = card.find("div", class_="label__price_new").find("span", class_="label__price-integer").text.strip()
            card_price_decimal = card.find("div", class_="label__price_new").find("span", class_="label__price-decimal").text.strip()
            card_price = f'{card_price_integer},{card_price_decimal}'
            
            card_sale_date = card.find("div", class_="card-sale__date").text.strip().replace("\n", " ")
            
            with open(f"{city}_{cur_time}.csv", 'a', encoding="cp1251", errors="ignore") as file:
                writer = csv.writer(file, delimiter=";")
                    
                writer.writerow(
                    (
                        card_title,
                        card_old_price,
                        card_price,
                        card_discount,
                        card_sale_date,
                        page,
                    )
                )
        page += 1
        # if page >= 140:
        #    break
    print(f"Файл {city}_{cur_time}.csv записан")
    
    
def main():
    collect_data()
    

if __name__ == "__main__":
    main()
    