from tornado.ioloop import PeriodicCallback, IOLoop
from tornado.web import Application

from handlers.timing import TimingHandler, get_time_target
from hardware.boiler import set_boiler_high, set_boiler_low
from hardware.temperature import get_current_temperature

def get_target():
    temp_target = get_time_target()
    current_temperate = get_current_temperature()
    if temp_target > current_temperate:
        set_boiler_high()
    else:
        set_boiler_low()


def make_app():
    PeriodicCallback(get_target, 1000).start()
    return Application([
        (r"/", TimingHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8082)
    IOLoop.current().start()
