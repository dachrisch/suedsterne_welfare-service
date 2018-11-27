# coding=utf-8

import jsonpickle
from flask import Flask

from config import MUCKI_TRACKER_SHEET_ID
from sheets import SheetConnector
from welfare import WelfareStatus

remote_app = Flask(__name__)
welfare_status = WelfareStatus(SheetConnector(MUCKI_TRACKER_SHEET_ID))


@remote_app.route('/welfare/api/v1.0/status', methods=['GET'])
def status():
    return jsonpickle.encode(welfare_status.team_status, unpicklable=False)


@remote_app.route('/welfare/api/v1.0/shout_out', methods=['GET'])
def shout_out():
    return jsonpickle.encode(welfare_status.shout_out, unpicklable=False)
