print("Starting")
import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC, make_key
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers as _Layers
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.lock_status import LockStatus
from kmk.modules.combos import Combos, Chord

from tanuki_ui import TanukiUI

keyboard = KMKKeyboard()
keyboard.extensions.append(MediaKeys())

keyboard.col_pins = (board.GP11,board.GP15,board.GP20,board.GP25,board.GP10,board.GP14,board.GP19,board.GP24,board.GP9,board.GP13,board.GP18,board.GP23)   
keyboard.row_pins = (board.GP22,board.GP17,board.GP12,board.GP8) 
keyboard.diode_orientation = DiodeOrientation.COL2ROW

#Class extensions
class LayersObj(_Layers): #deals with interactions based on layer switching
    last_layer_index = 0

    def after_hid_send(self, keyboard):
        if keyboard.active_layers[0] != self.last_layer_index:
            ui.layerIndex = keyboard.active_layers[0]
            self.last_layer_index = keyboard.active_layers[0]
            ui.updateUI(locks)

class LockStatusObj(LockStatus): #deals with interaction based on lock key status
    def after_hid_send(self, sandbox):
        super().after_hid_send(sandbox)
        if self.report_updated:
            ui.updateUI(locks)                    

locks = LockStatusObj()
keyboard.extensions.append(locks)
keyboard.modules.append(LayersObj())

#initialize UI for OLED
ui = TanukiUI(board.GP1,board.GP0)
ui.updateUI(locks)

#custom keys for tap or holding spacebars
KEY_LOWER   = KC.LT(2,KC.SPC, prefer_hold=False, tap_interrupted=False, tap_time=120)
KEY_HIGHER  = KC.LT(1,KC.SPC, prefer_hold=False, tap_interrupted=False, tap_time=120)

#combo module allows us to tap both spacebars to switch layers
combo = Combos()
keyboard.modules.append(combo)

def setSpaceLock():
    if ui.isSpaceLocked:
        ui.isSpaceLocked = False
        keyboard.active_layers[0] = 0 #switch layer to base
    else:
        ui.isSpaceLocked = True
        keyboard.active_layers[0] = 3 #switch layer to space locked
    ui.updateUI(locks)

make_key( #create a special key that triggers a function
    names=('SPLK',),
    on_press=lambda *args: setSpaceLock(),
)

#40 and 42 are spacebars int coords in matrix
combo.combos = [
    Chord((40,42),KC.SPLK, match_coord=True),
]

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
