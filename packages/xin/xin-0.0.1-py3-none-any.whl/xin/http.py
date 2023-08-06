"""HTTP module for xin Python Library
"""

import requests


def public_ip_address(**kwargs):
    """Get the public IP address (using httpbin.org's IP API)

    Args:
        **kwargs: Arbitrary keyword arguments.

    Return:
        The requester's public IP Address or '' (if anything was worng)
    """
    try:
        kwargs['timeout'] = kwargs.pop('timeout', 5)
        response = requests.get('http://httpbin.org/ip', **kwargs)
        _public_ip_address, *_ = response.json().get('origin', '').split(',')
        return _public_ip_address
    except BaseException as error:
        print('ERROR:', error)
        return ''


def dynu_ip_update(username: str, password: str, myip='', **kwargs) -> bool:
    """Update the primary IP address for your Dynu domain name

    Args:
        username: Your Dynu username.
        password: Your Dynu password.
        myip: Your public IP address. Will be auto detected if not given.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        The return value. True for success, False otherwise.
    """
    myip = myip or public_ip_address(**kwargs)
    params = {'username': username, 'password': password, 'myip': myip}
    url = 'http://api.dynu.com:8245/nic/update'
    kwargs['timeout'] = kwargs.pop('timeout', 5)
    kwargs['proxies'] = kwargs.pop('proxies', {'http': 'http://127.0.0.1:8118'})
    try:
        response = requests.get(url=url, params=params, **kwargs)
        assert response.text in ['good', 'nochg'], response.text
        return True
    except BaseException as error:
        print('ERROR:', error)
        return False
