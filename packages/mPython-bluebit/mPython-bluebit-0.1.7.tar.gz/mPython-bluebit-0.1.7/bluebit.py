# The MIT License (MIT)

# Copyright (c) 2018, Tangliufeng. LabPlus

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
| blue:bit modules library for mPython. 
| more about with bluebit info browse http://wiki.labplus.cn/index.php?title=Bluebit
"""
from mpython import i2c, sleep_ms, MPythonPin, PinMode
from micropython import const
from machine import UART
import framebuf
from machine import UART
import ubinascii
import ustruct
import math


class NTC(object):
    """NTC 模块

    :param pin: 掌控板引脚号,如使用P0,pin=0.
    """

    def __init__(self, pin):
        self.pin = pin

    def getTemper(self):
        """
        获取温度

        :return: 温度,单位摄氏度
        """
        _pin = MPythonPin(self.pin, PinMode.ANALOG)
        val = _pin.read_analog()
        return 1 / (math.log(4095 / val - 1) / 3935 + 1 / 298) - 273


class LM35(object):
    """LM35 模块

    :param pin: 掌控板引脚号,如使用P0,pin=0.
    """

    def __init__(self, pin):
        self.pin = pin

    def getTemper(self):
        """
        获取温度

        :return: 温度,单位摄氏度
        """
        _pin = MPythonPin(self.pin, PinMode.ANALOG)
        val = _pin.read_analog()
        return val / 4 * (3 / 10.24)


class joyButton(object):
    """
    四按键模块 

    :param pin: 掌控板引脚号,如使用P0,pin=0.
    """

    def __init__(self, pin):
        self.pin = pin

    def getVal(self):
        """
        获取按键

        :return: 返回按键,值可以是'A','B','C','D',无按键按下'None'.
        """
        _pin = MPythonPin(self.pin, PinMode.ANALOG)
        val = _pin.read_analog()
        btn = None
        if val < 100:
            btn = 'A'
        elif val > 600 and val < 1023:
            btn = 'B'
        elif val > 1700 and val < 2048:
            btn = 'C'
        elif val > 2700 and val < 3200:
            btn = 'D'
        return btn


class SHT20(object):
    """
    温湿度模块SHT20控制类

    :param i2c: I2C实例对象,默认i2c=i2c.
    """

    def __init__(self, i2c=i2c):
        self.i2c = i2c

    def temperature(self):
        """
        获取温度

        :return: 温度,单位摄氏度
        """
        self.i2c.writeto(0x40, b'\xf3')
        sleep_ms(70)
        t = i2c.readfrom(0x40, 2)
        return -46.86 + 175.72 * (t[0] * 256 + t[1]) / 65535

    def humidity(self):
        """
        获取湿度

        :return: 湿度,单位%
        """
        self.i2c.writeto(0x40, b'\xf5')
        sleep_ms(25)
        t = i2c.readfrom(0x40, 2)
        return -6 + 125 * (t[0] * 256 + t[1]) / 65535


class Color(object):
    """
    颜色模块控制类

    :param i2c: I2C实例对象,默认i2c=i2c.
    """

    def __init__(self, i2c=i2c):
        self.i2c = i2c

    def getRGB(self):
        """
        获取RGB值

        :return: 返回RGB三元组,(r,g,b)
        """
        color = [0, 0, 0]
        self.i2c.writeto(0x0a, bytearray([1]))
        sleep_ms(100)
        self.i2c.writeto(0x0a, bytearray([2]))
        state = self.i2c.readfrom(0x0a, 1)
        if state[0] == 3:
            self.i2c.writeto(0x0a, bytearray([3]))
            c = self.i2c.readfrom(0x0a, 6)
            color[0] = c[5] * 256 + c[4]  # color R
            color[1] = c[1] * 256 + c[0]  # color G
            color[2] = c[3] * 256 + c[2]  # color B
            maxColor = max(color[0], color[1], color[2])
            if maxColor > 255:
                scale = 255 / maxColor
                color[0] = int(color[0] * scale)
                color[1] = int(color[1] * scale)
                color[2] = int(color[2] * scale)
        return color

    def getHSV(self):
        """
        获取HSV值

        :return: 返回HSV三元组,(h,s,v)
        """
        rgb = self.getRGB()
        r, g, b = rgb[0], rgb[1], rgb[2]
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx - mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / df) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / df) + 120) % 360
        elif mx == b:
            h = (60 * ((r - g) / df) + 240) % 360
        if mx == 0:
            s = 0
        else:
            s = df / mx
        v = mx
        return round(h, 1), round(s, 1), round(v, 1)


class AmbientLight(object):
    """
    数字光线模块控制类

    :param i2c: I2C实例对象,默认i2c=i2c.
    """

    def __init__(self, i2c=i2c):
        self.i2c = i2c

    def getLight(self):
        """
        获取光线值

        :return: 返回光线值,单位lux
        """
        self.i2c.writeto(0x23, bytearray([0x10]))
        sleep_ms(120)
        t = self.i2c.readfrom(0x23, 2)
        sleep_ms(10)
        return int((t[0] * 256 + t[1]) / 1.2)


class Ultrasonic(object):
    """
    超声波模块控制类

    :param i2c: I2C实例对象,默认i2c=i2c.
    """

    def __init__(self, i2c=i2c):
        self.i2c = i2c

    def distance(self):
        """
        获取超声波测距

        :return: 返回测距,单位cm
        """
        self.i2c.writeto(0x0b, bytearray([1]))
        sleep_ms(2)
        temp = self.i2c.readfrom(0x0b, 2)
        distanceCM = (temp[0] + temp[1] * 256) / 10
        return distanceCM


class SEGdisplay(object):
    """
    4段数码管模块tm1650控制类

    :param i2c: I2C实例对象,默认i2c=i2c.
    """

    def __init__(self, i2c=i2c):
        self.i2c = i2c
        self.i2c.writeto(0x24, bytearray([0x01]))
        self._TubeTab = [
            0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F, 0x77,
            0x7C, 0x39, 0x5E, 0x79, 0x71, 0x00, 0x40
        ]

    def _uint(self, x):
        """ display unsigned int number """
        charTemp = [0, 0, 0, 0]
        x = (x if x < 10000 else 9999)
        charTemp[3] = x % 10
        charTemp[2] = (x // 10) % 10
        charTemp[1] = (x // 100) % 10
        charTemp[0] = (x // 1000) % 10
        if x < 1000:
            charTemp[0] = 0x10
            if x < 100:
                charTemp[1] = 0x10
            if x < 10:
                charTemp[2] = 0x10
        for i in range(0, 4):
            self.i2c.writeto(0x34 + i, bytearray([self._TubeTab[charTemp[i]]]))

    def numbers(self, x):
        """
        数字显示-999~9999

        :param int x: 数字,范围-999~9999
        """
        x = round(x)
        if x >= 0:
            self._uint(x)
        else:
            temp = (x if x > -999 else -999)
            temp = abs(temp)
            self._uint(temp)
            if temp < 10:
                self.i2c.writeto(0x36, bytearray([self._TubeTab[0x11]]))
            elif temp < 100:
                self.i2c.writeto(0x35, bytearray([self._TubeTab[0x11]]))
            elif temp < 1000:
                self.i2c.writeto(0x34, bytearray([self._TubeTab[0x11]]))

    def Clear(self):
        """
        数码管清屏
        """

        for i in range(0, 4):
            self.i2c.writeto(0x34 + i, bytearray([self._TubeTab[0x10]]))


_HT16K33_BLINK_CMD = const(0x80)
_HT16K33_BLINK_DISPLAYON = const(0x01)
_HT16K33_CMD_BRIGHTNESS = const(0xE0)
_HT16K33_OSCILATOR_ON = const(0x21)
_HT16K33_ADDR = const(0x70)


class HT16K33:
    def __init__(self, i2c=i2c):
        self.i2c = i2c
        self.address = _HT16K33_ADDR
        self._temp = bytearray(1)

        self.buffer = bytearray(16)
        self._write_cmd(_HT16K33_OSCILATOR_ON)
        self.blink_rate(0)
        self.brightness(15)

    def _write_cmd(self, byte):
        self._temp[0] = byte
        self.i2c.writeto(self.address, self._temp)

    def blink_rate(self, rate=None):
        """
        设置像素点闪烁率

        :param rate: 闪烁间隔时间,单位秒.默认None,常亮.
        """

        if rate is None:
            return self._blink_rate
        rate = rate & 0x03
        self._blink_rate = rate
        self._write_cmd(_HT16K33_BLINK_CMD | _HT16K33_BLINK_DISPLAYON
                        | rate << 1)

    def brightness(self, brightness):
        """
        设置像素点亮度

        :param brightness: 亮度级别,范围0~15.
        """
        if brightness < 0 or brightness > 15:
            raise ValueError("out of range,the brightness in 0~15")
        brightness = brightness & 0x0F
        self._brightness = brightness
        self._write_cmd(_HT16K33_CMD_BRIGHTNESS | brightness)

    def show(self):
        """
        显示生效
        """
        self.i2c.writeto_mem(self.address, 0x00, self.buffer)

    def fill(self, color):
        """
        填充所有

        :param color: 1亮;0灭
        """
        fill = 0xff if color else 0x00
        for i in range(16):
            self.buffer[i] = fill


class HT16K33Matrix(HT16K33):
    def __init__(self, i2c=i2c):
        super().__init__(i2c)

        self._fb_buffer = bytearray(self.WIDTH * self.HEIGHT * self.FB_BPP //
                                    8)
        self.framebuffer = framebuf.FrameBuffer(self._fb_buffer, self.WIDTH,
                                                self.HEIGHT, self.FORMAT)

        self.framebuffer.fill(0)
        self.pixel = self.framebuffer.pixel
        self.fill = self.framebuffer.fill
        self.text = self.framebuffer.text
        self.fill(0)
        self.show()

    def show(self):
        self._copy_buf()
        super().show()

    def bitmap(self, bitmap):
        for j in range(self.HEIGHT):
            for i in range(self.WIDTH):
                if bitmap[j] >> (7 - i) & 0x01:
                    self.pixel(i, j, 1)


class Matrix(HT16K33Matrix):
    """
    8x8点阵模块控制类

    :param i2c: I2C实例对象,默认i2c=i2c.
    """
    WIDTH = 8
    HEIGHT = 8
    FORMAT = framebuf.MONO_HLSB
    FB_BPP = 1

    def _copy_buf(self):
        for y in range(8):
            b = 0x00
            for i in range(8):

                b = ((self._fb_buffer[y] >> i) & 0x01) | b
                if i < 7:
                    b = b << 1

            self.buffer[y * 2] = b

    # commands
    _LCD_CLEARDISPLAY = const(0x01)
    _LCD_RETURNHOME = const(0x02)
    _LCD_ENTRYMODESET = const(0x04)
    _LCD_DISPLAYCONTROL = const(0x08)
    _LCD_CURSORSHIFT = const(0x10)
    _LCD_FUNCTIONSET = const(0x20)
    _LCD_SETCGRAMADDR = const(0x40)
    _LCD_SETDDRAMADDR = const(0x80)
    # flags for display entry mode
    _LCD_ENTRYRIGHT = const(0x00)
    _LCD_ENTRYLEFT = const(0x02)
    _LCD_ENTRYSHIFTINCREMENT = const(0x01)
    _LCD_ENTRYSHIFTDECREMENT = const(0x00)
    #flags for display on/off control
    _LCD_DISPLAYON = const(0x04)
    _LCD_DISPLAYOFF = const(0x00)
    _LCD_CURSORON = const(0x02)
    _LCD_CURSOROFF = const(0x00)
    _LCD_BLINKON = const(0x01)
    _LCD_BLINKOFF = const(0x00)
    #flags for display/cursor shift
    _LCD_DISPLAYMOVE = const(0x08)
    _LCD_CURSORMOVE = const(0x00)
    _LCD_MOVERIGHT = const(0x04)
    _LCD_MOVELEFT = const(0x00)
    #flags for function set
    _LCD_8BITMODE = const(0x10)
    _LCD_4BITMODE = const(0x00)
    _LCD_2LINE = const(0x08)
    _LCD_1LINE = const(0x00)
    _LCD_5x10DOTS = const(0x04)
    _LCD_5x8DOTS = const(0x00)


class LCD1602(object):
    """
    LCD1602模块控制类

    :param i2c: I2C实例对象,默认i2c=i2c.
    """

    LEFT_TO_RIGHT = const(0)
    """文本方向常量-从左到右"""

    RIGHT_TO_LEFT = const(1)
    """文本方向常量-从右到左"""

    def __init__(self, i2c=i2c):
        self.i2c = i2c
        self._displayfunction = _LCD_8BITMODE | _LCD_2LINE | _LCD_5x8DOTS
        self._row_offsets = [0, 0, 0, 0]
        self._displaymode = _LCD_ENTRYLEFT | _LCD_ENTRYSHIFTDECREMENT
        self._displaycontrol = _LCD_DISPLAYON | _LCD_CURSOROFF | _LCD_BLINKOFF
        self.Init()

    def Init(self):
        """
        1602初始化函数
        """
        self._setRowOffsets(0x00, 0x40, (0x00 + 16), (0x40 + 16))
        sleep_ms(50)
        self.display(True)
        self.Clear()
        self._sendCommand(_LCD_ENTRYMODESET | self._displaymode)
        self.Cursor(1)
        self.Blink(1)

    def Print(self, str):
        """
        打印字符串

        :param str str: 显示字符串,只支持英文.
        """
        for c in str:
            self._sendCharacter(ord(c))

    def Clear(self):
        """清屏"""
        self._sendCommand(_LCD_CLEARDISPLAY)
        sleep_ms(2)

    def setCursor(self, col, row):
        """
        设置光标位置

        :param col: 列,1~16
        :param col: 行,1~2

        """
        if row >= 2:
            row = 1
        # Clamp to last column of display
        if col >= 16:
            col = 15
        # Set location
        self._sendCommand(_LCD_SETDDRAMADDR | (col + self._row_offsets[row]))

    def Cursor(self, show):
        """
        光标显示使能

        :param bool show: True or False
        """
        if not show:
            self._displaycontrol &= ~_LCD_CURSORON

        else:
            self._displaycontrol |= _LCD_CURSORON
        self._sendCommand(_LCD_DISPLAYCONTROL | self._displaycontrol)

    def Blink(self, blink):
        """
        光标闪烁使能

        :param bool blink: True or False
        """
        if not blink:
            self._displaycontrol &= ~_LCD_BLINKON

        else:
            self._displaycontrol |= _LCD_BLINKON
        self._sendCommand(_LCD_DISPLAYCONTROL | self._displaycontrol)

    def display(self, enable):
        """
        显示使能

        :param bool enable: True or False
        """
        if enable:
            self._displaycontrol |= _LCD_DISPLAYON
        else:
            self._displaycontrol &= ~_LCD_DISPLAYON
        self._sendCommand(_LCD_DISPLAYCONTROL | self._displaycontrol)

    def move_left(self):
        """
        左滚动显示
        """
        self._sendCommand(_LCD_CURSORSHIFT | _LCD_DISPLAYMOVE | _LCD_MOVELEFT)

    def move_right(self):
        """
        右滚动显示
        """
        self._sendCommand(_LCD_CURSORSHIFT | _LCD_DISPLAYMOVE | _LCD_MOVERIGHT)

    @property
    def text_direction(self):
        """
        文本方向
        """
        return self._direction

    @text_direction.setter
    def text_direction(self, direction):
        self._direction = direction
        if direction == self.LEFT_TO_RIGHT:
            self._left_to_right()
        elif direction == self.RIGHT_TO_LEFT:
            self._right_to_left()

    # 字符串流从左到右
    def _left_to_right(self):
        self._displaymode |= _LCD_ENTRYLEFT
        self._sendCommand(_LCD_ENTRYMODESET | self._displaymode)

    # 字符串流从右到左
    def _right_to_left(self):
        self._displaymode &= ~_LCD_ENTRYLEFT
        self._sendCommand(_LCD_ENTRYMODESET | self._displaymode)

    def createChar(self, location, charmap=[]):
        """
        制作用户自定义
        Fill one of the first 8 CGRAM locations with custom characters.
        The location parameter should be between 0 and 7 and pattern should
        provide an array of 8 bytes containing the pattern. E.g. you can easily
        design your custom character at http://www.quinapalus.com/hd44780udg.html
        To show your custom character use

        :param location: integer in range(8) to store the created character
        :param ~bytes pattern: len(8) describes created character

        """
        _location = location & 0x7
        self._sendCommand(_LCD_SETCGRAMADDR | (_location << 3))
        for i in range(0, 8):
            self._sendCharacter(charmap[i])

    def Home(self):
        """光标返回屏幕原点"""
        self._sendCommand(_LCD_RETURNHOME)
        sleep_ms(2)

    # 非用户调用函数------------------------------------------------

    #设置行偏移
    def _setRowOffsets(self, row0, row1, row2, row3):
        self._row_offsets[0] = row0
        self._row_offsets[1] = row1
        self._row_offsets[2] = row2
        self._row_offsets[3] = row3

    def _sendCommand(self, cmd):
        command = bytearray([0x01, cmd])
        self.i2c.writeto(24, command)
        sleep_ms(1)

    def _sendCharacter(self, c):
        character = bytearray([0x02, c])
        self.i2c.writeto(24, character)
        sleep_ms(1)


class MIDI(object):
    """
    MIDI模块控制类

    :param i2c: I2C实例对象,默认i2c=i2c.
    """

    def __init__(self, tx):
        self.uart = UART(1, 31250, tx=tx)
        sleep_ms(30)
        self.uart.write(bytearray([0xb0, 0x78, 0x00]))
        sleep_ms(5)
        self.uart.write(bytearray([0xb0, 0x79, 0x7f]))
        sleep_ms(15)
        self.volume = 100

    @property
    def volume(self):
        """
        设置或返回音量
        """
        return self._vol

    @volume.setter
    def volume(self, vol):
        # range 0~127 volume
        self._vol = vol
        self.uart.write(bytearray([0xb0, 0x07, self._vol]))
        sleep_ms(10)

    @property
    def instrument(self):
        """
        设置或返回音色
        """
        return self._ins

    @instrument.setter
    def instrument(self, ins):
        self._ins = ins
        self.uart.write(bytearray([0xc0, self._ins]))
        sleep_ms(10)

    def note(self, note, on_off):
        """
        播放音符

        :param note: MIDI音符编码
        :param on_off: 音符播放或停止
        """
        if on_off == 1:
            self.uart.write(bytearray([0x90, note, 0x7f]))
        elif on_off == 0:
            self.uart.write(bytearray([0x80, note, 0x00]))
        sleep_ms(5)


class extIO(object):
    """
    引脚拓展模块控制类

    :param i2c: I2C实例对象,默认i2c=i2c.
    """

    OUTPUT = const(0)
    """引脚输出类型常量"""

    INPUT = const(1)
    """引脚输入类型常量"""

    def __init__(self, i2c):
        self.i2c = i2c

    def IOInit(self, pin, mode):
        """
        引脚初始化

        :param pin: 拓展引脚,0~7
        :param mode: 引脚模式输入或输出;OUTPUT,INPUT
        """
        self.i2c.writeto(0x20, bytearray([3]))
        mode_old = self.i2c.readfrom(0x20, 1)
        mode_new = 0
        if mode == self.INPUT:
            mode_new = mode_old[0] | (1 << pin)
        elif mode == self.OUTPUT:
            mode_new = mode_old[0] & (~(1 << pin))
        cfg = bytearray([0x03, mode_new])
        self.i2c.writeto(0x20, cfg)

    def readIO(self, pin):
        """
        读引脚

        :param pin: 拓展引脚,0~7
        """
        reg = bytearray([0])
        self.i2c.writeto(0x20, reg)
        dat = self.i2c.readfrom(0x20, 4)
        return (dat[0] >> pin) & 0x01

    def writeIO(self, pin, output):
        """
        写引脚

        :param pin: 拓展引脚,0~7
        :param output: 电平值;1 or 0
        """
        reg = bytearray([1])
        self.i2c.writeto(0x20, reg)
        stat_old = self.i2c.readfrom(0x20, 3)
        stat_new = 0
        if output == 1:
            stat_new = stat_old[0] | (1 << pin)
        elif output == 0:
            stat_new = stat_old[0] & (~(1 << pin))
        cfg = bytearray([0x01, stat_new])
        self.i2c.writeto(0x20, cfg)


class MP3(object):
    """
    MP3模块控制类

    :param i2c: I2C实例对象,默认i2c=i2c.
    """

    def __init__(self, tx):
        self.uart = UART(1, 9600, tx=tx)
        self.volume = 25

    def _cmdWrite(self, cmd):
        sum = 0
        for i in range(0, 6):
            sum += cmd[i]
        sum1 = ((0xFFFF - sum) + 1)
        sum_l = sum1 & 0xff
        sum_h = sum1 >> 8

        self.uart.write(bytearray([0x7E]))
        self.uart.write(cmd)
        self.uart.write(bytearray([sum_h]))
        self.uart.write(bytearray([sum_l]))
        self.uart.write(bytearray([0xEF]))
        sleep_ms(20)

    def play_song(self, num):
        """
        播放歌曲

        :param int num: 歌曲编号,类型为数字
        """
        var = bytearray([0xFF, 0x06, 0x03, 0x01, 0x00, num])
        self._cmdWrite(var)

    def play(self):
        """
        播放,用于暂停后的重新播放
        """
        var = bytearray([0xFF, 0x06, 0x0D, 0x01, 0x00, 0x00])
        self._cmdWrite(var)

    def playDir(self, dir, songNo):
        """
        播放指定文件夹指定歌曲

        :param int dir: 文件夹编号,类型数字
        :param int songNo: 歌曲编号,类型为数字
        """
        var = bytearray([0xFF, 0x06, 0x0F, 0x00, dir, songNo])
        self._cmdWrite(var)

    def playNext(self):
        """播下一首"""
        var = bytearray([0xFF, 0x06, 0x01, 0x00, 0x00, 0x00])
        self._cmdWrite(var)

    def playPrev(self):
        """播上一首"""
        var = bytearray([0xFF, 0x06, 0x02, 0x00, 0x00, 0x00])
        self._cmdWrite(var)

    def pause(self):
        """暂停播放"""
        var = bytearray([0xFF, 0x06, 0x0E, 0x01, 0x00, 0x00])
        self._cmdWrite(var)

    def stop(self):
        """停止播放"""
        var = bytearray([0xff, 0x06, 0x16, 0x00, 0x00, 0x00])
        self._cmdWrite(var)

    def volumeInc(self):
        """
        增加音量
        """
        self._vol += 1
        var = bytearray([0xFF, 0x06, 0x04, 0x00, 0x00, 0x00])
        self._cmdWrite(var)
        # 减小音量
    def volumeDec(self):
        """
        减小音量
        """
        self._vol -= 1
        var = bytearray([0xFF, 0x06, 0x05, 0x00, 0x00, 0x01])
        self._cmdWrite(var)

    def loop(self, songNo):
        """
        目录内指定序号歌曲循环播放

        :param int songNo: 歌曲编号,类型为数字
        """
        #
        var = bytearray([0xFF, 0x06, 0x08, 0x00, 0x00, songNo])
        self._cmdWrite(var)

    def loopDir(self, dir):
        """
        指定目录内循环播放

        :param int dir: 文件夹编号,类型数字
        """
        # 指定目录内循环播放
        var = bytearray([0xFF, 0x06, 0x17, 0x00, dir, 0x01])
        self._cmdWrite(var)

    def singleLoop(self, onOff):
        """
        单曲循环开关

        :param int onOff: 0:不循环  1：循环
        """
        if onOff:
            var = bytearray([0xFF, 0x06, 0x19, 0x00, 0x00, 0x00])
        else:
            var = bytearray([0xFF, 0x06, 0x19, 0x00, 0x00, 0x01])
        self._cmdWrite(var)

    @property
    def volume(self):
        """
        设置或返回音量设置,范围0~30
        """
        return self._vol

    @volume.setter
    def volume(self, vol):
        # set volume range 0~30
        self._vol = vol
        var = bytearray([0xFF, 0x06, 0x06, 0x00, 0x00, self._vol])
        self._cmdWrite(var)

    def resetDevice(self):
        """复位MP3"""
        var = bytearray([0xFF, 0x06, 0x0C, 0x00, 0x00, 0x00])
        self._cmdWrite(var)


class OLEDBit(framebuf.FrameBuffer):
    """
    bluebit OLED模块类

    :param rx,tx: 接收,发送引脚
    """

    font_5x7 = const(0x00)
    """字体常量-5*7英文字体"""

    font_song16 = const(0x01)
    """字体常量-16*16宋体"""
    font_song24 = const(0x02)
    """字体常量-24*24宋体"""
    font_consol32 = const(0x03)
    """字体常量-32*32宋体"""

    # 继承micropython framebuf 类,支持framebuffer方法
    def __init__(self, rx, tx):
        # 定义串口引脚
        self.uart = UART(1, 115200, rx=rx, tx=tx)
        self.buffer = bytearray(128 * 8)
        super().__init__(self.buffer, 128, 64, framebuf.MONO_VLSB)
        self.clear()

    def Print(self, str, x, y, font=font_song16):
        """
        显示中英文字符串,支持字体 '0' =Font5x7, '1' = 宋体16x16, '2' = 宋体24x24, '3' = Consolas32x32

        :param str str: 中英文字符串
        :param int x y: 显示坐标
        :param font: 字体类型, ``font_5x7`` , ``font_song24`` , ``font_consol32`` ;
        """

        temp = "@%d,%d,%d:%s\r\n" % (x, y, font, str)
        self.uart.write(temp.encode())

    def clear(self, x0=0, y0=0, x1=127, y1=63):
        """
        清除,默认全屏清除,也可以局部清除

        :param int x0 y0: 抹去区域左上坐标
        :param int x1 y1: 抹去区域右下坐标
        """

        self.uart.write("#0:%d,%d,%d,%d\r\n" % (x0, y0, x1, y1))

    def show(self):
        """
        显示生效,当使用framebuf类方法后使用show()刷新屏幕.
        """
        self.uart.write(">".encode() + self.buffer)

    def Bitmap(self, x, y, bitmap, w, h, c):
        """ 
        显示图案

        :param int x y: 起点坐标
        :param bitmap: 图案1bit数据
        :param w,h: 图案宽高
        :param c: 颜色,1 or 0 
        """
        byteWidth = int((w + 7) / 8)
        for j in range(h):
            for i in range(w):
                if bitmap[int(j * byteWidth + i / 8)] & (128 >> (i & 7)):
                    super().pixel(x + i, y + j, c)


class IRRecv(object):
    """
    红外接收模块

    :param rx: 接收引脚设置
    :param uart_id: 串口号:1、2
    """

    def __init__(self, rx, uart_id=1):

        self.uart = UART(uart_id, baudrate=115200, rx=rx)

    def recv(self):
        """
        接收数据

        :return int: 返回红外值,类型整形
        """
        if self.uart.any():
            temp = self.uart.read()
            if temp is not None:
                return ustruct.unpack("B", temp)[0]
            else:
                return None


class IRTrans(object):
    """
    红外发射模块

    :param tx: 发送引脚设置
    :param uart_id: 串口号:1、2
    """

    def __init__(self, tx, uart_id=2):
        self.uart = UART(uart_id, baudrate=115200, tx=tx)

    def transmit(self, byte):
        """
        发送数据

        :param byte byte: 发送数据,单字节
        """
        self.uart.write(byte)


class DelveBit(object):
    """
    实验探究类的blue:bit,适用的模块有电压、电流、磁场、电导率、PH、光电门、气压、力传感器

    :param address: 模块的I2C地址,可再模块拨动选择不同的地址避免冲突。
    :param i2c: I2C实例对象,默认i2c=i2c
    """

    def __init__(self, address, i2c=i2c):
        self.i2c = i2c
        self.address = address

    def common_measure(self):
        """
        获取实验探究类传感器测量值的通用函数

        :return int: 返回传感器测量值,单位:电压(V)、电流(A)、磁场(mT)、电导率(uS/cm)、PH(pH)、光电门(s)、气压(kPa)、力传感器(N)
        """

        self.i2c.scan()
        temp = self.i2c.readfrom(self.address, 2)
        data = ustruct.unpack(">h", temp)
        sleep_ms(20)
        return round(data[0] / 100, 2)

    def _trigger_receive(self):
        self.i2c.scan()
        temp = self.i2c.readfrom(self.address, 5, True)
        if temp[0] in [0, 1]:
            return temp
        else:
            temp = b'\xff'
            return temp

    def photo_gate(self):
        """
        Photogate Timer 是用来记录刚触发时刻和触发结束时刻的时间。计算信号的正脉宽时间,当输入信号由低变高为触发开始点,由高变低位触发触发结束点,计算之间的时间差。

        :return int: 返回正脉宽时间,单位秒
        """
        old_start = b'\xff'
        while True:
            start = self._trigger_receive()
            if start[0] == 1 and old_start[0] == 255:
                trigger_begin = start[1] * 16777216 + start[2] * 65536 + start[
                    3] * 256 + start[4]
                old_end = start
                while True:
                    end = self._trigger_receive()
                    if old_end[0] == 0 and end[0] == 255:
                        trigger_end = old_end[1] * 16777216 + old_end[
                            2] * 65536 + old_end[3] * 256 + old_end[4]
                        trigger_time = (trigger_end - trigger_begin) / 2041667
                        # print("time:", trigger_time, trigger_begin,
                        #       trigger_end)
                        return trigger_time
                    else:
                        old_end = end
                        continue
            else:
                old_start = start
                continue


class EncoderMotor(object):
    """
    blue:bit编码电机驱动,提供pwm、cruise、position 三种驱动方式。

    :param address: 模块的I2C地址,可再模块拨动选择不同的地址避免冲突。
    :param i2c: I2C实例对象,默认i2c=i2c
    """

    PWM_MODE = b'\x05'
    """pwm模式"""

    CRUISE_MODE = b'\x0a'
    """巡航模式"""

    POSITION_MODE = b'\x0f'
    """定位模式"""

    def __init__(self, address, i2c=i2c):
        self.i2c = i2c
        self.address = address

    def _effect(self, mode):
        """
        生效
        """
        write_buf = b'\x00' + mode
        self.i2c.writeto(self.address, write_buf)
        sleep_ms(10)

    def motor_stop(self):
        """
        停止编码电机转动
        """

        self.i2c.writeto(self.address, b'\x00\x00')
        sleep_ms(10)

    def set_pwm(self, speed1, speed2):
        """
        pwm模式

        :param speed1: 设置M1通道编码电机速度,范围-1023~1023
        :param speed2: 设置M2通道编码电机速度,范围-1023~1023
        """
        if speed1 > 1023 or speed1 < -1023 or speed2 > 1023 or speed2 < -1023:
            raise ValueError("Speed out of range:-1023~1023")
        write_buf = b'\x06' + ustruct.pack('>HH', speed1, speed2)
        self.i2c.writeto(self.address, write_buf)
        sleep_ms(10)
        self._effect(self.PWM_MODE)

    def set_cruise(self, speed1, speed2):
        """
        Cruise巡航模式,设定速度后,当编码电机受阻时,会根据反馈,自动调整扭力,稳定在恒定的速度。

        :param speed1: 设置M1通道编码电机速度,范围-1023~1023
        :param speed2: 设置M2通道编码电机速度,范围-1023~1023
        """
        if speed1 > 1023 or speed1 < -1023 or speed2 > 1023 or speed2 < -1023:
            raise ValueError("Speed out of range:-1023~1023")
        write_buf = b'\x0a' + ustruct.pack('>HH', speed1, speed2)
        self.i2c.writeto(self.address, write_buf)
        sleep_ms(10)
        self._effect(self.CRUISE_MODE)

    def set_position(self, turn1, turn2):
        """
        定位模式,可设置编码编码电机定点位置,范围-1023~1023。

        :param turn1: 设置M1通道编码电机定位,-1023~1023
        :param turn2: 设置M2通道编码电机定位,-1023~1023
        """
        if turn1 > 1023 or turn1 < -1023 or turn2 > 1023 or turn2 < -1023:
            raise ValueError("Position out of range:0~1023")
        write_buf = b'\x10' + ustruct.pack('>ll', turn1, turn2)
        self.i2c.writeto(self.address, write_buf)
        sleep_ms(10)
        self._effect(self.POSITION_MODE)
