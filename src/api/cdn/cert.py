import src.api.dogecloud_api as dogecloud_api


def list() -> dict:
    api_path = '/cdn/cert/list.json'
    data = dogecloud_api.send(api_path)
    return data

def upload() -> dict:
    pass

def delete() -> dict:
    pass