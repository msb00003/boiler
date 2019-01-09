from datetime import datetime, timedelta, date, time
from typing import Tuple

from tornado.escape import url_unescape
from tornado.web import RequestHandler

import json

from handlers.timing.generator import get_initial_data, days, periods

DATA_FILE_NAME = "data.json"

DATA = None
try:
    with open(DATA_FILE_NAME, "r") as f:
        DATA = json.load(f)
except:
    DATA = get_initial_data()


class Target:
    def __init__(self, transition: datetime, target: float, period) -> None:
        self.transition = transition
        self.target = target
        self.period = period


def parse_data_to_transitions():
    current_datetime = datetime.now()
    monday_of_week = date.fromtimestamp(
        int((current_datetime - timedelta(days=current_datetime.weekday())).timestamp())
    )
    # so cast all the inputs to datetime

    transitions = []
    for day_i, day_set in enumerate(DATA):
        for period_j, period_set in enumerate(day_set["periods"]):
            hour, minute = period_set["time"].split(":")
            _time = datetime.combine(monday_of_week + timedelta(days=day_i), time(hour=int(hour), minute=int(minute)))
            transitions.append(
                Target(_time, float(period_set["target"]), period_set["period_name"])
            )
    # TODO: verify order
    return transitions


def get_targets() -> Tuple[Target, Target]:
    current_datetime = datetime.now()
    transitions = parse_data_to_transitions()
    current_target = [target for target in transitions if target.transition < current_datetime][-1]
    next_target = [target for target in transitions if target.transition > current_datetime][1]

    return current_target, next_target


class TimingHandler(RequestHandler):
    def post(self):
        body = url_unescape(self.request.body)

        key_values = dict(key_value.split("=") for key_value in
                          [data_set for data_set in body.split("&")]
                          )
        for whole_key, value in key_values.items():
            split = whole_key.split("-")
            if len(split) == 2:
                continue

            day, period, thing = split
            DATA[days.index(day)]["periods"][periods.index(period)][thing] = value
            with open(DATA_FILE_NAME, "w") as fw:
                json.dump(DATA, fw, indent=4)

        self.render("time_template.html", title="My title", data=DATA)

    def get(self):
        self.render("time_template.html", title="My title", data=DATA)
