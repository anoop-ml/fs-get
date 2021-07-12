import json
import base64
import subprocess
import os
import sys
from datetime import datetime
import time

import boto3

print(f'boto3 version: {boto3.__version__}')
try:
    boto_session = boto3.Session()
    boto_fs_client = boto_session.client(
        service_name='sagemaker-featurestore-runtime'
    )
except:
    print(f'Failed while connecting to SageMaker Feature Store')
    print(f'Unexpected error: {sys.exc_info()[0]}')

def get_fs_record(boto_fs_client, fg_name, feat_id, feat_names=None):
    import time
    
    req = dict(
        FeatureGroupName=fg_name, 
        RecordIdentifierValueAsString=str(feat_id)
    )
    if feat_names:
        req['FeatureNames'] = feat_names
    
    start = time.time()
    record = boto_fs_client.get_record(**req)
    end = time.time()
    duration = end-start
    
    return (record.get('Record', None), duration)

def lambda_handler(event, context):
    fg_name = event['featureGrpName']
    feat_id = event['featureId']
    
    print(f'Received feature with id = {feat_id} for feature group = {fg_name}')
    
    _, duration1 = get_fs_record(boto_fs_client, fg_name, feat_id)
    
    _, duration2 = get_fs_record(boto_fs_client, fg_name, feat_id)
    
    
    
    return {
        'fs_read1': duration1, 
        'fs_read2': duration2
        
    }