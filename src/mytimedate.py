import sys
import pytz
from datetime import datetime, timedelta
from src.config import CDN_LOGS_TIMEZONE as TZ
import src.logger

def get(when: str, format: int=-1):
    # 检查TZ是否合法
    all_timezones = pytz.all_timezones
    if TZ not in all_timezones:
        for i in all_timezones:
            print(i)

        logger.new('error', "Your TimeZone Setting is invalid! Above is all avaiable timezone")
        sys.exit(1)
        
    # 获取今天时间
    today = datetime.now(pytz.timezone(TZ))
    # 获取昨天时间
    yesterday = datetime.now(pytz.timezone(TZ)) - timedelta(1)

    if format == 0: # 返回格式 "YYYY-MM-DD"
        if when == 'today':
            return today.strftime("%Y-%m-%d")
        elif when == 'yesterday':
            return yesterday.strftime("%Y-%m-%d")
        else:
            logger.new('error', 'Undefined date passed')
    elif format == 1: # 返回格式 ["YYYY", "MM", "DD"]
        if when == 'today':
            return [today.strftime("%Y"), today.strftime("%m"), today.strftime("%d")]
        elif when == 'yesterday':
            return [yesterday.strftime("%Y"), yesterday.strftime("%m"), yesterday.strftime("%d")]
        else:
            logger.new('error', 'Undefined date passed')
    else:
        logger.new('error', 'Your TimeZone Type is undefined')
        sys.exit(1)