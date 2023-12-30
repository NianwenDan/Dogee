import httpx
import asyncio
import gzip, shutil
from config import CDN_LOGS_STOREPATH as storePATH
from config import MERGE_LOG
import os, sys
import logger
import mytimedate
import api.cdn.log

def mergeLogs(mergePATH="", domainName="UNKNOWN.DOMAIN"):
    logger.new('info', "Merge Logs: " + domainName)
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
        logger.new('debug', 'Merge File: ' + mergePATH + filename)
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


async def save_log_local(fullStorePATH: str, url: str) -> None:
    async with httpx.AsyncClient() as client:
        logger.new('info', 'httpx request: ' + url)
        response = await client.get(url)

        if response.status_code == 200:
            # Write the content to the file asynchronously
            with open(fullStorePATH, "wb") as f:
                f.write(response.content)
            logger.new('info', 'Stored file to ' + fullStorePATH)
        else:
            logger.new('error', f'Failed to download {url} with status code: {response.status_code}')


async def download_all_logs():
    # 获取一下昨天的时间
    date_list = mytimedate.get('yesterday', 1)
    year, month, day = date_list
    # 获取需要下载的连接
    log_links = api.cdn.log.get()
    
    tasks = []

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
            logger.new('error', 'Faild to create directory: ' + str(exc))
            sys.exit(1)

        for info in log_infos:
            file_name = info['name']
            url = info['url']
            # 定义存储路径为{storePATH}/{year}/{month}/{day}/{file_name}.gz
            fullStorePATH = domainStorePATH + f'{file_name}.gz'
            
            task = asyncio.create_task(save_log_local(fullStorePATH, url))
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


def download():
    asyncio.run(download_all_logs())