import supervisor


if hasattr(supervisor, 'set_usb_identification'):
    supervisor.set_usb_identification(manufacturer="Seth", product="Tanuki-Ext-Oled", vid=0xfeed, pid=0x5671)