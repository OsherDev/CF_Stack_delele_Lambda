import json, boto3


def lambda_handler(event, context):
    print(json.dumps(event))
    ## Get the function name that was deleted....
    DeletedFunction = event['detail']['requestParameters']['functionName']

    ## declare cfn boto3 client
    client = boto3.client('cloudformation')

    ## list all stacks
    response = client.list_stacks(StackStatusFilter=['CREATE_COMPLETE'])

    ## iterate through stacks
    for stackid in response['StackSummaries']:
        print("Stack name is: "+stackid['StackName'])

        ## list all resources in the current stack
        stackresource = client.list_stack_resources(StackName=stackid['StackName'])
        print("Total resources in this stack: "+str(len(stackresource['StackResourceSummaries'])))

        ## iterate through the resources and find only those resources whose resource type is AWS::Lambda::Function
        resource = 0
        while resource < len(stackresource['StackResourceSummaries']):

            if 'AWS::Lambda::Function' in stackresource['StackResourceSummaries'][resource]['ResourceType']:

                ## store the function name in variable
                FunctionName = stackresource['StackResourceSummaries'][resource]['PhysicalResourceId']

                ## check if the function name under the stack is same as that of the Lambda event
                if FunctionName == DeletedFunction:
                    print("Stack to delete: "+stackid['StackName'])
                    print("Function found: "+FunctionName+ " and Deleted function is: "+DeletedFunction)

                    ## delete stack and print response
                    response = client.delete_stack(StackName=stackid['StackName'])
                    print(json.dumps(response))

            resource += 1
