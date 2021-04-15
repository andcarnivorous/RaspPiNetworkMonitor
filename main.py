import lcddriver
import time
import utils
import os

display = lcddriver.lcd()

if "database.db" not in os.listdir():
    
    newtable = """ CREATE TABLE IF NOT EXISTS visitors (
    ip TEXT,
    name TEXT,
    date TEXT
    ); 
    CREATE UNIQUE INDEX idx_name on visitors (name);"""

    with utils.create_connection("database.db") as conn:
        utils.create_table(conn, newtable)

try:
    while True:
        # Remember that your sentences can only be 16 characters long!
        ipadd = ".".join(utils.get_ip_address())
        ips, names = utils.give_ips()
        display.lcd_clear()

        for ip in range(1,len(ips)):
            display.lcd_display_string("# Devices: %d" % len(ips), 1) # Write line of text to first line of display
            display.lcd_display_string("# %d: %s" % (ip, ips[ip]), 3) # Write line of text to first line of display
            display.lcd_display_string("Name: %s" % names[ip][:13], 4)
            time.sleep(2)
            display.lcd_clear()

        display.lcd_display_string("Scanning network...", 1)
        display.lcd_display_string("MyIP : %s" % ipadd, 4) # Write line of text to second line of display

except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_clear()
