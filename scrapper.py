import requests
from bs4 import BeautifulSoup
import json
import re
import csv
def collect_data(url, array):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    pattern = re.compile(r's:"[A-Z]*"', re.DOTALL)
    soup_str = str(soup)
    matches = pattern.findall(soup_str)
    for match in matches:
        pattern2 = re.compile(r'[A-Z]+')
        array.append(pattern2.findall(match))


