import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Dogee command line interface.")
    subparsers = parser.add_subparsers(dest='command', help='Sub-command help')

    # Define the 'cdn' sub-command
    parser_cdn = subparsers.add_parser('cdn', help='CDN commands')
    cdn_subparsers = parser_cdn.add_subparsers(dest='cdn_command', help='CDN sub-command help')

    # Define the 'domain' sub-command under 'cdn'
    parser_cdn_domain = cdn_subparsers.add_parser('domain', help='CDN domain commands')
    parser_cdn_domain.add_argument('domain_command', choices=['list'], help='CDN domain sub-command')

    # Define the 'cert' sub-command under 'cdn'
    parser_cdn_cert = cdn_subparsers.add_parser('cert', help='CDN cert commands')
    parser_cdn_cert.add_argument('cert_command', choices=['list'], help='CDN cert sub-command')

    # Define the '-t' option
    parser.add_argument('-t', action='store_true', help='Run a test.')

    # Define the '-v' option
    parser.add_argument('-v', action='store_true', help='Print version and exit.')

    return parser.parse_args()

