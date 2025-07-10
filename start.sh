#!/bin/bash
pip3 install -r requirements.txt
python3 -m streamlit run app.py --server.port=$PORT --server.enableCORS=false