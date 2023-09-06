   import boto3 
   import pandas as pd
   from io import BytesIO   
   import email   
   from botocore.exceptions import ClientError
   from email.mime.multipart import MIMEMultipart
   from email.mime.text import MIMEText
   from email.mime.application import MIMEApplication

   def lambda_handler(event, context):
       client_sns = boto3.client('sns')
       message = "" 
       client = boto3.client('ec2') 
       id = boto3.client('sts').get_caller_identity().get('Account')   
    
        #  ------------------------lists for storing the info of ec2 and rds---------------------------------
    
       Tab_message = ""
       S_no = []
       Account_ID = []
       Account_Name = []
       Service = []
       Instance_ID = []
       Instance_Name = []  
       Instance_Size = []
       Region = []
       Status = []
       ids = []
       s_no=0
    
          S_no.append("S No.")
          Account_ID.append("Account ID")
          Account_Name.append("Account Name")
          Service.append("Service")
          Instance_ID.append("Service ID")
          Instance_Name.append("Service Name")   
          Instance_Size.append("Service Size")
          Region.append("Region")
          Status.append("Status")
    
        #  ------------------------------EC2-----------------------------------------------------------------
    
       ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    
       for region in ec2_regions:   
           ec2 = boto3.resource('ec2',region_name=region)    
           instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
           RunningInstances = [instance.id for instance in instances]
          
           if len(RunningInstances) > 0:         
               for each in range(len(RunningInstances)):
                   ec2_client = boto3.client('ec2',region_name=region)
                   ec2_resp = ec2_client.describe_instances(InstanceIds=RunningInstances)
                   for resp in ec2_resp['Reservations']:   
                       for each in resp['Instances']:
                           Account_Name.append("Devops")
                           Account_ID.append(id)
                           s_no = s_no+1
                           message += "EC2" + "\n"      
                           message += "Instance Id : " + each['InstanceId'] + "\n" 
                           message += "Region Name : " + each['Placement']['AvailabilityZone'] + "\n"
                           for t in each['Tags']:
                               if t['Key'] == 'Name':   
                                   message += "Name : " + t['Value'] + "\n"          name
                                   Instance_Name.append(t['Value'])   
                               if t['Key'] == 'LastStartedBy':   
                                   message += "Last started by : " + t['Value'] + "\n"
                           message += "Status : "+ "STOPPED" +"\n" 
                           Instance_ID.append(each['InstanceId'])                    id
                           Instance_Size.append(each['InstanceType'])                type
                           Status.append("Stopped")                                  status
                           Service.append("EC2")                                     service
                           S_no.append(s_no)  
                           Region.append(each['Placement']['AvailabilityZone'])
                           message += "-------------------------------------------------------------------------------------" + "\n"
                        perform the shutdown   
                    shuttingDown = ec2.instances.filter(InstanceIds=RunningInstances).stop()
                    print (shuttingDown) 
              
              
        #  --------------------------RDS-----------------------------------------------------------------------------
            

       for ls in ec2_regions:    
           rds_client = boto3.client('rds',region_name=ls)    
           instances = rds_client.describe_db_instances()               
           for each in range(len(instances['DBInstances'])): 
               s_no = s_no+1
               Account_Name.append("Devops")
               S_no.append(s_no) 
               Account_ID.append(id)  
               message += "RDS" + "\n"        
               message += "Name : " + instances['DBInstances'][each]['DBInstanceIdentifier'] +"\n"
               message += "ID : " + instances['DBInstances'][each]['DbiResourceId'] +'\n'
               message += "Last Started By : " + str(instances['DBInstances'][each]['TagList'][1]['Value']) +"\n"              
               message += "Status : " + "STOPPED" + "\n"
               message += "--------------------------------------------------------------------------------------" + "\n"
               available = [i['DBInstanceIdentifier'] for i in instances['DBInstances'] if i['DBInstanceStatus'] == 'available']
                      for x in available:
                          response = rds_client.stop_db_instance(
                          DBInstanceIdentifier = x
                          )   
                         print (len(available))                  
               Service.append("RDS")  
               Instance_Name.append(instances['DBInstances'][each]['DBInstanceIdentifier'])
               Instance_ID.append(instances['DBInstances'][each]['DbiResourceId'])
               Instance_Size.append(instances['DBInstances'][each]['DBInstanceClass'])   
               Status.append("Stopped")
               Region.append(instances['DBInstances'][each]['AvailabilityZone'])
            
               
            
        #  ------------------------Table work--------------------------------------------------------------------------------
    
          print(len(S_no))
          print(len(Account_ID))
          print(len(Instance_Name))
          print(len(Service)) 
          print(len(Instance_ID))
          print(len(Instance_Size))      
          print(len(Region))    
         
       Tab_message = ""        
       Tab_message += "\n"
       Tab_message += "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------" + "\n"
       Tab_message += "|{}{}{}{}{}{}{}{}".format('S no'.ljust(7," "), 'Account Id'.center(25," "), 'Service Name'.center(25," "), 'Service'.center(10," "),'Service Id'.center(40," "),'Service Size'.center(40," "),'Region'.center(20," ") ,'Status'.rjust(20," ")) + "\n"
       Tab_message += "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------" + "\n"
    
       for i in range(len(S_no)):
           Tab_message += "---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------" +"\n"
           Tab_message += "|{}{}{}{}{}{}{}{}".format(str(S_no[i]).ljust(7," "),str(Account_ID[i]).center(25," "),str(Instance_Name[i]).center(25," ") ,str(Service[i]).center(10," "), str(Instance_ID[i]).center(40," "), str(Instance_Size[i]).center(30," "), str(Region[i]).center(20," ") ,"Stopped".rjust(20," ")) + "\n"
           Tab_message += "---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------" + "\n" 
       ids.append(Tab_message)
    
       str1 = ""
       s=str1.join(ids)
    
            
        #  -------------------------------message delivery work---------------------------------------------------------------
       if message == "":   
           message =" No EC2 or RDS instances are running currently!!!"
           resp = client_sns.publish(TargetArn="arn:aws:sns:ap-south-1:322971359654:RDS_EC2_Status", Message=message, Subject="RDS and EC2 Detail")
       else:
           resp = client_sns.publish(TargetArn="arn:aws:sns:ap-south-1:322971359654:RDS_EC2_Status", Message=message, Subject="RDS and EC2 Detail")   
           print(message)



    
    
                    #    -----------for table-----------
          if Tab_message == "":   
              Tab_message =" No EC2 or RDS instances are running currently!!!"
              resp = client_sns.publish(TargetArn="arn:aws:sns:ap-south-1:322971359654:rds_ec2_info", Message=Tab_message, Subject="RDS and EC2 Detail")
          else:
              resp = client_sns.publish(TargetArn="arn:aws:sns:ap-south-1:322971359654:rds_ec2_info", Message=Tab_message, Subject="RDS and EC2 Detail")   
              print(Tab_message)   
        
        
        #  --------------------------sending data as an attachment------------------------------------------------------
    
   

          data={'S No ':S_no, 'Account Id':Account_ID, 'Account Name':Account_Name,'Service': Service,'Service Name': Instance_Name,'Service ID': Instance_ID,'Size': Instance_Size,'Region':Region,'Status':Status}
          df=pd.DataFrame(data)
          csv_buffer = BytesIO()
          s3 = boto3.resource('s3')
    
          filename = "EC2 and RDS Details.csv"                
          k = "Stop Instance List/"+filename                                 Name of folder where Elastic Ip details is stored
          df.to_csv(csv_buffer)
          content = csv_buffer.getvalue()
          d=s3.Object('  abcbuckettest',k).put(Body=content) 
        
          s3 = boto3.client("s3")    
          SENDER = "  abc.abc@gmail.com"                        specify the email
          RECIPIENT = "  abcabc1309@gmail.com"
          AWS_REGION = "ap-south-1"
        
          FILE_NAME = "EC2 and RDS Details.csv"                             Name of folder where Elastic Ip details is stored
          k = "Stop Instance List/"+ filename                                k = key name to get the document                   
          TMP_FILE_NAME =  '/tmp/' + FILE_NAME
          s3.download_file('  abcbuckettest', k, TMP_FILE_NAME)
          ATTACHMENT = TMP_FILE_NAME
          SUBJECT = "EC2 and Rds Details"
          BODY_TEXT  = """
          Hello,
        
          Please find the EC2 and RDS Details attached in the document.
        
          Best Regards,
            abc
            """
        
          client = boto3.client('ses',region_name=AWS_REGION)
          msg = MIMEMultipart()
                 Add subject, from and to lines.
          msg['Subject'] = SUBJECT 
          msg['From'] = SENDER 
          msg['To'] = RECIPIENT
          textpart = MIMEText(BODY_TEXT)  
          msg.attach(textpart)
          att = MIMEApplication(open(ATTACHMENT, 'rb').read())
          att.add_header('Content-Disposition','attachment',filename=ATTACHMENT)
          msg.attach(att)
          print(msg)
          try:
              response = client.send_raw_email(
                      Source=SENDER,
                      Destinations=['  abc.abc@gmail.com','  abc.abc1309@gmail.com'],
                      RawMessage={ 'Data':msg.as_string() }
              )
          except ClientError as e:   
              print(e.response['Error']['Message'])
          else:
              print("Email sent! Message ID:",response['MessageId'])

   import boto3 
   import pandas as pd
   from io import BytesIO   
   import email   
   from botocore.exceptions import ClientError
   from email.mime.multipart import MIMEMultipart
   from email.mime.text import MIMEText
   from email.mime.application import MIMEApplication

   def lambda_handler(event, context):
    
       client = boto3.client('ec2') 
       id = boto3.client('sts').get_caller_identity().get('Account')   
  
        
       s3 = boto3.client("s3")    
       SENDER = "  abc.  abc@gmail.com"                          specify the email
       RECIPIENT = "  abc  abc1309@gmail.com"
       AWS_REGION = "ap-south-1"
            
       SUBJECT = "EC2 and Rds Details"
       BODY_TEXT  = """
       Hello,
        
       No EC2 or RDS are running currently.
            
       Best Regards,
         abc
         """
            
       client = boto3.client('ses',region_name=AWS_REGION)
       msg = MIMEMultipart()
                  Add subject, from and to lines.
       msg['Subject'] = SUBJECT 
       msg['From'] = SENDER 
       msg['To'] = RECIPIENT
       textpart = MIMEText(BODY_TEXT)  
       msg.attach(textpart)   
       try:
           response = client.send_raw_email(
                   Source=SENDER,
                   Destinations=['  abc.  abc@gmail.com','  abcabc1309@gmail.com'],
                   RawMessage={ 'Data':msg.as_string() }
           )
       except ClientError as e:   
           print(e.response['Error']['Message'])
       else:
           print("Email sent! Message ID:",response['MessageId'])



 
    
                 
   
   
   

     
        
        
   
    
   

    
  
   
   

         
  
        
        
   
    
   

    
  
   
   

     
        
        
   
    
   

    
  
   
   

      
