# wordpress-on-lightsail-python-backup

Sample Python code to backup Wordpress running on an AWS Lightsail instance using AWS APIs

## Why do I need this code?

Getting a good backup of Wordpress requires stopping mySQL, PHP, and Apache.  If Wordpress is running on an AWS Lightsail instance this can be combined with a Lightsail instance snapshot to capture the state of the instance with the services stopped.  This Lightsail snapshot can serve as a backup copy in case of corruption of our Wordpress installation or Lightsail instance since we can recreate Lightsail instances from existing instance snapshots.  

For good measure, we also 'tar' the /opt/bitnami directory while the services are stopped and upload this tar file to S3 for safe keeping.  That way we not only have a Lightsail snapshot of our instance with Wordpress services stopped, we also have a tar file of all the Wordpress data (everything resides in /opt/bitnami) in AWS S3.

The AWS CLI is not required but is helpful since it sets up the Python environment and AWS credential keys.  If you do not have the AWS CLI installed, you can still use this code, just make sure you have Boto3 installed via PIP and have your AWS credentials configured locally on your Lightsail instance.  The account defined by the credentials require access to Lightsail and S3.  

## How to use this code

1.  Edit the file and add your AWS Lightsail instance name ('lightsail_instance_name')
2.  Edit the file and add your S3 bucket name ('my_bucket')
3.  Configure your Lightsail image with your AWS credentials so that your script will have access to Lightsail and S3.  The steps can be found with the instructions for add the AWS CLI to your instance.  
4.  This script can co-exist with the AWS CLI but **DO NOT** upgrade pip since that will break the AWS CLI (if you have the AWS CLI installed)
5.  Use /usr/bin/python which is version 2.7 when your instance has the AWS CLI installed.  
6.  To run the file, issue the command 'sudo python wordpress_on_lightsail_python_backup.py'.  
