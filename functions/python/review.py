#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys

from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibmcloudant.cloudant_v1 import CloudantV1

def main(params : dict):
    """Main Function for review handling

    Args:
        dict (Dict): input paramaters
    """

    DB_NAME = "reviews"
    REQ_METHOD = params.get("__ow_method")

    # setup client
    authenticator = IAMAuthenticator(apikey=params.get("IAM_API_KEY"))

    client = CloudantV1(authenticator=authenticator)
    client.set_service_url(service_url=params.get("COUCH_URL"))

    # get reviews by dealership id
    if REQ_METHOD == "get":
        try:
            DEALERSHIP_ID = int(params.get("dealerId"))
        except:
            return {
                "statusCode" : 400,
                "body" : {
                    "mssg" : f"please provide a valid dealership id. Provided: (?dealerId={params.get('dealerId')})"
                }
            }
        
        data : dict = client.post_find(
            db=DB_NAME,
            selector={"dealership" : { "$eq": DEALERSHIP_ID} }
        ).get_result()
        filteredData : dict = data.get("docs")

        if (not filteredData or len(filteredData) == 0):
            print("no reviews")
            return {
                # can't implement 204 NO CONTENT as IBM actions removes the body automatically is 204 is used
                "statusCode" : 400,
                "body" : {
                    "mssg" : f"no reviews on this dealership id: {DEALERSHIP_ID}"
                }
            }

        return {"body": filteredData }
    
    # post new review
    elif REQ_METHOD == "post":
        try:
            review = params.get("review")
        except:
            return {
                "statusCode" : 400,
                "body" : {
                    "mssg" : "no review found in request"
                }
            }
        
        data : dict = client.post_document(
            db=DB_NAME,
            document=review
        ).get_result()
        
        return {"body" : data }

    return {
        "statusCode" : 400,
        "body" : {
            "mssg" : "please use supported request method"
        }
    }
