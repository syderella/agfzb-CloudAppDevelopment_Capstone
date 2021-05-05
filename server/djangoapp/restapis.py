import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


def get_request(url, api_key=None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        if api_key:
         
            response = requests.get(url, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', api_key), params=kwargs)
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)

    except:
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result["rows"]
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


def get_dealers_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        reviews = json_result["rows"]
        for review in reviews:
            review_doc = review["doc"]
            if review_doc["purchase"]: 
                review_obj = DealerReview(car_model=review_doc["car_model"], car_year=review_doc["car_year"], dealership=review_doc["dealership"],
                                    id=review_doc["id"], name=review_doc["name"], purchase=review_doc["purchase"],
                                    purchase_date=review_doc["purchase_date"],
                                    review=review_doc["review"], car_make=review_doc["car_make"])
            else:
                review_obj = DealerReview(dealership=review_doc["dealership"],
                                    id=review_doc["id"], name=review_doc["name"], purchase=review_doc["purchase"],
                                    review=review_doc["review"], car_model="Not Available", 
                                    car_year="Not Available", purchase_date="Not Available", car_make="Not Available")

            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)


    return results


def analyze_review_sentiments(dealer_review):
    api_key = "32Tk7C3ELJ_XhREGh9pSYRXcigHkO_VBRbNg9W_cpxEN"
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/082e1174-aa72-4f50-9b20-375cdb66c0e5/v1/analyze"
    response = get_request(
        url=url,
        api_key=api_key,
        features="sentiment",
        text= dealer_review ,
        version="2021-03-25"
    )
    return response["sentiment"]["document"]["label"]


def post_request(url, json_payload, **kwargs):
    respond = requests.post(url, params=kwargs, json=json_payload)
    return respond
