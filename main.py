# Cart scale for Food Donation services
# Author: Bill@Kilgallons.com, 20260910
# MIT license
#
#
# Display, touchscreen, and compute module:
#      https://www.amazon.com/dp/B0D93MBWC2
#      Hosyond 3.5'' 320x480 Touch Screen ESP32 Display with WiFi+BT, ST7796U Driver LCD TFT Screen Module for Arduino IoT
#      https://www.lcdwiki.com/res/E32R35T/3.5inch_E32R35T_E32N35T_MicroPython_Demo_Instructions.pdf
#      https://www.lcdwiki.com/3.5inch_ESP32-32E_Display
#      Micropython library pulled from board demo, and extended by me
#
# Strain gauges
#      https://www.amazon.com/dp/B07B4DNJ2L
#      4 x 50kg Load Cell Half Bridge Strain Gauge Weight Sensor + 1x HX711 Module
#      Which included the HX711 sensor
#      https://github.com/SergeyPiskunov/micropython-hx711/tree/master
#
# 3d printed strain gauge holders from Thingiverse module scaled up by 1%
# Screwed into big rigid board, see wiring below to HX711
#               G1     G3
#               G2     G4
#
# Wiring things up (CYD = Cheap Yellow Display ESP32 board I2C)
#
#        CYD                  Ribbon       HX711
#    =================================================
#        3.3V (Red)           Red          VCC (Red)
#        SDA/IO32 (Black)     Orange       Data (Orange)
#        SCL/IO25 (Yel)       Yellow       Clk (White)
#        Gnd (Grn)            Grn          Gnd (Black)
#       
# Wiring things up (HX711 to 4x half bridge strain gauges)
#
#    Hx711       Strain Gauge      Strain Gauge
#   ============================================
#     E-           G1-Red
#     A+           G2-Red
#     A-           G3-Red
#     E+           G4-Red
#                  G1-Black          G3-BLack
#                  G3-White          G4-White
#                  G4-Black          G2-Black
#                  G1 White          G2-White
#

# Function to get a fresh tare value

# The rough tare of the scale and platform itself with no "extra" weight
baseline_tare = 802249
    
def get_tare_counts(hx)->int :
    tare = 0

    for x in range(0,10) :

        # Give things a moment to settle
        Delay_Ms(200)

        # Read values, block until a value is read
        while hx.is_ready() :
            continue

        val =  hx.read()
        tare += val

    tare = int(tare / 10)

    return tare

######################################################
# CYD Display Configuration
#############################################################
from machine import SPI, Pin
from ST7796 import LCD_35_ST7796, SPI_W_SPEED, Delay_Ms, display_number, display_segment  # pyright: ignore[reportMissingImports]
from Font_8x16_EN import Font_8x16_EN # pyright: ignore[reportMissingImports]
from Font_16x32_EN import Font_16x32_EN # pyright: ignore[reportMissingImports]

# Set up the pins for the TFT display on this particular CYD
#pin define
LCD_RS = 2
LCD_CS = 15
#LCD_RST = 27  #connect to ESP32 reset pin
LCD_SCK = 14
LCD_SDA = 13
LCD_SDO = 12
LCD_BL = 27

# And define some colors we might use
#color define
BLACK = 0x0000
WHITE = 0xFFFF
RED = 0xF800
GREEN = 0x07E0
BLUE = 0x001F
DARKBLUE = 0x01CF

# Set up the connection to the TFT
spi = SPI(1,baudrate=SPI_W_SPEED,sck=Pin(LCD_SCK),mosi=Pin(LCD_SDA),miso=Pin(LCD_SDO))
mylcd = LCD_35_ST7796(spi, LCD_CS, LCD_RS, LCD_BL)

# Set up the static background 
print('SPI channel for LCD set up with baud rate ' + str(SPI_W_SPEED))
mylcd.LCD_Clear(BLACK)
mylcd.Show_BMP_Pic('food_pantry.bmp', 0, 0)

# Set up a couple of buttons

# Set up the Tare button
mylcd.Fill_Rect(0,     # X
                197,   # Y
                159,   # width
                60,    # height
                BLUE) # color

# Now put label Show_String(x, y, string, font, color, backcolor = None)
mylcd.Show_String(5, 207, "Take Tare", Font_16x32_EN, WHITE)

# Set up the hold button
mylcd.Fill_Rect(170,   # X
                197,   # Y
                150,   # width
                60,    # height
                BLUE) # color

# Now put label
mylcd.Show_String(205, 207, "Hold", Font_16x32_EN, WHITE)

# Define where the numbers should go
digits_x_pos = 20
digits_y_pos = 277
digit_width = 90
digit_height = 150

#########################################
# Connection to digital scale
# Uses https://github.com/SergeyPiskunov/micropython-hx711/blob/master/hx711.py
#########################################

from hx711 import HX711 # pyright: ignore[reportMissingImports]
from machine import Pin

# Initialize HX711
hx = HX711(d_out=32, pd_sck=25)

# Turn off then on
hx.power_off()
hx.power_on()

# scaling factor for scale empiraclly measured to arrive at value
scale_count_conversion_factor = 9611

##############################
# Set up the touch screen
##############################

# Note this requires a lot more here... calibration, understanding coordinates, etc
# That being said, this worked if I touched the upper right hand corner
#
# coord = [0xFFFF, 0xFFFF] (x, y coordinates that will be populated by the )
# Read_Touch(coord, threshold)
# print('How touching! ' + str(coord))
# How touching!
# [-24, -30]

from touch import XPT2046 # pyright: ignore[reportMissingImports]
TOUCH_CS = 33
mytouch = XPT2046(spi, TOUCH_CS, lcd_speed = SPI_W_SPEED)
coord = [0xFFFF, 0xFFFF]
mytouch.Set_Touch_Cal(253, 240, 3464, 3622, 320, 480, 1)

#
# Get the tare value at boot.
# Note this should probably stay here, but also be exposed as a button on the touch screen
# eventually.
#
# It also wouldnt hurt to move this into a function in a library that 
# represents this module and gauges wired in a particular way to
# represent a digital scale that reads pounds
#

print('Setting tare for unloaded scale')

tare = get_tare_counts(hx) # Done at boot or with button push
tare_lbs = int(abs(tare - baseline_tare) / scale_count_conversion_factor)

mylcd.Show_String(1, 464, 'Current Tare : ' + str(tare_lbs) + ' lbs / ' + str(tare) + ' counts', Font_8x16_EN, WHITE)

print('Tare raw counts: ' + str(tare))

# Set up the hold button
hold_state = 0

while True:

    #
    # Now lets try reading our own peripheral (strain gauges set up as a weight scale)
    #

    if not hold_state :
        # not sure if True means ready or not.  Play with this when it actually matters
        while hx.is_ready() :
            continue

        # Read raw data
        raw_value = hx.read()
        print("Scale read :", raw_value)

        # Convert it to pounds
        pounds = int((raw_value - tare) / scale_count_conversion_factor)
        if pounds < 0 : pounds = 0

        # Display the reading on the display (320x480)
        # display_number(mylcd, number: int, position_x : int, position_y : int, char_x_width : int, char_y_height : int, color)

        # Erase old number (8 erases all segments in the digit)
        display_number(mylcd, 888, digits_x_pos, digits_y_pos, digit_width, digit_height, BLACK)

        # Draw new number
        display_number(mylcd, pounds, digits_x_pos, digits_y_pos, digit_width, digit_height, RED)

        # print('Displayed ' + str(pounds))

    #
    # Now lets try the touch screen
    #
    coord = [0xFFFF, 0xFFFF]
    loopcount = 0

    while True :

        # Instead of just delay, we will read the touch screen here while the number
        # shows for a bit (it has pretty bad flicker when updating, it is a really slow display)
        # 5 reads is about a second.  The touch screen is slow also.

        loopcount += 1
        if loopcount > 15 :
            break
    
        if mytouch.Read_Touch(coord, 200):
            print('Tare touch: ' + str(coord))

            x = coord[0]
            y = coord[1]

            #
            # See if it was the tare button
            #

            if ( abs(x-86) < 20) and (abs(y-220) < 20) :

                # Blank the old tare display
                mylcd.Show_String(1, 464, 'Current Tare : ' + str(tare_lbs) + ' lbs / ' + str(tare) + ' counts', Font_8x16_EN, BLACK)

                # Toggle the tare button color to busy
                mylcd.Fill_Rect(0,     # X
                                197,   # Y
                                159,   # width
                                60,    # height
                                RED) # color

                # Now update label
                mylcd.Show_String(5, 207, "Wait", Font_16x32_EN, WHITE)
                
                # Get the new tare 
                tare = get_tare_counts(hx) # Done at boot or with button push

                # Display the new tare
                tare_lbs = int(abs(tare - baseline_tare) / scale_count_conversion_factor)
                mylcd.Show_String(1, 464, 'Current Tare : ' + str(tare_lbs) + ' lbs / ' + str(tare) + ' counts', Font_8x16_EN, WHITE)               

                # Toggle the tare button color to normal
                mylcd.Fill_Rect(0,     # X
                                197,   # Y
                                159,   # width
                                60,    # height
                                BLUE) # color

                # Now update label
                mylcd.Show_String(5, 207, "Take Tare", Font_16x32_EN, WHITE)

                print('New Tare: ' + str(tare))

            #
            # See if it was the hold button
            #

            if ( abs(x-248) < 20) and (abs(y-230) < 20) :
                print('Hold touch: ' + str(coord))

                hold_state = not hold_state

                if hold_state :
                    mylcd.Fill_Rect(170, 197, 150, 60, RED)

                    # Now put label
                    mylcd.Show_String(205, 207, "Resume", Font_16x32_EN, WHITE)

                else: 
                    mylcd.Fill_Rect(170, 197, 150, 60, BLUE)

                    # Now put label
                    mylcd.Show_String(205, 207, "Pause", Font_16x32_EN, WHITE)

                # Debounce the display a little
                Delay_Ms(500)




  


        






