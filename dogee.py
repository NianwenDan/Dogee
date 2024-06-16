import src.core.download_logs as log
import src.core.renew_cert as renew_cert
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
    push_msg = []
    if config.CDN_LOG_SAVE_ENABLE:
        msg = log.download()
        push_msg.append(msg)
    if config.CDN_SSL_RENEW_ENABLE:
        msg = renew_cert.start()
        push_msg.append('\n\n')
        push_msg.append(msg)
    asyncio.run(src.push.send.main('Dogee Task', ''.join(push_msg)))


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
            data = domain.filter_domains(status='online')
            pprint.pp(data, indent=4)
        elif args.cdn_command == 'cert' and args.cert_command == 'list':
            print("Listing CDN SSL Cert resources...")
            data = cert.filter_certs()
            pprint.pp(data, indent=4)
    else:
        run()

if __name__ == "__main__":
    main()