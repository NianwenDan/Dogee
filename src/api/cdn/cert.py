import src.api.dogecloud_api as dogecloud_api
from typing import List, Dict, Any


def list() -> dict:
    api_path = '/cdn/cert/list.json'
    data = dogecloud_api.send(api_path)
    return data

def filter_certs() -> List[Dict[str, Any]]:
    data = list()
    response = []
    if data and 'data' in data and 'certs' in data['data']:
        response = data['data']['certs']
    return response

def upload() -> dict:
    pass

def delete() -> dict:
    pass