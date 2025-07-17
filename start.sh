#!/bin/bash

pip install --upgrade pip
pip install --force-reinstall openai==1.3.0
pip install -r requirements.txt

streamlit run app.py