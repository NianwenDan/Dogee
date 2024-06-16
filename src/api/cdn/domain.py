import src.api.dogecloud_api as dogecloud_api
import src.logger as logger
from typing import List, Dict, Any

def list() -> dict:
    api_path = '/cdn/domain/list.json'
    data = dogecloud_api.send(api_path)
    return data


def filter_domains(status: str = None) -> List[Dict[str, Any]]:
    """
    Filter the domains based on status
    
    :param status: The status to filter by (optional).
    :return: A list of filtered domain dictionaries.
    """
    data = list()
    response = []

    if data and 'data' in data and 'domains' in data['data']:
        domains = data['data']['domains']
        
        for domain in domains:
            if status and domain.get('status') != status:
                continue
            response.append(domain)
    
    return response