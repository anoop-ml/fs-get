
import json
import os
import pickle as pkl
import time
import sys
import subprocess
import numpy as np
import logging

from sagemaker_containers.beta.framework import encoders


def model_fn(model_dir):
    print ('processing - in model_fn')
    return None


def input_fn(request_body, request_content_type):
    print (f'processing - in input_fn with content_type = {request_content_type}, request_body = {request_body}')
    return request_body


def predict_fn(input_data, model):
    input_data_type = type(input_data)
    print (f'processing - in predict_fn, with input_data = {input_data}, with type = {input_data_type}')
    
    return 100

#ref - https://github.com/aws/sagemaker-xgboost-container/blob/master/src/sagemaker_xgboost_container/handler_service.py
def output_fn(prediction, accept):
    print (f'processing - output_fn with values = {prediction}, for output content_type = {accept}')    
    return str(prediction)
