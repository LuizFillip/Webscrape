# -*- coding: utf-8 -*-
"""
Created on Wed May 15 09:22:01 2024

@author: Luiz
"""



import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

# URL and credentials
url = 'https://aer-nc-web.nict.go.jp/gaia/wk3/gaia/'
username = 'realion'
password = 'DataDL01'

# Send the request with authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password))

# Check if the request was successful
if response.status_code == 200:
    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    # Do something with the soup object
    print(soup.prettify())
else:
    print(f"Failed to access the URL: {response.status_code}")
