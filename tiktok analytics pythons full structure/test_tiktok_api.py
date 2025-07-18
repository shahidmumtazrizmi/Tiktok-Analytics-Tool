import http.client
import json

API_HOST = "tiktok-shop-api.p.rapidapi.com"
API_KEY = "45cc26173amshe51d82ecf68ea77p162486jsnc02a83530a0a"
PRODUCT_ID = "1729678412356815347"
REGION = "TH"
COUNT = 2
CURSOR = 0
SORT_TYPE = 2

conn = http.client.HTTPSConnection(API_HOST)
headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': API_HOST
}

endpoint = f"/api/shop/product/reviews?productId={PRODUCT_ID}&region={REGION}&count={COUNT}&cursor={CURSOR}&sortType={SORT_TYPE}"
conn.request("GET", endpoint, headers=headers)
res = conn.getresponse()
data = res.read()

try:
    result = json.loads(data.decode("utf-8"))
    with open("api_response.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print("API response written to api_response.json")
except Exception as e:
    print("Error parsing JSON:", e)
    with open("api_response.json", "wb") as f:
        f.write(data)
    print("Raw response written to api_response.json") 