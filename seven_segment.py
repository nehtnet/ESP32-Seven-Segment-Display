import time, urandom

DIGITS = 8

SEG_A = 0b01000000
SEG_B = 0b00100000
SEG_C = 0b00010000
SEG_D = 0b00001000
SEG_E = 0b00000100
SEG_F = 0b00000010
SEG_G = 0b00000001
SEG_DP = 0b10000000
HOURGLASS = [SEG_A, SEG_B, SEG_C, SEG_D, SEG_E, SEG_F]
UPDOWN = [SEG_A, SEG_G, SEG_D, SEG_G]
LEFTRIGHT = [SEG_B | SEG_C, SEG_E | SEG_F]

BIN = {
    ' ': 0b00000000,
    '!': 0b10100000,
    '"': 0b00100010,
    "'": 0b00100000,
    '#': 0b01111110,
    '$': 0b01101101,
    '%': 0b01001001,
    '&': 0b01011111,
    '(': 0b01001110,
    ')': 0b01111000,
    '[': 0b01001110,
    ']': 0b01111000,
    '{': 0b01001110,
    '}': 0b01111000,
    '*': 0b00110111,
    '+': 0b00110001,
    '-': 0b00000001,
    '_': 0b00001000,
    '=': 0b01000001,
    '|': 0b00110000,
    '/': 0b00100101,
    '\\': 0b00010011,
    ',': 0b00010000,
    '.': 0b10000000,
    ':': 0b01001000,
    ';': 0b01010000,
    '<': 0b00110001,
    '>': 0b00000111,
    '?': 0b11100101,
    '@': 0b01111101,
    '^': 0b01100010,
    '`': 0b00000010,
    '~': 0b01000000,

    '0': 0b01111110,
    '1': 0b00110000,
    '2': 0b01101101,
    '3': 0b01111001,
    '4': 0b00110011,
    '5': 0b01011011,
    '6': 0b01011111,
    '7': 0b01110000,
    '8': 0b01111111,
    '9': 0b01111011,

    'A': 0b01110111,
    'B': 0b00011111,
    'C': 0b01001110,
    'D': 0b00111101,
    'E': 0b01001111,
    'F': 0b01000111,
    'G': 0b01011110,
    'H': 0b00110111,
    'I': 0b00000110,
    'J': 0b00111100,
    'K': 0b01110101,
    'L': 0b00001110,
    'M': 0b00010101,
    'N': 0b01110110,
    'Ñ': 0b01010101,
    'O': 0b01111110,
    'P': 0b01100111,
    'Q': 0b01101011,
    'R': 0b00100101,
    'S': 0b01011011,
    'T': 0b00001111,
    'U': 0b00111110,
    'V': 0b00111110,
    'W': 0b00101010,
    'X': 0b00110111,
    'Y': 0b00111011,
    'Z': 0b01101101,

    'a': 0b01111101,
    'b': 0b00011111,
    'c': 0b00001101,
    'd': 0b00111101,
    'e': 0b01101111,
    'f': 0b01000111,
    'g': 0b01111011,
    'h': 0b00010111,
    'i': 0b00000100,
    'j': 0b00011000,
    'k': 0b01110101,
    'l': 0b00000110,
    'm': 0b00010100,
    'n': 0b00010101,
    'ñ': 0b01010101,
    'o': 0b00011101,
    'p': 0b01100111,
    'q': 0b01110011,
    'r': 0b00000101,
    's': 0b01011011,
    't': 0b00001111,
    'u': 0b00011100,
    'v': 0b00011100,
    'w': 0b00010100,
    'x': 0b00110111,
    'y': 0b00111011,
    'z': 0b01101101
}

class SevenSegmentDisplay:
    def __init__(self, spi, cs):
        self.cs = cs
        self.spi = spi
        self.cs.value(1)
        self.buffer = [0x00] * DIGITS

        time.sleep_ms(100)
        self.write(0x0C, 0x00)  # FORCE shutdown
        time.sleep_ms(10)

        self.write(0x09, 0x00)  # NO decode
        self.write(0x0A, 0x08)  # brightness 0x00 - 0x0F
        self.write(0x0B, 0x07)  # scan limit = 8 digits
        self.write(0x0C, 0x01)  # normal operation
        self.write(0x0F, 0x00)  # test OFF

        self.clear_all()

    def on(self):
        self.write(0x0C, 0x01)

    def off(self):
        self.write(0x0C, 0x00)

    def write(self, reg, data):
        self.cs.value(0)
        time.sleep_us(5)
        self.spi.write(bytearray([reg, data]))
        time.sleep_us(5)
        self.cs.value(1)

        if 1 <= reg <= DIGITS:
            self.buffer[DIGITS - reg] = data

    def read(self, pos):
        return self.buffer[pos]

    def brightness(self, value):
        self.write(0x0A, value)

    def clear(self, pos):
        self.write(DIGITS - pos, 0x00)
        
    def clear_all(self):
        for pos in range(DIGITS):
            self.clear(pos)

    def digit(self, pos, char):
        self.write(DIGITS - pos, BIN[char])

    def clear_digit(self, pos, char):
        self.write(DIGITS - pos, self.read(pos) & ~BIN[char])

    def dot(self, pos):
        self.write(DIGITS - pos, self.read(pos) | SEG_DP)

    def clear_dot(self, pos):
        self.write(DIGITS - pos, self.read(pos) & ~SEG_DP)

    def text(self, string):
        for i, char in enumerate(string[:8]):
            self.digit(i, char)

    def scroll(self, string, delay=0.2):
        string = " " * DIGITS + string + " " * DIGITS
        for i in range(len(string) - DIGITS + 1):
            self.text(string[i:i+DIGITS])
            time.sleep(delay)

    def sequence(self, pos, seq, delay=0.1):
        for seg in seq:
            self.write(DIGITS - pos, seg)
            time.sleep(delay)
        self.clear_all()
    
    def ping_pong(self, char, delay=0.1):
        for i in range(DIGITS):
            self.digit(i, char)
            if i!=DIGITS: self.clear(i - 1)
            time.sleep(delay)
        for i in range(DIGITS - 2, 0, -1):
            self.clear(i + 1)
            self.digit(i, char)
            time.sleep(delay)
        self.clear(i)

    def flash(self, times=3, delay=0.2):
        for _ in range(times):
            self.off()
            time.sleep(delay)
            self.on()
            time.sleep(delay)

    def blink_digit(self, pos, times=3, delay=0.2):
        orig = self.read(pos)
        for _ in range(times):
            self.clear(pos)
            time.sleep(delay)
            self.write(DIGITS - pos, orig)
            time.sleep(delay)

    def loading_bar(self, percent):
        for i in range(DIGITS):
            state = int((percent * DIGITS * 2) // 100) - (i * 2)
            pattern = SEG_E | SEG_F | SEG_B | SEG_C
            if state <= 0:
                pattern = 0x00
            elif state == 1:
                pattern = SEG_E | SEG_F

            self.write(DIGITS - i, pattern)

    def flip_text(self, string, all=True, background=True, steps=12, delay=0.05):
        targets = [BIN[c] for c in string]
        locked = [False] * len(string)
        for reveal_pos in range(len(string)):
            for _ in range(steps):
                for pos in range(len(string) if background else reveal_pos + 1):
                    if locked[pos]:
                        self.write(DIGITS - pos, targets[pos])
                    else:
                        pattern = 0
                        for bit in (SEG_A, SEG_B, SEG_C, SEG_D, SEG_E, SEG_F, SEG_G):
                            if urandom.getrandbits(1):
                                pattern |= bit
                        self.write(DIGITS - pos, pattern)
                time.sleep(delay)
            if not all:
                locked[reveal_pos] = True
                self.write(DIGITS - reveal_pos, targets[reveal_pos])
            else:
                self.text(string)
                return
