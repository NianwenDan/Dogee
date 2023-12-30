import httpx
import api.dogecloud_api as dogecloud_api
import logger

def list() -> dict:
    api_path = '/cdn/domain/list.json'
    data = dogecloud_api.send(api_path)
    return data


def offline():
    pass


def online():
    pass

