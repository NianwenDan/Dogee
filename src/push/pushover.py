import httpx
import src.logger as logger
import src.config as config
import asyncio
import json

# Define the number of concurrent tasks allowed
MAX_CONCURRENT_TASKS = 2

# Create the semaphore
semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

async def req(user: str, title: str, msg : str, priority: int=0) -> None:
    '''
    Send message to pushover

    :param user: user key
    :param title: message title
    :param msg: message to send
    :param priority: message priority

    :returns: None
    '''
    payload = {
        'token': config.PUSHOVER_APP_TOKEN,
        'user': user, 
        'message': str(msg), 
        'title': str(title),
        'priority': priority
    }

    headers = {
        'accept': "application/json",
        'content-type': "application/json"
    }
    
    async with semaphore:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post('https://api.pushover.net/1/messages.json', data=json.dumps(payload), headers=headers)
                resp.raise_for_status()
            logger.new('info', 'PUSHOVER PUSH:', str(user)[:8])
        except Exception as e:
            logger.new('error', 'Pushover push error:', e)
            return
        else:
            logger.new('debug', 'Pushover push success:', resp.json())
            return