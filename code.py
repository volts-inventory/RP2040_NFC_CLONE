import time
import board
import digitalio
import bitbangio
import mfrc522
import time
import board
from board import SCL, SDA
import adafruit_ssd1306
import busio

i2c = busio.I2C(SCL, SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
display.fill(0)
display.show()
# VCC = 3V
rst = digitalio.DigitalInOut(board.A3)
gnd = digitalio.DigitalInOut(board.A2)
gnd.switch_to_output(value=False)
spi = bitbangio.SPI(board.SCK, MOSI=board.A0, MISO=board.A1)
cs = digitalio.DigitalInOut(board.MISO)
rfid = mfrc522.MFRC522(spi, cs, rst)
rfid.set_antenna_gain(0x07 << 4)

level = 0
count = 0

def clear_screen(delay = 1):
    time.sleep(delay)
    global level
    display.fill(0)
    display.show()
    level = 0
    
def print_screen(string):
    global level
    display.text(string, 0, level, 1)
    display.show()
    level += 10


def status_rfid():
    global count
    
    prev_data = ""
    prev_time = 0
    timeout = 1
    while True:
        if count == 0:
            clear_screen()
            print("\nScan your RFid tag\n")
            print_screen("\nScan your RFid tag\n")
            count += 1
        (status, tag_type) = rfid.request(rfid.REQALL)
        if status == rfid.OK:
            count = 0
            clear_screen(delay=0)
            (status, raw_uid) = rfid.anticoll()
            if status == rfid.OK:
                rfid_data = "{:02x}{:02x}{:02x}{:02x}".format(raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
                if rfid_data != prev_data:
                    prev_data = rfid_data
                    print("Card detected! UID: {}".format(rfid_data))
                    print("  - tag type: 0x%02x" % tag_type)
                    print_screen("Card detected! UID: {}".format(rfid_data))
                    print_screen("  - tag type: 0x%02x" % tag_type)
                prev_time = time.monotonic()
                return
        else:
            if time.monotonic() - prev_time > timeout:
                prev_data = ""
            
def read_rfid():
    global count
    while True:
        if count == 0:
            clear_screen()
            print("\nScan your RFid tag\n")
            print_screen("\nScan your RFid tag\n")
            count += 1
        (stat, tag_type) = rfid.request(rfid.REQIDL)
        if stat == rfid.OK:
            count = 0
            (stat, raw_uid) = rfid.anticoll()
            if stat == rfid.OK:
                if rfid.select_tag(raw_uid) == rfid.OK:
                    clear_screen(delay=0)
                    print("New card detected")
                    print("  - tag type: 0x%02x" % tag_type)
                    print("  - uid\t : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    print('')
                    print_screen("New card detected")
                    print_screen("  - tag type: 0x%02x" % tag_type)
                    print_screen("  - uid\t : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    print_screen('')
                    clear_screen()
                    r = rfid.read(8)
                    print("Address 8 data: 0x%02x%02x%02x%02x" % (r[0], r[1], r[2], r[3]))
                    print_screen("Address 8 data: 0x%02x%02x%02x%02x" % (r[0], r[1], r[2], r[3]))
                    return
                else:
                    clear_screen()
                    print("Failed to select tag")
                    print_screen("Failed to select tag")

def write_rfid():
    global count
    while True:
        if count == 0:
            print("\nWrite your RFid tag\n")
            clear_screen()
            print_screen("\nWrite your RFid tag\n")
            count += 1
        (stat, tag_type) = rfid.request(rfid.REQIDL)
        if stat == rfid.OK:
            count = 0
            (stat, raw_uid) = rfid.anticoll()
            if stat == rfid.OK:  
                clear_screen(delay=0)
                print("New card detected")
                print("  - tag type: 0x%02x" % tag_type)
                print("  - uid\t : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                print('')
                print_screen("New card detected")
                print_screen("  - tag type: 0x%02x" % tag_type)
                print_screen("  - uid\t : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                print_screen('')
                if rfid.select_tag(raw_uid) == rfid.OK:
                    
                    stat = rfid.write(8, b"\x00\x01\x02\x03\x04\x05\x06\x07x00\x01\x02\x03\x04\x05\x06\x07")

                    if stat == rfid.OK:
                        clear_screen()
                        print("Data written to card")
                        print_screen("Data written to card")
                        return
                    else:
                        clear_screen()
                        print("Failed to write data to card")
                        print_screen("Failed to write data to card")
                    
                else:
                    clear_screen()
                    print("Failed to select tag")
                    print_screen("Failed to select tag")

def main():
    read_rfid()
    pass
    

main()
