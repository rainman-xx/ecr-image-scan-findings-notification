# Sending email notification of the image scan findings from Amazon ECR in CloudWatch using an AWS Lambda function

Steps to create the solution:

1. Download the [Template-ECR-SFN.yml](Template-ECR-SFN.yml) template.
2. Edit the file and et the following variables
```yaml
          email_to: "to@email.com"
          email_from: "noreply@email.com"
          severities: "MEDIUM HIGH CRITICAL"
```
Alternatively, once uploaded (step #3 below) variables can be changed in AWS Lambda console (UI)

3. Upload the template to CloudFormation and create a new stack.
4. Test the solution by scanning an image on ECR. Then, check the email from the AWS SNS.
5. Feel free to modify the Lambda function code within the template and/or create the resources manually.
