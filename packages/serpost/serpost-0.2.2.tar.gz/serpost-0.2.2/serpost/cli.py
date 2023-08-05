# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import argparse

from .serpost import query_tracking_code

DATE_FORMAT = '%d/%m/%Y %H:%M'


def format_data(data, code):
    title = 'Tracking number: {}'.format(code)
    print('{}\n{}'.format(title, '-' * len(title)))
    if not data:
        print('No result')
        return
    template = '{0:16} | {1:100}'
    for item in data:
        date = item['date'].strftime(DATE_FORMAT)
        print(template.format(date, item['message']))
    print('\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('tracking_codes', help='Comma separated tracking codes: eg ABC123,ABC321', type=str)
    parser.add_argument('--year', help='Package year, if this argument is not provided the current year will be taken', type=int)
    args = parser.parse_args()

    for code in args.tracking_codes.split(','):
        format_data(query_tracking_code(code, year=args.year), code)


if __name__ == '__main__':
    main()
