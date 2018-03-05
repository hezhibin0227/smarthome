#!/usr/bin/python
# -*- coding: UTF-8 -*-

import boto
from setenv import env_ecs_secret_key

class ecsTestDrive:
    def __init__(self):
        self.ecs_access_key_id = '131607222163333044@ecstestdrive.emc.com'  
        self.ecs_secret_key = env_ecs_secret_key
        self.bucket_name = 'new-bucket-c91a56a0'

        self.session = boto.connect_s3(self.ecs_access_key_id, self.ecs_secret_key, host='object.ecstestdrive.com') 
        self.bucket = self.session.get_bucket(self.bucket_name)
        print ("["+ __name__ + "] Log >> " + "ECS connection is: " + str(self.session))
        print ("["+ __name__ + "] Log >> " + "Bucket is: " + str(self.bucket))

        
    def upload_to_ecs(self, file_name, file_type):
        k = self.bucket.new_key(file_name)
        k.set_metadata('wx_filetype', file_type)
        k.set_contents_from_filename(file_name)
        k.set_acl('public-read')
        print ("["+ __name__ + "] Log >> " + "The object's key is: "+str(k))


############################### url to access object ##########################################
#  https://new-bucket-c91a56a0.object.ecstestdrive.com/180223-174345.png                    (N)
#  https://131607222163333044.public.ecstestdrive.com/new-bucket-c91a56a0/180223-174345.png (Y)
###############################################################################################