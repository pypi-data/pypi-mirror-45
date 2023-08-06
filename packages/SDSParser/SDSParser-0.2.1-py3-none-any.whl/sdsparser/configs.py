import os
import json
from importlib import resources


class Configs:

    SDS_DEV = os.environ.get('SDS_DEV', False) in ('TRUE', '1')

    REQUEST_KEYS = [
        'manufacturer',
        'product_name',
        'flash_point',
        'specific_gravity',
        'nfpa_fire',
        'nfpa_health',
        'nfpa_reactivity',
        'sara_311',
        'revision_date',
        'physical_state',
        'cas_number',
    ]

    REGEXES = dict()

    regex_file_text = resources.read_binary('static', 'regexes.json')
    for regex_dict in json.loads(regex_file_text):
        REGEXES[regex_dict['name']] = regex_dict

    SUPPORTED_MANUFACTURERS = set(REGEXES.keys())
    SUPPORTED_MANUFACTURERS.remove('default')
