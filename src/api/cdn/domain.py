import src.api.dogecloud_api as dogecloud_api
import src.logger as logger

def list() -> dict:
    api_path = '/cdn/domain/list.json'
    data = dogecloud_api.send(api_path)
    return data


def list_ids() -> list:
    '''
    Get all domain ids

    :returns: A 2-D list of [domain ids, domain names]
    '''
    response = list()
    # if response is not empty
    if not response:
        return
    
    res = []
    for i in response['data']['domains']:
        # 只获取启用的域名
        if i['status'] == 'online':
            id = i['id']
            name = i['name']
            res.append([id, name])

    logger.new('info', 'Active Domain List:', res)
    return res