days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
periods = ["Wake Up", "Leave", "Home", "Sleep"]
init_day = {
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


def get_initial_data() -> list:
    new_data = []
    for day in days:
        new_periods = []
        for period in periods:
            new_periods.append({
                "period_name": period,
                "target": init_day[period]["target"],
                "time": init_day[period]["time"]
            })
        new_data.append({
            "day": day,
            "periods": new_periods
        })
    return new_data
