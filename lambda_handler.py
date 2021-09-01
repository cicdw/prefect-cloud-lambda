import json
import os
import urllib.parse
import urllib.request


print("Loading function")


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    ## prep the data
    create_mutation = """
    mutation($input: create_flow_run_input!){
        create_flow_run(input: $input){
            id
        }
    }
    """
    inputs = dict(flow_id=os.getenv("PREFECT__FLOW_ID"))

    # if you wish to pass information about the triggering event as a parameter,
    # simply add that to the inputs dictionary under the parameters key,
    # whose value should be a dictionary of PARAMETER_NAME -> PARAMETER_VALUE
    # inputs['parameters'] = dict(event=event)

    # if you wish to prevent duplicate runs from being created, you may also
    # provide an idempotency key
    # inputs['idempotency_key'] = event['Records'][0]['eventTime'] # for example

    # if you wish to name your flow run to be informative, you can do that
    # with the flow_run_name input
    # inputs['flow_run_name'] = event['Records'][0]['eventTime'] # for example

    # if you wish to pass a start time other than immediately
    # you can provide an ISO formatted timestamp for when you
    # want this run to begin

    # from datetime import datetime, timedelta

    # actually run the flow in two hours
    # inputs['scheduledStartTime'] = (datetime.utcnow() + timedelta(hours=2)).isoformat()

    variables = dict(input=inputs)
    data = json.dumps(
        dict(query=create_mutation, variables=json.dumps(variables))
    ).encode("utf-8")

    ## prep the request
    req = urllib.request.Request(os.getenv("PREFECT__CLOUD__API"), data=data)
    req.add_header("Content-Type", "application/json")
    req.add_header(
        "Authorization", "Bearer {}".format(os.getenv("PREFECT__CLOUD__API_KEY"))
    )

    ## send the request and return the response
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read().decode())
