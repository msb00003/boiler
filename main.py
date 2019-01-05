from tornado.ioloop import PeriodicCallback, IOLoop
from tornado.web import Application

from handlers.timing import TimingHandler, get_targets
from hardware.boiler import set_boiler_high, set_boiler_low
from hardware.display import render_targets
from hardware.temperature import get_current_temperature


def get_target():
    current_target, next_target = get_targets()
    current_temperate = get_current_temperature()

    render_targets(current_target, next_target, current_temperate)
    if current_target.target > current_temperate:
        set_boiler_high()
    else:
        set_boiler_low()
    print(current_target.target, current_temperate)


def make_app():
    PeriodicCallback(get_target, 1000).start()
    return Application([
        (r"/", TimingHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(80)
    IOLoop.current().start()
