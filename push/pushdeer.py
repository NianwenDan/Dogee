import httpx
import logger

async def req(key : str, title: str, msg : str) -> None:
    '''
    Send message to your pushdeer application

    :param key: pushdeer push key
    :param title: message title
    :param msg: message to send

    :returns: None
    '''
    logger.new('info', 'PUSHDEER PUSH: ' + str(key)[:8])
    url = 'https://api2.pushdeer.com/message/push'
    async with httpx.AsyncClient() as client:
        try:
            params = {
                'pushkey' : str(key),
                'text' : title,
                'desp' : msg
            }
            response = await client.get(url, params=params)
            if 'ok' not in response.text:
                logger.new('error', "PUSH ERROR(PUSHDEER): " + str(response.text))
        except httpx.HTTPError as err:
            logger.new('error', "PUSH ERROR(PUSHDEER): " + str(err))

