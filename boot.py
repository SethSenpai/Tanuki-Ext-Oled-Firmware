import supervisor
import board
import digitalio
import storage
import usb_cdc
import usb_hid

if hasattr(supervisor, 'set_usb_identification'):
    supervisor.set_usb_identification(manufacturer="Seth", product="Tanuki-Ext-Oled", vid=0xfeed, pid=0x5671)


# If this key is held during boot, don't run the code which hides the storage and disables serial
# Uncomment below here to enable hidden usb drive -----------------------------------

# col = digitalio.DigitalInOut(board.GP11) #esc key
# row = digitalio.DigitalInOut(board.GP22)
# col.switch_to_output(value=True)
# row.switch_to_input(pull=digitalio.Pull.DOWN)

# if not row.value:
#     storage.disable_usb_drive()
#     # Equivalent to usb_cdc.enable(console=False, data=False)
#     usb_cdc.disable()
#     usb_hid.enable(boot_device=1)

# row.deinit()
# col.deinit()