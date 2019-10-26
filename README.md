# prefect-cloud-lambda

A template for an AWS Lambda function that triggers Prefect Flow Runs.

## Instructions for use

This function requires three environment variables:
- `PREFECT__FLOW_ID`: a string UUID of the flow you wish to create a run for
- `PREFECT__CLOUD__API`: the URL of the Cloud API; most likely you'll want to use `"https://api.prefect.io/"`
- `PREFECT__CLOUD__AUTH_TOKEN`: an API token which has appropriate permissions to create flow runs

## Optional enhancements

As written, this lambda function simply triggers a flow run.  There are a few ways you can enhance this:

- configure your Flow to respond to information about the triggering event through a Prefect Parameter
- configure your Lambda function to pass an `idempotencyKey` to ensure duplicate runs aren't created
- configure your Flow to run at some time in the future instead of immediately
