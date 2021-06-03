
import json
import os
import pickle as pkl
import time
import sys
import subprocess
import numpy as np

subprocess.check_call([sys.executable, "-m", "pip", "install", "sagemaker"])

import boto3
import sagemaker

import sagemaker_xgboost_container.encoder as xgb_encoders

boto_session = boto3.Session()
boto_fs_client = boto_session.client(service_name='sagemaker-featurestore-runtime')

def model_fn(model_dir):
    print ('processing - in model_fn')
    return None


def input_fn(request_body, request_content_type):
    print ('processing - in input_fn')
    return request_body


def predict_fn(input_data, model):
    print ('processing - in predict_fn')
    
    params = input_data.split(',')
    fg_name = params[0]
    input_feat_id = int(params[1])
    
    
    start = time.time()
    rec = boto_fs_client.get_record(FeatureGroupName=fg_name, RecordIdentifierValueAsString=str(input_feat_id))
    end = time.time()
    feat = rec.get('Record', None)
    if not feat:
        print (f'processing - unable to read feature record with id {input_feat_id}, for fg {fg_name}')
    else:
        resp_feat_id = feat[0]['ValueAsString']
        print (f'processing - successfull get of feature record with id {resp_feat_id}, in fg {fg_name}')
    duration = end-start
    
    print (f'processing - duration = {duration}')
    
    return duration


def output_fn(prediction, content_type):
    print ('processing - output_fn', prediction)
    return str(prediction)
