# coding=utf-8
import os

import jsonpickle
from flask import Flask

from config import MUCKI_TRACKER_SHEET_ID
from google_service.bigquery import InboxZeroBigQueryConnector, SuedSterneBigQueryClientWrapper
from sheets import SheetConnector
from welfare import WelfareStatus

remote_app = Flask(__name__)
welfare_status = WelfareStatus(SheetConnector(MUCKI_TRACKER_SHEET_ID))


class SuedsterneStatus(object):
    def __init__(self, query_connector: InboxZeroBigQueryConnector):
        self.query_connector: InboxZeroBigQueryConnector = query_connector

    @property
    def all_mates(self):
        return self.query_connector.mates()


suedsterne_status = SuedsterneStatus(InboxZeroBigQueryConnector(SuedSterneBigQueryClientWrapper()))


@remote_app.route('/welfare/api/v2.0/mates', methods=['GET'])
def member():
    return jsonpickle.encode(suedsterne_status.all_mates, unpicklable=False)


@remote_app.route('/welfare/api/v1.0/status', methods=['GET'])
def status():
    return jsonpickle.encode(welfare_status.team_status, unpicklable=False)


@remote_app.route('/welfare/api/v1.0/shout_out', methods=['GET'])
def shout_out():
    return jsonpickle.encode(welfare_status.shout_out, unpicklable=False)


if __name__ == '__main__':
    remote_app.run(host=os.getenv('WELFARE_SERVICE_HOST', '0.0.0.0'),
                   port=os.getenv('WELFARE_SERVICE_PORT', 5000))
