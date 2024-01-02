import asyncio
import config
# import push.mie as mie
import push.pushdeer as pushdeer
import push.pushover as pushover
# import push.zeptomail as zepomail

async def main(title : str=None, msg : str=None) -> None:
    '''
    Entry point of send message to all push service

    :param title: message title
    :param msg: message to send

    :returns: None
    '''
    # if no title or msg, do not send
    if not title or not msg:
        return
    
    tasks = []
    # if config.ENABLE_QQ_PUSH:
    #     for qqid in config.QQ_PUSH_NUMBERS:
    #         tasks.append(mie.req(qqid, msg))
    if config.PUSHDEER_KEYS:
        for key in config.PUSHDEER_KEYS:
            tasks.append(pushdeer.req(key, title, msg))
    if config.PUSHOVER_APP_TOKEN and config.PUSHOVER_USERS:
        for user in config.PUSHOVER_USERS:
            # user is not empty
            if not user:
                continue
            tasks.append(pushover.req(user, title, msg))
    # if config.ENABLE_ZEPO_MAIL_PUSH:
    #     for email in config.EMAIL_PUSH:
    #         tasks.append(zepomail.req(email, title, msg.replace('\n', ' <br>\n')))
    
    # print(tasks)
    await asyncio.gather(*tasks)
    