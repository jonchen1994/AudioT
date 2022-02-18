import boto3
import pandas as pd
import os 
from sagemaker import get_execution_role
import numpy as np
import io

def createDirs(root, dirList):
    finDirs = []
    for items in dirList:
        path = os.path.join(root, items)
        if not os.path.exists(path):
            os.mkdir(path)
        finDirs.append(path)
    return finDirs

def dwnldBucket(bucket, root, dir_name = 'All'):
    if dir_name == 'All':
        obj = s3_conn.list_objects(Bucket = bucket)['Contents']
        dlist = list(set([x['Key'].split('/')[0] for x in obj]))
    elif type(dir_name) != list:
        dlist = [dir_name]
    print(dlist)
    createDirs(root, dlist)
    for direct in dlist:
        files = s3_conn.list_objects(Bucket = bucket, Prefix=direct)['Contents']
        for ii in range(len(files)):
            if ii > 0:
                file_src = files[ii]['Key']
                print(ii, file_src)
                folder = os.path.abspath('/root/AudioT/data')
                file_dst =  os.path.join(root,file_src)
                s3_conn.download_file(bucket_name,file_src , file_dst)