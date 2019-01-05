from handlers.timing import Target


def write(string):
    print(string)


def _render_targets(current_target: Target, next_target: Target, current_temperate: float):
    write('Now: {0} {1}, \r\n'.format(current_target.transition.strftime("%a"), current_target.period)
          + 'Target: {0}°C\r\n'.format(current_target.target)
          + 'Actual: {0}°C\r\n'.format(current_temperate)
          + 'Next: {0} {1}°C'.format(next_target.transition.strftime("%H:%M"), next_target.target))
    # TODO: nice bit of lag when rendering, might need to shift the cursor


if True:
    from RPLCD.i2c import CharLCD

    lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
                  cols=20, rows=4, dotsize=8, charmap='A00',
                  auto_linebreaks=True, backlight_enabled=True)


    def write(string):
        lcd.write_string(string)


    def render_targets(current_target: Target, next_target: Target, current_temperate: float):
        lcd.cursor_pos = (0, 0)
        _render_targets(current_target, next_target, current_temperate)
else:  # testing locally, need to handle better
    def render_targets(current_target: Target, next_target: Target, current_temperate: float):
        _render_targets(current_target, next_target, current_temperate)

    # lcd.backlight_enabled = False
# lcd.backlight_enabled = True
