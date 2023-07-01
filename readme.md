# Tanuki-Ext OLED Firmware

## Features
Release Version 1.0 includes the following features:
* HID compliant keyboard
* Space lock, activated by pressing both spacebars at the same time, used to disable spacebar layer switching (useful for games)
* Status indicators on OLED screen including, Current Layer, Caps Lock, Scroll lock
* A timeout feature to turn off the OLED after 1 minute of inactivity to prevent burn-in

More exotic features can be found in the branches of this project.

## Flashing the board
*Does the device identify itself as a Tanuki Keyboard when plugged in?*

**YES!** Hold down the escape key when plugging in the USB cable. A mass storage device called `CIRCUITPY` should appear. On the storage device you can find the currently running firmware files. Either edit them or delete files and upload new ones. The device auto restarts after a new file is uploaded or a file is saved.

**NO!** Go to the [Adafruit website](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython#install-circuitpython-3105177) and install the latest version of CircuitPython on the board. After that is done there should be a mass storage device called `CIRCUITPY`. Copy over all the files except those in the .git and .vscode folders. You can also ignore this readme when copying over the firmware.

## File Structure
The core function of the firmware contains only 2 files. The `main.py` file and the `boot.py` file. 

`main.py` contains the application code. In other words the code that makes the keyboard a keyboard and its probably the file that you'll be editing the most. 

The `boot.py` file contains code that can change the startup behaviour of the keyboard. This is where the identifying name of the keyboard is set. It also contains a commented out block of code that you can enable by uncommenting it. This code block allows you to hide the Mass storage device and serial debug port. Allowing the keyboard to be just like any other normal HID keyboard. By holding the ESC key during bootup you can reenable the Serial and Mass storage.

## Debugging using Serial
When the device is has its Mass storage device and serial connection enabled you can have your code Print things to the Serial port for debugging purposes. How to connect to the Serial port depends on what operating system you're using. Check out this [article](https://learn.adafruit.com/welcome-to-circuitpython/kattni-connecting-to-the-serial-console) on the Adafruit website to learn more.

Personally on Linux I like to use `screen`. This can be done by opening a terminal window and typing in:

`ls /dev/ttyACM*`

Which should give you a list of the currently available Serial ports. Connecting can then be done with:

`screen /dev/ttyACM0`

Make sure to change the 0 to a number you got back from the first command.

## Libraries Included in this Firmware
Based on commit `93b0bb1` from [kmk firmware](https://github.com/KMKfw/kmk_firmware).

Using uncompressed version of the [DisplayIO_SSD1306](https://github.com/adafruit/Adafruit_CircuitPython_DisplayIO_SSD1306) commit `
4a48127` due to errors in latest stable release causing the rotation function to display random noise on the OLED.

Also included are the `adafruit_display_text` and `adafruit_display_shapes` libraries from the release of the Adafruit_CircuitPython_Bundle on [28th of May, 2023](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/tag/20230528)

## Known Issues
* With the current version of Circuitpython and the Tanuki-Ext OLED PCB there is a chance the board does not boot immediately after the usb cable is connected. This has something to do with the way Circuitpython enables the external oscillator and can be fixed by unplugging and re-plugging the keyboard.

* Boot times are rather slow and can take up to 5 seconds before the device becomes fully available.