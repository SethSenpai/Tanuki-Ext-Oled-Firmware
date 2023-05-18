print("Starting")
import board

import displayio
import adafruit_displayio_ssd1306
import busio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
import terminalio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.lock_status import LockStatus

keyboard = KMKKeyboard()

keyboard.col_pins = (board.GP11,board.GP15,board.GP20,board.GP25,board.GP10,board.GP14,board.GP19,board.GP24,board.GP9,board.GP13,board.GP18,board.GP23)   
keyboard.row_pins = (board.GP22,board.GP17,board.GP12,board.GP8) 
keyboard.diode_orientation = DiodeOrientation.COL2ROW

keyboard.modules.append(Layers())
keyboard.extensions.append(MediaKeys())

KEY_LOWER   = KC.LT(1,KC.SPC, prefer_hold=False, tap_interrupted=False, tap_time=120)
KEY_HIGHER  = KC.LT(2,KC.SPC, prefer_hold=False, tap_interrupted=False, tap_time=120)

class LEDLockStatus(LockStatus):
    def after_hid_send(self, sandbox):
        super().after_hid_send(sandbox)  # Critically important. Do not forget
        if self.report_updated:
            renderUI()

locks = LEDLockStatus()
keyboard.extensions.append(locks)
isSpaceLocked = False

def renderUI():
    global display
    global locks
    screen = displayio.Group()
    uiGroup = displayio.Group()
    border = Rect(0,2,32,128, outline=0xffffff)
    uiGroup.append(border)

    screen.append(uiGroup)

    if locks.get_caps_lock():
        ta = label.Label(terminalio.FONT, text = "CL", color = 0x000000, x = 4, y = 8,background_color=0xffffff, padding_left = 2, padding_right=1)
        screen.append(ta)
    else:
        ta = label.Label(terminalio.FONT, text = "", color = 0xffffff, x = 3, y = 8)
        screen.append(ta)
        
    display.show(screen)

displayio.release_displays() #needed because the otherwise its claimed for debugging
i2c = busio.I2C(board.GP1,board.GP0)
display_bus = displayio.I2CDisplay(i2c,device_address=0x3c)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=32,height=128, rotation=90) #this configuration only works when pulling from the latest adafruit master

renderUI()

keyboard.keymap = [
    [   #Main
        KC.ESC,     KC.Q,   KC.W,   KC.E,   KC.R,            KC.T,   KC.Y,            KC.U,   KC.I,   KC.O,   KC.P,   KC.BSPC,
        KC.TAB,     KC.A,   KC.S,   KC.D,   KC.F,            KC.G,   KC.H,            KC.J,   KC.K,   KC.L,   KC.SCLN,KC.ENT,
        KC.LSFT,    KC.Z,   KC.X,   KC.C,   KC.V,            KC.B,   KC.N,            KC.M,   KC.QUOT,KC.SLSH,KC.DEL, KC.UP,
        KC.LCTL,    KC.LALT,KC.COMM,KC.NO,  KEY_LOWER,       KC.NO,  KEY_HIGHER,      KC.DOT, KC.LGUI,KC.LEFT,KC.DOWN,KC.RIGHT   
    ],
    [   #Symbols
        KC.GRV,     KC.LBRC,KC.RBRC,KC.LCBR,KC.RCBR,KC.PIPE,KC.BSLS,KC.PLUS,KC.MINS,KC.UNDS,KC.EQL, KC.RESET,
        KC.TRNS,    KC.EXLM,KC.AT,  KC.HASH,KC.DLR, KC.PERC,KC.CIRC,KC.AMPR,KC.ASTR,KC.LPRN,KC.RPRN,KC.DEBUG,
        KC.TRNS,    KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.VOLU,
        KC.TRNS,    KC.TRNS,KC.TRNS,KC.NO,  KC.TRNS,KC.NO, KC.TRNS, KC.TRNS,KC.TRNS,KC.MUTE,KC.VOLD,KC.MNXT
    ],
    [   #numbers and functions
        KC.F1,      KC.F2,  KC.F3,  KC.F4,  KC.F5,  KC.F6,  KC.F7,  KC.F8,  KC.F9,  KC.F10, KC.F11, KC.F12,
        KC.TRNS,    KC.P1,  KC.P2,  KC.P3,  KC.P4,  KC.P5,  KC.P6,  KC.P7,  KC.P8,  KC.P9,  KC.P0,  KC.TRNS,
        KC.CAPS,    KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.PGUP,KC.TRNS,
        KC.PSCR,    KC.TRNS,KC.TRNS,KC.NO,  KC.TRNS,KC.NO, KC.TRNS, KC.TRNS,KC.TRNS,KC.HOME,KC.PGDN,KC.END
    ],
    [   #Space Locked
        KC.ESC,     KC.Q,   KC.W,   KC.E,   KC.R,            KC.T,   KC.Y,            KC.U,   KC.I,   KC.O,   KC.P,   KC.BSPC,
        KC.TAB,     KC.A,   KC.S,   KC.D,   KC.F,            KC.G,   KC.H,            KC.J,   KC.K,   KC.L,   KC.SCLN,KC.ENT,
        KC.LSFT,    KC.Z,   KC.X,   KC.C,   KC.V,            KC.B,   KC.N,            KC.M,   KC.QUOT,KC.SLSH,KC.DEL, KC.UP,
        KC.LCTL,    KC.LALT,KC.COMM,KC.NO,  KC.SPC,          KC.NO,  KC.SPC,          KC.DOT, KC.LGUI,KC.LEFT,KC.DOWN,KC.RIGHT   
    ]
]

if __name__ == '__main__':
    keyboard.go()    
