
import json
import os
import pickle as pkl
import time
import sys
import subprocess
import numpy as np

#from sagemaker_inference import content_types
#from sagemaker_containers.beta.framework import encoders

subprocess.check_call([sys.executable, "-m", "pip", "install", "sagemaker"])

import boto3
import sagemaker

boto_session = boto3.Session()
boto_fs_client = boto_session.client(service_name='sagemaker-featurestore-runtime')
feat_cols = ['f_1','f_2','f_3','f_4','f_5','f_6','f_7','f_8','f_9']

def model_fn(model_dir):
    print ('processing - in model_fn')
    return None


def input_fn(request_body, request_content_type):
    print (f'processing - in input_fn with content_type = {request_content_type}')
    return request_body


def predict_fn(input_data, model):
    print ('processing - in predict_fn')
    
    params = input_data.split(',')
    fg_name = params[0]
    input_feat_id = int(params[1])
    
    
    start = time.time()
    rec = boto_fs_client.get_record(FeatureGroupName=fg_name, RecordIdentifierValueAsString=str(input_feat_id),FeatureNames=feat_cols)
    end = time.time()
    feats = rec.get('Record', None)
    duration = end-start
    
    print (f'processing - duration = {duration}')
    
    if feats:
        return ','.join(i['ValueAsString'] for i in feats)
    else:
        return ''

#ref - https://github.com/aws/sagemaker-xgboost-container/blob/master/src/sagemaker_xgboost_container/handler_service.py
def output_fn(prediction, content_type):
    print (f'processing - output_fn with values = {prediction}, for output content_type = {content_type}')
    return prediction
