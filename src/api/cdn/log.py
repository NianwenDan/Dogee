import src.logger as logger
import src.api.dogecloud_api as dogecloud_api
import src.api.cdn.domain as domain
import src.mytimedate as mytimedate


def get_domain_ids() -> list:
    '''
    Get all domain ids

    :returns: A 2-D list of [domain ids, domain names]
    '''
    response = domain.list()
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
    

def get() -> dict:
    '''
    Get all downloadable links

    :returns: A dictionary of all downloadable links
    '''
    # Dictionary to store all downloadable links
    log_info = {}
    # ex for domain_ids = [[10008, 'nwdan.com'], [10010, 'www.nwdan.com']]
    domain_ids = get_domain_ids()
    # 获取一下昨天的时间
    date = mytimedate.get('yesterday', 0)
    
    for id, name in domain_ids:
        api_path = f'/cdn/log/list.json?id={id}&date={date}&page_size=100'
        data = dogecloud_api.send(api_path)
        if data['code'] == 200:
            log_info[name] = data['data']['log_list']

    logger.new('debug', '\{domain\: its_log_info\}', log_info)

    # 返回一个字典{'域名'：'对应域名的log信息'}
    return log_info

