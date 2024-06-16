from src.api.cdn.domain import filter_domains
from src.api.cdn.cert import filter_certs
import src.logger as logger


def check_domain_cert() -> dict:
    response = []
    domain_infos = filter_domains(status='online')
    certs_infos = filter_certs()
    certs_infos_dict = {}
    # Convert certs info to a dictionary improve efficiency
    for cert in certs_infos:
        certs_infos_dict[cert['id']] = cert
    if not domain_infos:
        return response
    for domain in domain_infos:
        did = domain['id']
        dname = domain['name']
        cid = domain['cert_id']
        cert_ttl = None
        if certs_infos_dict.get(cid):
            cert_ttl = certs_infos_dict[cid]['ttl']
        else:
            logger.new('error', 'Cannot Find Certificate ID: ', cid)
        response.append({
            'did' : did,
            'dname' : dname,
            'cid' : cid,
            'cert_ttl' : cert_ttl
        })
    logger.new('info', 'Domain SSL Certificate TTL:', response)
    return response


def start() -> str:
    msg = '#CDN SSL CERTIFICATE\n'
    domain_ssl_ttl = check_domain_cert()
    for i in domain_ssl_ttl:
        domain_name = i['dname']
        ttl_days = int(i['cert_ttl'] / 60 / 60 / 24)
        m = f'[{domain_name}] certs left {ttl_days} days\n'
        msg += m
    return msg