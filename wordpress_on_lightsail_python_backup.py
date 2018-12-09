import os
import boto3
import datetime
import time
import tarfile

def stop_wordpress(client_stop):
        #Function to stop all three Wordpress services using the Bitnami
        #script 'ctlscript'.  We cannot get a good backup of Wordpress
        #(mySQL, PHP, Apache) without stopping the services

        print("Stopping Wordpress")
        client_stop = os.system("sudo /opt/bitnami/ctlscript.sh stop")
	print("Wordpress is stopped")
        return (client_stop)

def start_wordpress(client_start):
        #Function to start all three Wordpress services using the Bitnami
        #script 'ctlscript'  We will start the services up when we complete
        #the Lightsail snapshot

        print("Starting Wordpress")
        client_start = os.system("sudo /opt/bitnami/ctlscript.sh start")
	print("Wordpress is started")
        return (client_start)

def create_instance_snapshot(client, snapshot_name, instance_name):
        #Boto3 'lightsail' client function to take an instance snapshot of
        #a Lightsail instance.  This will only snapshot the instance, if there
        #are additional disks attached then a disk snapshot is required.  This
        #function waits for the snapshot to complete before returning a response.
        #A snapshot is complete when the "status" is "available".

        print("Creating Lightsail snapshot, will wait until completed")
        response = client.create_instance_snapshot(
                instanceSnapshotName=snapshot_name,
                instanceName=instance_name
        )

        client.get_instance_snapshots()
        snapshot_id = client.get_instance_snapshot(instanceSnapshotName=snapshot_name)
        while snapshot_id['instanceSnapshot']['state'] != 'available' :
                print ("Waiting to complete snapshot")
                time.sleep(60)
                snapshot_id = client.get_instance_snapshot(instanceSnapshotName=snapshot_name)

        return(response)

def make_bitnami_tar(output_file, input_dir):
        #Function to tar all of the /opt/bitnami directory into a single tar file
        #with the current date and time stamp as the name.  Bitnami documentation
        #says to tar the entire directory for a backup.
	
	print("Dumping /opt/bitnami to tar file")
        with tarfile.open(output_file, mode='w') as tar:
                response = tar.add(input_dir, arcname=os.path.basename(input_dir))
        print("Tar file completed")
        return(response)

def upload_to_s3(client,bucket,tar,out):
        #Function to take our tar file from the make_bitnami_tar function and upload
        #it to an S3 bucket.  

        print("Uploading tar file to S3")
        response = client.Bucket(bucket).upload_file(tar,out)
	print("Upload completed")

        return(response)

#Main body of the code defines our Boto3 clients and defines our Lightsail instance name.
#The date and time are combined into a string (with no spaces or colons) to use for our 
#snapshot name (must be unique).  We set the output for our tar file along with the input
#directory of our /opt/bitnammi installation.  An S3 bucket name is also defined.
#Add your individual Lightsail instance name and S3 bucket to the code before running.    

wordpress_client=('os.system')
lightsail_client=boto3.client('lightsail')
s3_client=boto3.resource('s3')
lightsail_instance_name="<insert_your_lightsail_instance_name>"
now=str(datetime.datetime.now())
now = now.replace(":","_")
now = now.replace(" ","")
lightsail_instance_snapshot_name = now
output = "/home/bitnami/backup/" + now + ".tar"
input = "/opt/bitnami"
my_bucket='<insert_your_S3_bucket_name>'
tar_file = output
dump_file = now

(stop) = stop_wordpress(wordpress_client)
(tar) = make_bitnami_tar(output,input)
(snap) = create_instance_snapshot(lightsail_client, lightsail_instance_snapshot_name, lightsail_instance_name)
(start) = start_wordpress(wordpress_client)
(upload) = upload_to_s3(s3_client,my_bucket,tar_file,dump_file)
