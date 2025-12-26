# (spi=1, cs=8, din=9, clk=10)

from machine import Pin, SPI
import time
import seven_segment

spi = SPI(1, baudrate=100000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(9))
cs = Pin(8, Pin.OUT, value=1)

display = seven_segment.SevenSegmentDisplay(spi, cs)
display.brightness(0x00)

for _ in range (4): display.sequence(4, seven_segment.HOURGLASS)
display.scroll("12345678")
display.text("12345678")
time.sleep(2)
display.clear_all()
display.flip_text("12345678")
time.sleep(2)
display.clear_all()
display.flip_text("12345678", all=False)
time.sleep(2)
display.clear_all()
display.flip_text("12345678", all=False, background=False)
time.sleep(1)
display.blink_digit(7)
display.flash()
display.clear_all()
for _ in range (2): display.ping_pong('-')
for i in range (100):
    display.loading_bar(i + 1)
    time.sleep(0.01)
time.sleep(2)
display.clear_all()
for i in range (10, 0, -1):
    display.text(f"{i:5d}")
    time.sleep(1)

display.clear_all()
display.off()
