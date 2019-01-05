from handlers.timing import Target

if True:
    from RPLCD.i2c import CharLCD

    lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
                  cols=20, rows=4, dotsize=8, charmap='A00',
                  auto_linebreaks=True, backlight_enabled=True)


    def render_targets(current_target: Target, next_target: Target, current_temperate: float):
        lcd.clear()
        lcd.write_string(f'Now: {current_target.transition.strftime("%a")} {current_target.period}\r\n')
        lcd.write_string(f'Target: {current_target.target}°C\r\n')
        lcd.write_string(f'Actual: {current_temperate}°C\r\n')
        lcd.write_string(f'Next: {next_target.transition.strftime("%H:%M")} {next_target.target}°C')
else:  # testing locally, need to handle better
    def render_targets(_: Target, __: Target):
        pass

# lcd.backlight_enabled = False
# lcd.backlight_enabled = True
