# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 21:51:59 2022

@author: mukhopad-admin
"""
import os
import time
import numpy as np
from transcribe import assemblyai
from transcribe import utils
from transcribe.compare import compare
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def predict():
    filename = request.files['videofile']
    groundtruth, assembly, confidence = assemblyai.get_transcript(filename)
    return render_template(
        'index.html', groundtruth=groundtruth, assembly=assembly, confidence=confidence)

if __name__ == "__main__":
    app.run(port=3000, debug=True)
