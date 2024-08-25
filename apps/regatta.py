# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2024 Christian Mäder
"""Regatta Application
~~~~~~~~~~~~~~~~~~~~

An application to track the start of a regatta.

"""

import wasp
import fonts
import time
import widgets
import math
from micropython import const

# > tools/rle_encoder.py res/icons/regatta_icon.png
# 2-bit RLE, 96x64, generated from res/icons/regatta_icon.png, 1301 bytes
icon = (
    b'\x02'
    b'`@'
    b'1@\xfcA\x80\xac\x81\x81\xc0\xeb\xc1@\xdbAA\x80'
    b'\xff\x81\xc0\xfd\xc1@\xfcA?\x18\x80\xfe\x81\xc0\xfb\xc1'
    b'@\xf3A\x80\xc9\x81\x81\xc0\xd0\xc1\xc1@\xfbA\x80\xac'
    b'\x81\x81\xc0\xeb\xc1@\xdbA\x80\xfc\x81?\x14\xc0V\xc1'
    b'@\xd0A\x80\xb4\x81\x81\x81\x81\xc0\xbb\xc1\xc1\xc1@\xc2'
    b'A\x80\xc9\x81\xc0\xd7\xc1@\xffA?\x14\x80\xdb\x81\xc0'
    b'\xf7\xc1@\xb4AG\x80\xbb\x81\xc0\xfb\xc1@\xfcA?'
    b'\x14\x80\x81\x81\xc0\xc9\xc1@\xb4AG\x80\xc2\x81\xc0\xfb'
    b'\xc1\x01?\x14@\xebA\x80\xc9\x81\xc0\xb4\xc8@\xc2A'
    b'\x80\xac\x81\x01?\x14\xc0\xfb\xc1A@\xb4H\x80\xc9\x81'
    b'\xc0\xeb\xc1\x01?\x14@\xfbA\x80\xbb\x81\xc0\xb4\xc8@'
    b'\xc9A\x80\x81\x81\x01?\x13\xc0\xfe\xc1@\xfbA\x80\xb4'
    b'\x89\xc0\xf7\xc1@\x81A?\x14\x80\xdb\x81\xc0\xd0\xc1@'
    b'\xb4I\xc1\x80V\x81?\x14\xc0\xeb\xc1@\xc9A\x80\xb4'
    b'\x89\xc0\xfb\xc1@\xfdA?\x14\x80\xac\x81\xc0\xc2\xc1@'
    b'\xb4H\x80\xbb\x81\xc0\xfb\xc1\x01?\x13@\xfcA\x80\xac'
    b'\x81\xc0\xbb\xc1@\xb4H\x80\xf3\x81\xc0\xfb\xc1?\x14@'
    b'\xfdA\xc1\x80\xbb\x81\xc0\xb4\xc8@\xf7A\x80\xeb\x81?'
    b'\x14\xc0\xff\xc1@\xd0A\x80\xbb\x81\xc0\xb4\xc8A@\xdb'
    b'A?\x14\x80V\x81\xc0\xd0\xc1@\xb4AGA\xc1\x80'
    b'\xfe\x81?\x14\xc0\xdb\xc1@\xf7A\x80\xbb\x81\xc0\xb4\xc7'
    b'\x81@\xfbA\x80\xfc\x81?\x14\xc0\xdb\xc1AA@\xd0'
    b'AA\x80\xc9\x81\xc0\xc2\xc1@\xbbA\x80\xb4\x82\xc1\xc0'
    b'\xac\xc1\x01?\x14\x01\x01@+A\x80V\x81\xc0\x81\xc1'
    b'@\xfbAAAA\x80\xd0\x81\x81\xc0\xeb\xc1\x01?\x18'
    b'@+A\x80\xfb\x81\xc0\xfc\xc1\xc1@\xffA\x80\xdb\x81'
    b'\xc0\x81\xc1@VA\x01?\x18\x80\xff\x81\xc0\xac\xc1@'
    b'\xfcA?\x1e\x80\xdb\x81\xc0\xeb\xc1\x01?\x1e\x81\xc1\x01'
    b'?\x1e\xc1@\x81A?\x1f\x80\xac\x81\xc0\xdb\xc1?\x1f'
    b'@\xfbA\x80\xfd\x81?\x1e\x81A?\x1f\xc1A?\x1f'
    b'\xc0\xeb\xc1\xc1?\x1f@\xacA\x80V\x81?\x1e\xc0\xfc'
    b'\xc1@\xfbA\x80\xfd\x81?\x07\x02\x01\x14\x81\xc0\xac\xc1'
    b'@\xfcA?\x07\x80\xdb\x81\xc0\xeb\xc1@\x81AA\x81'
    b'\x80V\x81\xc0\xfd\xc1@\xfcA\x0f\x81\x80\xac\x81A?'
    b'\x06\xc0+\xc1@\xe7A\x80\xf3\x81\xc0\xc9\xc1\xc1@\xf7'
    b'A\x80\xd0\x81\xc0\xfb\xc1\xc1\xc1@\xacA\x80\xeb\x81\xc0'
    b'\xdb\xc1@\xfeA\x80+\x81\xc0\xfc\xc1\x01\x01\x01\x01\x04'
    b'@\xdbA\x80\xeb\x81\x01?\x06\xc0V\xc1@\x9eA\x80'
    b'\xb4\x86\xc0\xbb\xc1@\xc2A\x80\xf3\x81\xc0\xf7\xc1@\xd0'
    b'AAA\x80\xfb\x81\xc0\xac\xc1@\xebAA\x80\x81\x81'
    b'\x81\xc0\xdb\xc1@\xffA\x80\xfd\x81\xc0\x81\xc1@\xebA'
    b'?\x07\xc1\x80\xbb\x81\xc0\xb4\xcb\xc1\x81\x81@\xc2AA'
    b'\x80\xf3\x81\xc0\xc9\xc1\xc1@\xd0A\x80\xfb\x81\x81\x81\x81'
    b'\xc0\xac\xc1@\x81A\x80V\x81\xc0\xfe\xc1@\xfcAA'
    b'\x01\x01\x01\x01;\x01\x80\xeb\x81\xc0\xb4\xc1\xd6@\xbbA'
    b'\x80\xc2\x81\xc0\xc9\xc1@\xd0AAAAA\x80\xac\x81'
    b'\xc0\xeb\xc1\xc1@\x81AA\x80\xdb\x81\xc0\xfe\xc1@\xfc'
    b'A7A\x80\xac\x81\xc0\xb4\xdc\xc1@\xbbAA\x80\xc2'
    b'\x81\xc0\xf3\xc1@\xc9AA\x80\xf7\x81\xc0\xd0\xc1@\xfb'
    b'AAAA\x80\xeb\x81\xc0\xdb\xc1@VA\x80\xfd\x81'
    b'\xc0\xfc\xc10@\xfeA\x80\xf7\x81\xc0\xb4\xe6@\xbbA'
    b'\x80\xc2\x81\xc0\xf3\xc1@\xc9A\x80\xd0\x81\x81\x81\x81\xc0'
    b'\xfe\xc1/@\xdbA\x80\xc9\x81\xc0\xb4\xeb\xc1@\xbbA'
    b'A\x80\xdb\x81.\x01\xc0\xeb\xc1@\xc9A\x80\xb4\xad\xc0'
    b'\xbb\xc1@\xebA.\x01A\x80\xc2\x81\xc0\xb4\xed@\xbb'
    b'A\x80\xac\x81.\xc0\xfc\xc1\x81@\xc2A\x80\xb4\xadA'
    b'\xc0\xac\xc1.@\xfcA\xc1\x80\xc2\x81\xc0\xb4\xed@\xc9'
    b'A\x80\xeb\x81*\x01\x03\xc0+\xc1@\xd0A\x80\xbb\x81'
    b'\xc0\xb4\xed@\xc9A\x80\x81\x81\x01\x01,\xc0\xfd\xc1@'
    b'\xd0A\x80\xbb\x81\xc0\xb4\xec\xc1@\xc9A\x80\xdb\x81\x01'
    b'\xc0$\xc1,@\xffA\x80\xd0\x81\xc0\xb4\xc1\xec\xc1@'
    b'\xf7A\x80\xdb\x81\x01\xc0$\xc1,\x81@\xd0A\x80\xb4'
    b'\x81\xac\x81A\xc0V\xc1.@\x81A\x80\xd0\x81\xc0\xb4'
    b'\xed\xc1@\xfbA\x80\xfe\x81.\xc0\xeb\xc1@\xc9A\x80'
    b'\xb4\xad\xc0\xbb\xc1@\xfbA\x80+\x81.A\xc0\xc2\xc1'
    b'@\xb4m\x80\xbb\x81\xc0\xfb\xc1\x01.\xc1\x81m@\xc2'
    b'A\xc1.\x80\xfc\x81\xc1\xc0\xb4\xc1\xed@\xc9A\x80\xac'
    b'\x81.\xc0\xfe\xc1@\xfbA\x80\xb4\xae\xc0\xd0\xc1@\x81'
    b'A.\x80\xdb\x81\xc1\xc0\xb4\xee@\xfbA\x80V\x81.'
    b'\xc0\x81\xc1@\xf7A\x80\xb4\xad\x81\xc0\xfb\xc1@\xfdA'
    b'-\x01\x80\xeb\x81\xc0\xc9\xc1@\xb4m\x80\xbb\x81\xc0\xfb'
    b'\xc1\x01-\x01@\xebA\x80\xc2\x81\xc0\xb4\xed\x81@\xfb'
    b'A.\x01\x80\xac\x81\xc0\xc2\xc1@\xb4m\xc1\x81,\x80'
    b'\xfc\x81\xc0\x81\xc1\xc1@\xfbA\x80\xc2\x81\xc0\xbb\xd3\xc1'
    b'\xc1@\xb4ACA\xc1\xd2\x80\xc9\x81\xc0\xac\xc1@\xdb'
    b'BA\x80\xfd\x81(\x81\xc1\xc1\xc1\xc0\xeb\xd4\xc1@\xf7'
    b'A\x80\xbb\x81\xc0\xb4\xc3@\xc2A\x80\xac\x81\xc0\xeb\xd2'
    b'\xc1\x81\x82\x81@VA?\x01\x80\xfd\x81\xc0\xfb\xc1@'
    b'\xbbA\x80\xb4\x82\x81\xc0\xd0\xc1@\x81A\x01\x12\x04\x80'
    b'$\x81?\x02A\xc1\xc0\xc9\xc1@\xc2A\x80\xd0\x81\xc0'
    b'\xac\xc1@\xfcA?\x1b\x80\xdb\x81\xc1\xc0\xfb\xc1@\x81'
    b'A/'
)

_STOPPED = const(0)
_COUNTDOWN = const(1)
_COUNTUP = const(2)

_BUTTON_Y = const(180)

_PRE_10S = 0xf800  # rgb565
_PRE_30S = 0xfca0  # rgb565
_PRE_60S = 0x07df  # rgb565
_POST_60S = 0x07c0  # rgb565


class RegattaApp():
    """Allows the user to set a regatta timer.
    """
    NAME = 'Regatta'
    ICON = icon

    def __init__(self):
        """Initialize the application."""
        self.hours = widgets.Spinner(50, 60, 0, 9, 1)
        self.minutes = widgets.Spinner(130, 60, 0, 59, 2)

        self.zero_time = None
        self.start_time = None

        self.current_zero_alarm_time = None
        self.current_minute_alarm_time = None

        self.button_down_time = None

        self.minutes.value = 5
        self.state = _STOPPED

        self.bg_cleared = False

    def foreground(self):
        """Activate the application."""
        self._draw()
        wasp.system.request_event(wasp.EventMask.TOUCH)
        wasp.system.request_event(wasp.EventMask.BUTTON)
        wasp.system.request_tick(500)

    def press(self, button, is_down):
        """Button press event"""
        if self.state == _STOPPED:
            return True

        if not button == wasp.EventType.HOME:
            return True

        now = wasp.watch.rtc.time()
        if is_down:
            self.button_down_time = now
            return False

        if not self.button_down_time and self.state == _COUNTDOWN:
            # only quick press, possibly accidental
            return False

        hold_time = now - self.button_down_time
        if hold_time < 0.2 and self.state == _COUNTDOWN:
            # only quick press, possibly accidental
            pass
        elif hold_time < 3 and self.state == _COUNTDOWN:
            self._sync()
            self.button_down_time = False
            return False
        elif hold_time < 3 and self.state == _COUNTUP:
            # not holding button down, possibly accidental
            pass
        else:
            print("stop")
            self._stop()

        self.button_down_time = False

    def background(self):
        """De-activate the application."""

    def tick(self, ticks):
        """Notify the application that its periodic tick is due."""
        if self.state == _COUNTDOWN:
            wasp.system.keep_awake()
        self._update()

    def touch(self, event):
        """Notify the application of a touchscreen touch event."""
        if self.state == _STOPPED:
            if self.minutes.touch(event) or self.hours.touch(event):
                pass
            else:
                y = event[2]
                if y >= _BUTTON_Y:
                    self._start()
        else:
            y = event[2]
            if y >= _BUTTON_Y:
                self._stop()

    def _sync(self):
        if self.state != _COUNTDOWN:
            return

        tss = self._time_since_start()
        modulo = tss % 60

        if modulo < 20:
            modifier = modulo
        else:
            modifier = -(60 - modulo)

        self.start_time = self.start_time + modifier
        self.zero_time = self.zero_time + modifier

        ttz = self._time_to_zero()
        if ttz > 0:
            self._minute_alarm()
            self._reset_zero_alarm()
        else:
            self.state = _COUNTUP
            self._zero_alarm()
            self._reset_minute_alarm()

        self._update()

    def _start(self):
        now = wasp.watch.rtc.time()
        self.start_time = now

        minutes = self.minutes.value * 60
        hours = self.hours.value * 60 * 60
        if minutes > 0 or hours > 0:
            self.state = _COUNTDOWN
            self.zero_time = now + minutes + hours
        else:
            self.state = _COUNTUP
            self.zero_time = now

        self._reset_alarms()
        self._draw()

    def _reset_alarms(self):
        self._reset_zero_alarm()
        self._reset_minute_alarm()

    def _reset_zero_alarm(self):
        if self.current_zero_alarm_time:
            wasp.system.cancel_alarm(self.current_zero_alarm_time, self._zero_alarm)
            self.current_zero_alarm_time = None

        if self.state == _COUNTDOWN:
            self.current_zero_alarm_time = self.zero_time
            wasp.system.set_alarm(self.current_zero_alarm_time, self._zero_alarm)

    def _reset_minute_alarm(self):
        if self.current_minute_alarm_time:
            wasp.system.cancel_alarm(self.current_minute_alarm_time, self._minute_alarm)
            self.current_minute_alarm_time = None

        if self.state != _COUNTDOWN:
            return

        now = wasp.watch.rtc.time()
        ttz = self.zero_time - now
        if not ttz > 60:
            return

        next_alarm_delay = (ttz % 60)
        next_minute_alarm_time = now + next_alarm_delay
        if next_minute_alarm_time > self.zero_time:
            return

        self.current_minute_alarm_time = next_minute_alarm_time
        wasp.system.set_alarm(self.current_minute_alarm_time, self._minute_alarm)

    def _stop(self):
        self.state = _STOPPED
        wasp.system.cancel_alarm(self.current_zero_alarm_time, self._zero_alarm)
        wasp.system.cancel_alarm(self.current_minute_alarm_time, self._minute_alarm)
        self._draw()

    def _draw(self):
        """Draw the display from scratch."""
        draw = wasp.watch.drawable
        draw.fill()
        sbar = wasp.system.bar
        sbar.clock = True
        sbar.draw()
        self.bg_cleared = False

        if self.state == _STOPPED:
            draw.set_font(fonts.sans36)
            draw.string(':', 110, 120 - 18, width=20)

            self.minutes.draw()
            self.hours.draw()

            self._draw_play(110, _BUTTON_Y)
        else:
            self._draw_stop(100, _BUTTON_Y)
            self._update()

    def _update(self):
        wasp.system.bar.update()
        draw = wasp.watch.drawable
        if self.state != _STOPPED:
            ttz = math.floor(self._time_to_zero())
            s = abs(ttz)

            if s > const(60 * 60):
                l = str(s // 60 // 60)
                r = str(s // 60) % 60
            else:
                l = str(s // 60)
                r = str(s % 60)

            if len(l) < 2:
                l = '0' + l
            if len(r) < 2:
                r = '0' + r

            draw.set_font(fonts.sans36)
            y = 120 - fonts.sans36.height() // 2

            indicator_s = const(20)
            indicator_y = y + (fonts.sans36.height() - indicator_s) // 2
            indicator_x = const((46 - indicator_s) // 2)
            if ttz > 0:
                self._draw_down(indicator_x, indicator_y, s=indicator_s)
            elif ttz == 0:
                draw.fill(bg=0, x=indicator_x, y=indicator_y, w=indicator_s, h=indicator_s)
            elif ttz < 0:
                self._draw_up(wasp.watch.display.width - indicator_s - indicator_x, indicator_y, s=indicator_s)

            if -60 < ttz <= 0:
                draw.set_color(_POST_60S)
            elif s <= 10:
                draw.set_color(_PRE_10S)
            elif s <= 30:
                draw.set_color(_PRE_30S)
            elif s <= 60:
                draw.set_color(_PRE_60S)

            if s >= 60:
                draw.string(l, 46, y, width=64)
                draw.string(':', 110, y, width=20)
                draw.string(r, 130, y, width=64)
            else:
                if s == 59:
                    draw.fill(bg=0, x=46, y=y, h=fonts.sans36.height())
                draw.string(r, 80, y, width=80)

            draw.reset()

    def _draw_play(self, x, y, s=40):
        draw = wasp.watch.drawable
        for i in range(0, s // 2):
            draw.fill(0xffff, x + i, y + i, 1, s - 2 * i)

    def _draw_up(self, x, y, s=40):
        draw = wasp.watch.drawable
        for i in range(0, s):
            draw.fill(0xffff, x + i // 2, y + s - i, s - i, 1)

    def _draw_down(self, x, y, s=40):
        draw = wasp.watch.drawable
        for i in range(0, s):
            draw.fill(0xffff, x + i // 2, y + i, s - i, 1)

    def _draw_stop(self, x, y, s=40):
        wasp.watch.drawable.fill(0xffff, x, y, s, s)

    def _minute_alarm(self):
        wasp.watch.vibrator.pulse(duty=50, ms=200)
        self._reset_minute_alarm()
        wasp.system.wake()
        wasp.system.switch(self)

    def _zero_alarm(self):
        self.state = _COUNTUP
        wasp.watch.vibrator.pulse(duty=50, ms=500)
        wasp.system.wake()
        wasp.system.switch(self)

    def _time_since_start(self):
        now = wasp.watch.rtc.time()
        return now - self.start_time

    def _time_to_zero(self):
        now = wasp.watch.rtc.time()
        return self.zero_time - now
