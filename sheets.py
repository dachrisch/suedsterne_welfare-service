# coding=utf-8
from os import path

from apiclient import discovery
from cachetools import TTLCache
from google.oauth2 import service_account

import config
from my_logging import get_logger


def key(sheet_id, sheet_range):
    return sheet_id + sheet_range


class SheetConnector(TTLCache):
    def __init__(self, sheet_id):
        TTLCache.__init__(self, maxsize=128, ttl=600)
        self.__sheet_id = sheet_id

    def values_for_range(self, sheet_range):
        values = None
        try:
            values = self[key(self.__sheet_id, sheet_range)]
            get_logger(__name__).debug('using cached values')
        except KeyError:
            get_logger(__name__).debug('invocation not cached')

        if not values:
            credentials = service_account.Credentials.from_service_account_file(
                path.join(path.join(path.expanduser('~'), '.credentials'), 'suedsterne-1328.json'),
                scopes=config.SCOPES).with_subject('cd@it-agile.de')
            service = discovery.build('sheets', 'v4', credentials=credentials, cache_discovery=False)
            values = service.spreadsheets().values().get(spreadsheetId=self.__sheet_id,
                                                         range=sheet_range).execute().get('values', [])
            self[key(self.__sheet_id, sheet_range)] = values
        return values
