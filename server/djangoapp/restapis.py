import os
import requests
import json
from dotenv import load_dotenv
# import related models here
from requests.auth import HTTPBasicAuth

from djangoapp.models import CarDealer, DealerReview


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs) -> dict:
    print(kwargs)
    print(f"GET from {url}")
    try:
        # Call get method of requests library with URL and parameters
        if (kwargs.get('api_key') is None):
            
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs,
                                    auth=HTTPBasicAuth('apiKey', kwargs['api_key']))
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print(f"With status {status_code} ")
    json_data: dict = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs) -> dict:
    print(kwargs)
    print(f"POST to {url}")
    
    try:
        # post the payload to the url with the kwargs
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print(f"With status {status_code} ")

    json_data: dict = json.loads(response.text)
    
    print(json_data)

    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs) -> list[CarDealer]:
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    
    # print(json_result)

    if json_result:
        # Get the row list in JSON as dealers
        dealers: list[dict] = json_result["dealerships"]
        # For each dealer object
        for dealer in dealers:
            
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   state=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)
    return results

def get_dealers_from_cf_by_state(url, stateName) -> list[CarDealer]:
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, state=stateName)
    
    # print(json_result)

    if json_result:
        # Get the row list in JSON as dealers
        dealers: list[dict] = json_result["dealerships"]
        # For each dealer object
        for dealer in dealers:
            
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   state=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_id) -> list[DealerReview]:
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealer_id)
    
    # print(json_result)

    if json_result:
        # Get the row list in JSON as dealers
        reviews: list[dict] = json_result["reviews"]
        # For each dealer object
        for review in reviews:
            
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(
                id=review["id"],
                review=review["review"],
                dealership=review["dealership"],
                name=review["name"],
                purchase=review["purchase"],
                purchase_date=review["purchase_date"],
                car_make=review["car_make"],
                car_model=review["car_model"],
                car_year=review["car_year"],
                sentiment=analyze_review_sentiments(review["review"])
            )
            results.append(review_obj)
    return results



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealer_review_text) -> str:
    
    load_dotenv()

    url = os.getenv("IBM_WATSON_NLU_URL") + "/v1/analyze"
    api_key = os.getenv("IBM_WATSON_NLU_API_KEY")

    params = {
        "text" : dealer_review_text,
        "version" : "2022-04-07",
        "features" : "sentiment",
        "return_analyzed_text" : "true",
        "language" : "en"
    }
    try :
        response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        
        print(f"Dealer Review: {dealer_review_text}")
        
        sentiment_score = json.loads(response.text)["sentiment"]["document"]["score"]
        sentiment_label = json.loads(response.text)["sentiment"]["document"]["label"]
        
        status_code = response.status_code
        print(f"NLU With status {status_code} ")
        
        print(f"Sentiment label: {sentiment_label} Sentiment score: {sentiment_score}")

        # print(json.dumps(response.text, indent=2))
        return sentiment_label
    
    except:
        status_code = response.status_code
        print(f"NLU With status {status_code} ")
        print("Network exception occurred")
        print(json.dumps(response.text, indent=2))
        return "unknown"




