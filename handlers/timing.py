from datetime import datetime, timedelta, date, time
from typing import Tuple

from tornado.escape import url_unescape
from tornado.web import RequestHandler

data = {
    "Monday": {
        "Wake Up": {
            "time": "07:00",
            "target": "19.5",
        },
        "Leave": {
            "time": "09:00",
            "target": "17.5",
        },
        "Home": {
            "time": "18:00",
            "target": "19.5",
        },
        "Sleep": {
            "time": "21:00",
            "target": "17.5",
        }
    },
    "Tuesday": {
        "Wake Up": {
            "time": "07:00",
            "target": "19.5",
        },
        "Leave": {
            "time": "09:00",
            "target": "17.5",
        },
        "Home": {
            "time": "18:00",
            "target": "19.5",
        },
        "Sleep": {
            "time": "21:00",
            "target": "17.5",
        }
    },
    "Wednesday": {
        "Wake Up": {
            "time": "07:00",
            "target": "19.5",
        },
        "Leave": {
            "time": "09:00",
            "target": "17.5",
        },
        "Home": {
            "time": "18:00",
            "target": "19.5",
        },
        "Sleep": {
            "time": "21:00",
            "target": "17.5",
        }
    },
    "Thursday": {
        "Wake Up": {
            "time": "07:00",
            "target": "19.5",
        },
        "Leave": {
            "time": "09:00",
            "target": "17.5",
        },
        "Home": {
            "time": "18:00",
            "target": "19.5",
        },
        "Sleep": {
            "time": "21:00",
            "target": "17.5",
        }
    },
    "Friday": {
        "Wake Up": {
            "time": "07:00",
            "target": "19.5",
        },
        "Leave": {
            "time": "09:00",
            "target": "17.5",
        },
        "Home": {
            "time": "18:00",
            "target": "19.5",
        },
        "Sleep": {
            "time": "21:00",
            "target": "17.5",
        }
    },
    "Saturday": {
        "Wake Up": {
            "time": "07:00",
            "target": "19.5",
        },
        "Leave": {
            "time": "09:00",
            "target": "17.5",
        },
        "Home": {
            "time": "18:00",
            "target": "19.5",
        },
        "Sleep": {
            "time": "21:00",
            "target": "17.5",
        }
    },
    "Sunday": {
        "Wake Up": {
            "time": "07:00",
            "target": "19.5",
        },
        "Leave": {
            "time": "09:00",
            "target": "17.5",
        },
        "Home": {
            "time": "18:00",
            "target": "19.5",
        },
        "Sleep": {
            "time": "21:00",
            "target": "17.5",
        }
    }
}


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
    for i, day in enumerate(data):
        for period in data[day]:
            current = data[day][period]
            hour, minute = current["time"].split(":")
            _time = datetime.combine(monday_of_week + timedelta(days=i), time(hour=int(hour), minute=int(minute)))
            transitions.append(
                Target(_time, float(current["target"]), period)
            )
    # TODO: verify order
    return transitions


def get_targets() -> Tuple[Target, Target]:
    current_datetime = datetime.now()
    transitions = parse_data_to_transitions()
    current_target = [target for target in transitions if target.transition < current_datetime][-1]
    next_target = [target for target in transitions if target > current_datetime][1]

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
            data[day][period][thing] = value
        self.render("time_template.html", title="My title", data=data)

    def get(self):
        self.render("time_template.html", title="My title", data=data)
