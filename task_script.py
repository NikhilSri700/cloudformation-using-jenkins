import sys
import json
import boto3
import botocore

aws_console = boto3.session.Session(aws_access_key_id=sys.argv[1], aws_secret_access_key=sys.argv[2], region_name='ap-south-1')
cfn_client = aws_console.client('cloudformation')


def create_or_update(stackName, VpcCidr, publicSubnetCidr, privateSubnetCidr, email, instanceType):
    template_url = 'https://cf-templates-124lkz1hfo78n-ap-south-1.s3.ap-south-1.amazonaws.com/cfn_task.yaml'
    param = [
        {
            'ParameterKey': 'VpcCIDR',
            'ParameterValue': VpcCidr
        },
        {
            'ParameterKey': 'PublicSubnetCIDR',
            'ParameterValue': publicSubnetCidr
        },
        {
            'ParameterKey': 'PrivateSubnetCIDR',
            'ParameterValue': privateSubnetCidr
        },
        {
            'ParameterKey': 'EmailForEventRule',
            'ParameterValue': email
        },
        {
            'ParameterKey': 'EC2InstanceType',
            'ParameterValue': instanceType
        }
    ]

    try:
        if _stack_exists(stackName):
            print(f'Updating {stackName}')
            response = cfn_client.update_stack(StackName=stackName, TemplateURL=template_url, Parameters=param)
            waiter = cfn_client.get_waiter('stack_update_complete')
        else:
            print(f'Creating {stackName}')
            response = cfn_client.create_stack(StackName=stackName, TemplateURL=template_url, Parameters=param)
            waiter = cfn_client.get_waiter('stack_create_complete')
        print("Waiting for stack to be ready...")
        waiter.wait(StackName=stackName)
    except botocore.exceptions.ClientError as error:
        error_msg = error.response['Error']['Message']
        if error_msg == 'No updates are to be performed.':
            print('No changes')
        else:
            raise
    else:
        print(f"{stackName} is ready.")

def _stack_exists(stackName):
    stacks = cfn_client.list_stacks()['StackSummaries']
    for stack in stacks:
        if stack['StackStatus'] == 'DELETE_COMPLETE':
            continue
        if stackName == stack['StackName']:
            return True
    return False

create_or_update(*sys.argv[3:])
