import boto3
import json
import os
from botocore.exceptions import ClientError

def lambda_handler (event, context):
    # Setting the client for ECR (ecr_client), and for SES (ses_client)
    ecr_client = boto3.client('ecr')
    ses_client = boto3.client('ses')
    

    # Getting information from the event, to use it in the 'describe_image_scan_findings' API request
    accId = event['account']
    image = { "imageDigest": event['detail']["image-digest"], "imageTag": event['detail']["image-tags"][0]}
    repo = event['detail']['repository-name']

    # Initiate the DescribeImageScanFinding request, saving the response as a dictionary
    response = ecr_client.describe_image_scan_findings(
        registryId=accId,
        repositoryName=repo,
        imageId=image,
        maxResults=1000
    )
    
    severities = os.environ['severities']

    # The following loop sending email on each finding, and based on severity
    for i in response['imageScanFindings']['findings']:
        severity = i['severity']

        if severity in severities:
            try:
                finding_name = i['name']
                email_to = os.environ['email_to'] 
                email_from = os.environ['email_from']
                email_subject = 'SECURITY: [{}][{}] ECR Image Scan Finding - {}'.format(repo,severity,finding_name)
                print("Sending Email to {} for the finding {}".format(email_to,finding_name))
                response = ses_client.send_email(
                    Destination={
                        'ToAddresses': [ email_to]
                    },
                    Message={
                        'Body': {
                            'Text': {
                                'Charset': 'UTF-8',
                                'Data': json.dumps(i,indent=4)
                            }
                        },
                        'Subject': {
                            'Charset': 'UTF-8',
                            'Data': email_subject
                        }
                    },
                    Source = email_from
                )                  
                print('Sent email '+ email_subject)
            except ClientError:
                print("Couldn't send email "+ email_subject)
                raise

    print('Scan notification for '+ event['detail']["image-digest"]+':'+event['detail']["image-tags"][0]+ ' is complete.')
