import api.dogecloud_api as dogecloud_api

def list() -> dict:
    '''
    List all certificates in dogecloud

    :returns: dict
    '''
    api_path = '/cdn/cert/list.json'
    data = dogecloud_api.send(api_path)
    return data

def upload(note: str, certificate: str, private_key: str) -> dict:
    '''
    Upload a certificate to dogecloud

    :param note: nickname for the certificate
    :param certificate: certificate content
    :param private_key: private key content

    :returns: dict
    '''
    api_path = '/cdn/cert/upload.json'
    payload = {
        'note': note,
        'certificate': certificate,
        'private_key': private_key
    }
    data = dogecloud_api.send(api_path, payload)
    return data

def delete(id: str) -> dict:
    '''
    Delete a certificate from dogecloud

    :param id: certificate id, get it from list()

    :returns: dict
    '''
    api_path = '/cdn/cert/delete.json'
    payload = {
        'id': id
    }
    data = dogecloud_api.send(api_path, payload)
    return data