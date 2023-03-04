#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 11:15:33 2023

@author: svetlanamaslenkova
"""

import numpy as np
from flask import Flask, request, jsonify, render_template, url_for, flash, abort
import pickle
import re


app = Flask(__name__)
app.config['SECRET_KEY'] = '5acfad893553963f90d0827ab37a9f3180d2f5bfa6984ce7'

# load the model
def load_models():
    file_name = "models/model_file.p"
    with open(file_name, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
    return model

# prediction function
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 16)
    loaded_model = load_models()
    result = loaded_model.predict(to_predict)
    return result[0]


def preproccess(response):
    # response = {'location': '0', 'size': '1', 'type_of_ownership': 'Private', \
        # 'job_fam': 'DS', 'experience': 'Junior', 'revenue': '2.2', 'ml_yn': '1', \
            # 'stats_yn': '1', 'older_than_30_days': '1'}
            
    rating = float(re.sub(r"[^0-9.]", '', response['rating']))
    size = int(response['size'])
    revenue = float(re.sub(r"[^0-9.]", '', response['revenue']))
    older_than_30_days = 1 if 'older_than_30_days' in response else 0
    stats_yn = 1 if 'stats_yn' in response else 0
    ml_yn = 1 if 'ml_yn' in response else 0
    location_abu_dhabi = 1 if response['location'] == '1' else 0
    location_dubai = 1 if response['location'] == '2' else 0
    location_other = 1 if response['location'] == '0' else 0
    type_of_ownership_private = 1 if response['type_of_ownership'] == "Private" else 0
    type_of_ownership_public = 1 if response['type_of_ownership'] == "Public" else 0
    type_of_ownership_other = 1 if response['type_of_ownership'] == "Other" else 0
    job_fam_ds = 1 if response['job_fam'] == "DS" else 0
    job_fam_da = 1 if response['job_fam'] == "DA" else 0
    job_fam_ml = 1 if response['job_fam'] == "ML" else 0
    job_fam_other = 1 if response['job_fam'] == "Other" else 0
    experiemnce_other = 1 if response['experience'] == "Middle" else 0
    experiemnce_senior = 1 if response['experience'] == "Senior" else 0
    
    
    to_predict_list = [rating, size, revenue, older_than_30_days, stats_yn, ml_yn, location_abu_dhabi,\
                       location_dubai, type_of_ownership_private,
                       type_of_ownership_other, job_fam_ds, job_fam_da, job_fam_ml, job_fam_other, \
                           experiemnce_other, experiemnce_senior]
    
    return to_predict_list


@app.route("/")
def Home():
    return render_template("index.html")

@app.route('/result', methods = ['POST', 'GET'])
def result():

    if request.method == 'POST':
        response = request.form.to_dict()        
        to_predict_list = preproccess(response)
        result = np.round(int(ValuePredictor(to_predict_list))/1000, 1)	
        result_message = "The expected salary is around {}k AED per month".format(result)
        
        return render_template("index.html", result=result)
    
    abort(400)


# to_predict_list = [4, 2, 10, 0, 1, 1, 1, 0 ,1 ,0 ,1, 0, 0, 0, 1, 0]
# ['rating',
#  'size',
#  'revenue',
#  'older_than_30_days',
#  'stats_yn',
#  'ml_yn',
#  'country_Abu Dhabi',
#  'country_Dubai',
#  'type_of_ownership_Company - Private',
#  'type_of_ownership_Unknown',
#  'job_fam_da',
#  'job_fam_ds',
#  'job_fam_ml',
#  'job_fam_other',
#  'experience_level_other',
#  'experience_level_senior']