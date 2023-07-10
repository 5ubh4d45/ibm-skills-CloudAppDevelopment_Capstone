/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('@ibm-cloud/cloudant');

async function main(params) {
    const authenticator = new IamAuthenticator({apikey: params.IAM_API_KEY});
    const cloudant = CloudantV1.newInstance({authenticator: authenticator});
    
    const DB_NAME = 'dealerships';
    const state = params.state;

    cloudant.setServiceUrl(params.COUCH_URL);

    try {
        let data = null;

        // if (state || state != "") {
        //     data = await cloudant.postFind({
        //         db: DB_NAME,
        //         selector: {state: state}
        //     })
        // } else {
        //     data = await cloudant.postFind({
        //         db: DB_NAME,
        //         selector: {state: state}
        //     });
        // }
        
        data = await cloudant.postFind({
            db: DB_NAME,
            selector: {state: state}
        });
        
        let filteredData = data.result.docs.map((doc) => ({
            id: doc.id,
            city: doc.city,
            state: doc.state,
            st: doc.st,
            address: doc.address,
            zip: doc.zip,
            lat: doc.lat,
            long: doc.long
        }));
        if (filteredData.length < 1) {
            return {statusCode: 404, body: {
                message: "No records found."}};
        }
        return { body: { dealerships: filteredData } }; 
    } catch (error) {
        return { statusCode: 500, body: {error: error}};
    }
}