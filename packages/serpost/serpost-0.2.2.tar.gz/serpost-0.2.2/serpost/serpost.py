# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import sys
from datetime import datetime

if sys.version_info >= (3, 0):
    from urllib.request import urlopen, Request
else:
    from urllib2 import urlopen, Request


TRACKING_URL = 'http://clientes.serpost.com.pe/prj_online/Web_Busqueda.aspx/Consultar_Tracking'
TRACKING_DETAIL_URL = 'http://clientes.serpost.com.pe/prj_online/Web_Busqueda.aspx/Consultar_Tracking_Detalle_IPS'


def _make_request(url, payload):
    headers = {
        'Content-Type': 'application/json',
    }
    req = Request(url, headers=headers)
    data = json.dumps(payload).encode('utf-8')
    response = urlopen(req, data=data)
    return json.loads(response.read().decode('utf-8'))


def _process_detail(data):
    res = []
    for record in data:
        date = datetime.strptime(record['RetornoCadena3'].strip(), '%d/%m/%Y')
        res.append({
            'place': record['RetornoCadena2'].strip(),
            'date': date,
            'message': record['RetornoCadena4'].strip(),
        })
    return sorted(res, key=lambda x: x['date'])


def query_tracking_code(tracking_code, year=None):
    """
    Given a tracking_code return a list of events related the tracking code
    """
    payload = {
        'Anio': year or datetime.now().year,
        'Tracking': tracking_code,
    }
    response = _make_request(TRACKING_URL, payload)

    if not response['d']:
        return []

    data = response['d'][0]

    destination = data['RetornoCadena6']
    payload.update({
        'Destino': destination,
    })

    response = _make_request(TRACKING_DETAIL_URL, payload)
    return _process_detail(response['d'])
