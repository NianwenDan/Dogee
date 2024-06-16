import core.download_logs as log
import src.config as config
from src.args_parser import parse_args
from src.api.cdn import domain, cert
import pprint
import src.push.send
import asyncio


def run() -> None:
    '''
    Run the program
    '''
    if config.CDN_LOG_SAVE_ENABLE:
        msg = log.download()
        asyncio.run(src.push.send.main('Dogee[OK]: CDN Log Download', msg))


def print_version() -> None:
    '''
    Print version number

    :returns: None
    '''
    print('Version 1.1')


def main():
    args = parse_args()

    if args.v:
        print_version()
    elif args.t:
        print('This is a test.')
        asyncio.run(src.push.send.main('Dogee[OK]: TEST', '#test-msg\nDogee just tested!\n这是一条来自Dogee的测试信息!'))
    elif args.command == 'cdn':
        if args.cdn_command == 'domain' and args.domain_command == 'list':
            print("Listing CDN Domain resources...")
            data = domain.list()
            pprint.pp(data, indent=4)
        elif args.cdn_command == 'cert' and args.cert_command == 'list':
            print("Listing CDN SSL Cert resources...")
            data = cert.list()
            pprint.pp(data, indent=4)
    else:
        run()

if __name__ == "__main__":
    main()