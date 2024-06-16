import httpx
import asyncio
import gzip, shutil
from src.config import CDN_LOGS_STOREPATH as storePATH
from src.config import MERGE_LOG
from src.api.cdn.domain import list_ids
import src.api.dogecloud_api as dogecloud_api
import src.mytimedate as mytimedate
import src.logger as logger
import os, sys
import traceback
import time


def get_downloadable_log_links() -> dict:
    '''
    Get all downloadable links

    :returns: A dictionary of all downloadable links
    '''
    # Dictionary to store all downloadable links
    log_info = {}
    # ex for domain_ids = [[10008, 'nwdan.com'], [10010, 'www.nwdan.com']]
    domain_ids = list_ids()
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


def mergeLogs(mergePATH="", domainName="UNKNOWN.DOMAIN") -> None:
    '''
    Merge logs in mergePATH and save them to the parent directory

    :param mergePATH: The path of the directory to be merged
    :param domainName: The name of the domain

    :returns: None
    '''
    logger.new('info', 'Merge Logs:', domainName)
    if mergePATH == "":
        return
    
    time = mytimedate.get('yesterday', 0)
    dir_list = os.listdir(mergePATH)
    overseas_logs = []
    mainland_logs = []
    merged_filePATH_overseas = f'{mergePATH}../{domainName}_{time}_overseas.log'
    merged_filePATH_mainland = f'{mergePATH}../{domainName}_{time}_mainland.log'

    for i in dir_list:
        if "mainland" in i:
            mainland_logs.append(i)
        if "overseas" in i:
            overseas_logs.append(i)

    overseas_logs.sort()
    mainland_logs.sort()

    for filename in overseas_logs:
        logger.new('debug', 'Merge File:', mergePATH, filename)
        with gzip.open(mergePATH + filename, 'rb') as f_in:
            with open(merged_filePATH_overseas, 'ab') as f_out:
                shutil.copyfileobj(f_in, f_out)
                f_out.close()

        f_in.close()

    for filename in mainland_logs:
        with gzip.open(mergePATH + filename, 'rb') as f_in:
            with open(merged_filePATH_mainland, 'ab') as f_out:
                shutil.copyfileobj(f_in, f_out)
                f_out.close()

        f_in.close()


async def download_log(fullStorePATH: str, url: str) -> None:
    '''
    Download log file from url and save it to fullStorePATH

    :param fullStorePATH: The full path of the file to be stored
    :param url: The url of the file to be downloaded

    :returns: None
    '''
    try:
        async with httpx.AsyncClient() as client:
            logger.new('debug', 'httpx request:', url)
            response = await client.get(url)
            # Write the content to the file asynchronously
            with open(fullStorePATH, "wb") as f:
                f.write(response.content)
            logger.new('debug', 'Stored file to', fullStorePATH)
    except httpx.ConnectTimeout as exc:
        logger.new('error', 'httpx request timeout:', exc.request.url)
    except Exception:
        logger.new('error', 'httpx unidentified error:', traceback.format_exc())


async def download_and_manage_daily_logs() -> None:
    '''
    Download CDN logs and manage them

    :returns: None
    '''
    # 获取一下昨天的时间
    date_list = mytimedate.get('yesterday', 1)
    year, month, day = date_list
    # 获取需要下载的连接
    log_links = get_downloadable_log_links()
    
    tasks = []

    logger.new('info', 'Downloading logs...')

    for domain_name, log_infos in log_links.items():
        #domainStorePATH = storePATH + "/" + key + "/" + year + "/" + month + "/logtemps" + "/"
        domainStorePATH = f'{storePATH}/{domain_name}/{year}/{month}/logtemps/'

        # 关闭合并日志功能
        if not MERGE_LOG:
            domainStorePATH = f'{storePATH}/{domain_name}/{year}/{month}/{day}/'

        # 文件夹不存在得先建个文件夹, exist_ok=True 代表路径存在不要抛出异常
        try:
            os.makedirs(os.path.dirname(domainStorePATH), exist_ok=True)
        except OSError as exc:
            logger.new('error', 'Faild to create directory:', exc)
            sys.exit(1)

        for info in log_infos:
            file_name = info['name']
            url = info['url']
            # 定义存储路径为{storePATH}/{year}/{month}/{day}/{file_name}.gz
            fullStorePATH = domainStorePATH + f'{file_name}.gz'
            
            task = asyncio.create_task(download_log(fullStorePATH, url))
            #logger.new('debug', 'Adding task: ' + str(task))
            tasks.append(task)
        
    await asyncio.gather(*tasks)

    # 合并日志功能
    if MERGE_LOG:
        for domain_name, log_infos in log_links.items():
            domainStorePATH = f'{storePATH}/{domain_name}/{year}/{month}/logtemps/'
            # Merge Logs
            mergeLogs(domainStorePATH, domain_name)
            # Remove Tempoary Directory
            shutil.rmtree(domainStorePATH)


def download() -> str:
    '''
    Download CDN logs and save them to local

    :returns: A string that indicates the result
    '''
    asyncio.run(download_and_manage_daily_logs())
    cdn_log_time = mytimedate.get('yesterday', 0)
    curr_sys_time = time.localtime() 
    curr_clock = time.strftime('%Y-%m-%d %H:%M:%S %Z UTC%z', curr_sys_time)
    return f'{curr_clock}\n#CDN Log Download\n\nDogecloud CDN logs for {cdn_log_time} have been downloaded!\n多吉云CDN日志({cdn_log_time})已下载完成!'