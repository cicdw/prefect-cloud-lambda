import json
import os
import urllib.parse
import urllib.request


print("Loading function")


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    ## Get the object from the event and show its content type
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )

    ## prep the data
    create_mutation = """
    mutation($input: createFlowRunInput!){
        createFlowRun(input: $input){
            flow_run{id}
        }
    }
    """
    inputs = dict(input=dict(flowId=os.getenv("PREFECT__FLOW_ID")))
    data = json.dumps(dict(query=create_mutation, variables=json.dumps(inputs))).encode(
        "utf-8"
    )

    ## prep the request
    req = urllib.request.Request(os.getenv("PREFECT__CLOUD__API"), data=data)
    req.add_header("Content-Type", "application/json")
    req.add_header(
        "Authorization", "Bearer {}".format(os.getenv("PREFECT__CLOUD__AUTH_TOKEN"))
    )

    ## send the request and return the response
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read().decode())
