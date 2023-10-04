from datetime import datetime, timedelta
from urllib import request
import requests
import json
import time
import logging
# pip install -r requirements.txt

def update_auth():
    burp0_url = "https://api.business.kazanexpress.ru:443/api/oauth/token"
    burp0_headers = {
        "Sec-Ch-Ua": "\"(Not(A:Brand\";v=\"8\", \"Chromium\";v=\"99\"",
        "Accept": "application/json", 
        "Content-Type": "application/x-www-form-urlencoded", 
        "Authorization": "Basic a2F6YW5leHByZXNzOnNlY3JldEtleQ==", 
        "Sec-Ch-Ua-Mobile": "?0", 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36", 
        "Sec-Ch-Ua-Platform": "\"Windows\"", 
        "Origin": "https://business.kazanexpress.ru", 
        "Sec-Fetch-Site": "same-site", 
        "Sec-Fetch-Mode": "cors", 
        "Sec-Fetch-Dest": "empty", 
        "Referer": "https://business.kazanexpress.ru/", 
        "Accept-Encoding": "gzip, deflate", 
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
        }
    burp0_data = {"grant_type": "password", "username": login_ke, "password": password_ke}
    response = requests.post(burp0_url, headers=burp0_headers, data=burp0_data)
    print(burp0_headers)
    # print(response.text)
    auth_tokens = json.loads(response.text)
    return auth_tokens["access_token"]


def set_timeslots(shopid, invoices, timeslot):
    post_data="""{"invoiceIds":invoices_change,"timeFrom": time_to_set}"""
    post_data = post_data.replace("invoices_change", str(invoices))
    post_data = post_data.replace("time_to_set",str(timeslot))
    url_toset= f"https://api.business.kazanexpress.ru/api/seller/shop/{shopid}/v2/invoice/time-slot/set"
    
    response = requests.post(url_toset,headers=auth_headers,data=post_data)
    print(response.text)

def find_timeslots(shopid, invoices):
    url = f"https://api.business.kazanexpress.ru/api/seller/shop/{shopid}/v2/invoice/time-slot/get"
    time_now = datetime.now() + timedelta(days=1, hours=1)
    milliseconds = int(round(time_now.timestamp() * 1000))
    timeslots = []
    post_data = """{"invoiceIds":invoices_change,"timeFrom":"_timestamp_"}"""
    post_data = post_data.replace("invoices_change", str(invoices))
    post_data = post_data.replace("_timestamp_", str(milliseconds))
    try:
        response = requests.post(url,headers=auth_headers,data=post_data)
        response.raise_for_status()
        timestamps_list = json.loads(response.text)
        try:
            timeslots = timestamps_list["payload"]["timeSlots"]
        except:
            timeslots = []
        print(timeslots)
    except requests.exceptions.HTTPError as e:
        print(" ERROR ".center(80, "-"))
        print(e)
        print(response.text)
        if response.status_code == 503:
            time.sleep(3)
        if response.status_code == 500 or response.status_code == 401:
            auth_headers["Authorization"] = "Bearer " + update_auth()
            time.sleep(1)
            return []
    except requests.exceptions.RequestException as e:
        print(e)

    return(timeslots)

def market(timeslots, shop, shop_invoices, fo):
    time.sleep(1) 
    timeslots_shop = find_timeslots(shop,shop_invoices)
    if timeslots_shop!=[]:
        timeslots=timeslots_shop[0]["timeFrom"]
        set_timeslots(shop,shop_invoices, timeslots)
        fo.write( shop," \n DONE \n")

def main():
    timeslots_1 = []
    timeslots_2 = []
    timeslots_3 = []
    fo = open("log.txt", "w+")
    for i in range(1,10000):
        time.sleep(3) 
        timeslots_shop1 = find_timeslots(shop_1,shop_1_invoices)
        if timeslots_shop1!=[]:
            timeslots_1=timeslots_shop1[0]["timeFrom"]
            set_timeslots(shop_1,shop_1_invoices, timeslots_1)
            fo.write( " \n DONE1 \n")
        time.sleep(2) 
        timeslots_shop2 = find_timeslots(shop_2,shop_2_invoices)
        if timeslots_shop2!=[]:
            timeslots_2=timeslots_shop2[0]["timeFrom"]
            set_timeslots(shop_2,shop_2_invoices, timeslots_2)
            fo.write(" \n DONE2 \n")
        # time.sleep(1) 
        # timeslots_shop3 = find_timeslots(shop_3,shop_3_invoices)
        # if timeslots_shop3!=[]:
        #     timeslots_3=timeslots_shop3[0]["timeFrom"]
        #     set_timeslots(shop_3,shop_3_invoices, timeslots_3)
        #     fo.write(" \n DONE3 \n")

        fo.write(str(timeslots_1) + str(timeslots_2))# + str(timeslots_3))
        fo.flush()
        if timeslots_1 and timeslots_2:# and timeslots_3:
            break
    fo.close()

shop_1 = 55482 # JWL
shop_1_invoices =  [3856662]

shop_2 = 55482 # MGK
shop_2_invoices = [3856660]

shop_3 = 55482 # PVS
shop_3_invoices = [3856659, 3856665]



login_ke = "" 
password_ke = ""
auth_headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
"Accept": "application/json",
"Accept-Language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7",
"Content-Type": "application/json",
"Authorization": "Bearer KZJ-GjzyR6Ei8E48z2fyGP4-Rzo",
"Content-Length": "49",
"Origin": "https://business.kazanexpress.ru",
"Connection": "keep-alive",
"Referer": "https://business.kazanexpress.ru/",
"Sec-Fetch-Dest": "empty",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Site": "same-site",
"Host": "api.business.kazanexpress.ru"}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
    