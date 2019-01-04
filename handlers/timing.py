from datetime import datetime, timedelta, date, time

from tornado.escape import url_unescape
from tornado.web import RequestHandler


class Target:
    def __init__(self, transition: datetime, target: float) -> None:
        self.transition = transition
        self.target = target


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


def parse_data_to_transitions():
    current_datetime = datetime.now()
    monday_of_week = date.fromtimestamp(
        int((current_datetime - timedelta(days=current_datetime.weekday())).timestamp())
    )
    # so cast all the inputs to datetime

    transitions = {}
    for i, day in enumerate(data):
        for period in data[day]:
            current = data[day][period]
            hour, minute = current["time"].split(":")
            _time = datetime.combine(monday_of_week + timedelta(days=i), time(hour=int(hour), minute=int(minute)))
            target = current["target"]
            transitions[_time] = target

    return transitions


def get_target(transitions, current_datetime) -> Target:
    previous = [_time for _time, target in transitions.items() if _time < current_datetime][-1]
    target = float(transitions[previous])
    return Target(transition=previous, target=target)


def get_next(transitions, current_datetime) -> Target:
    next = [_time for _time, target in transitions.items() if _time > current_datetime][1]
    target = float(transitions[next])
    return Target(transition=next, target=target)


def get_time_target() -> float:
    current_datetime = datetime.now()
    transitions = parse_data_to_transitions()
    current_target = get_target(transitions, current_datetime)
    next_target = get_next(transitions, current_datetime)
    # TODO: display

    return current_target.target


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
