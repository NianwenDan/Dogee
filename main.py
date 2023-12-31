import core.save_logs as log
import push.send
import asyncio
import sys
import config

def run() -> None:
    if config.CDN_LOG_SAVE_ENABLE:
        msg = log.download()
        asyncio.run(push.send.main('Dogee[OK]: CDN Log Download', msg))


def print_version() -> None:
    '''
    Print version number

    :returns: None
    '''
    print('Version 1.0')


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if '-t' in sys.argv:
            print('This is a test.')
        if '-v' in sys.argv:
            print_version()
    else:
        run()

