# Cart scale for Food Donation services
# Author: Bill@Kilgallons.com, 20260910
# MIT license
#
# See readme.md for more info
#

# Some global constants
scale_count_conversion_factor = 9611     # Manually calculated by measuring two known counts and weights 
typ_zero_sensor_count = 837700           # Manually measured after platform built

# Function to get a fresh tare value
    
def get_sensor_tare_raw_counts(hx)->int :
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

# Calculate tare pounds
def get_tare_lbs(dolly_tare_state, cart_tare_state) -> int :

    tare_lbs = 0 
    dolly_lbs = 15
    cart_lbs = 45

    if dolly_tare_state:
        tare_lbs += dolly_lbs

    if cart_tare_state:
        tare_lbs += cart_lbs

    return tare_lbs

#
# Convert counts to lbs.  This needs to include the true tare counts from the sensor read
#

def sensor_lbs(sensor_tare_raw_counts, current_sensor_counts) -> int :

    tared_sensor_counts = current_sensor_counts - sensor_tare_raw_counts

    if tared_sensor_counts < 0:
        tared_sensor_counts = 0

    pounds = int(tared_sensor_counts / scale_count_conversion_factor)

    return pounds

#
# Set up the buttons
# This is a fussy little empirical process, just manually calculated and tuned
#

# Tare button, valid states are "READY" and "IN_PROGRESS"

def paint_tare_button(state : str, mylcd) :
  
    tare_but_x = 0
    tare_but_y = 197

    if 'READY' in state:
        bgcolor = BLUE
        button_text = 'Tare'

    else:
        bgcolor = RED
        button_text = 'Wait'

    # Paint the button
    mylcd.Fill_Rect(tare_but_x,     # X
                    tare_but_y,   # Y
                    100,   # width
                    60,    # height
                    bgcolor) # color

    # Label the button
    # Now put label Show_String(x, y, string, font, color, backcolor = None)
    mylcd.Show_String(tare_but_x + 15, tare_but_y + 10, button_text, Font_16x32_EN, WHITE)

# returns true if x y coordinates represent a press of the tare button
def pressed_tare_button(x, y) -> bool :

    if x > 0 and x < 100 :
        if y > 197 and y < 257 :
            return True

    return False

# Dolly button "ON" "OFF"
def paint_dolly_button(state : str, mylcd) :
    dolly_but_x = 109
    dolly_but_y = 197

    if 'OFF' in state:
        bgcolor = BLUE

    else:
        bgcolor = RED

    # Paint the button
    mylcd.Fill_Rect(dolly_but_x,     # X
                    dolly_but_y,    # Y
                    100,    # width
                    60,    # height
                    bgcolor) # color

    # Label the button
    # Now put label Show_String(x, y, string, font, color, backcolor = None)
    mylcd.Show_String(dolly_but_x + 10, dolly_but_y + 10, "Dolly", Font_16x32_EN, WHITE)

# returns true if x y coordinates represent a press of the tare button
def pressed_dolly_button(x, y) -> bool :

    if x > 109 and x < 209 :
        if y > 197 and y < 257 :
            return True

    return False

# Cart button
def paint_cart_button(state : str, mylcd) :

    cart_but_x = 218
    cart_but_y = 197

    if 'OFF' in state:
        bgcolor = BLUE

    else:
        bgcolor = RED

    # Paint the button
    mylcd.Fill_Rect(cart_but_x,    # X
                    cart_but_y,    # Y
                    100,    # width
                    60,    # height
                    bgcolor) # color

    # Label the button
    # Now put label Show_String(x, y, string, font, color, backcolor = None)
    mylcd.Show_String(cart_but_x + 15, cart_but_y + 10, "Cart", Font_16x32_EN, WHITE)

# returns true if x y coordinates represent a press of the tare button
def pressed_cart_button(x, y) -> bool :

    if x > 218 and x < 318 :
        if y > 197 and y < 257 :
            return True

    return False

# Display the Tare info string
def display_tare_info(mylcd, tare_lbs) :
    mylcd.Fill_Rect(0, 464, 320, 16, BLACK)
    mylcd.Show_String(1, 464, 'Current Tare : ' + str(tare_lbs) + ' lbs (auto subtracted)', Font_8x16_EN, WHITE)

# This is really just here to warn you that something has either gone really wrong with the sensor,
# or that you tared it with something else on the scale (intentionally or not)
def display_sensor_info(mylcd, tare_count) :

    current_delta = abs(tare_count - typ_zero_sensor_count)
    sensor_tare_lb_delta = int(current_delta / scale_count_conversion_factor)

    mylcd.Fill_Rect(0, 444, 320, 16, BLACK)
    mylcd.Show_String(1, 444, 'Sensor Tare : ' + str(sensor_tare_lb_delta), Font_8x16_EN, WHITE)

#
# Start of program
#

# Tare button states
dolly_tare_state = False
cart_tare_state = False

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

# Show the boot state buttons
paint_tare_button('IN_PROGRESS', mylcd)
paint_dolly_button('OFF', mylcd)
paint_cart_button('OFF', mylcd)

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
tare_count = get_sensor_tare_raw_counts(hx) # Done at boot or with button push

tare_lbs = get_tare_lbs(dolly_tare_state, cart_tare_state)
display_tare_info(mylcd, tare_lbs)

display_sensor_info(mylcd, tare_count)

print('Tare raw counts: ' + str(tare_count))
print('Tare Lbs: ' + str(tare_lbs))

# Refresh Tare Button state
paint_tare_button('READY', mylcd)

while True:
    
    #
    # Now lets try reading our own peripheral (strain gauges set up as a weight scale)
    #

    while hx.is_ready() :
        continue

    # Read raw data
    current_sensor_counts = hx.read()
    print('Raw sensor counts: ' + str(current_sensor_counts))

    # Convert to lbs
    pounds = sensor_lbs(tare_count, current_sensor_counts)
    # print('sensor lbs are: ' + str(pounds))

    # Apply current tare
    pounds = pounds - tare_lbs

    if pounds < 0 :
        pounds = 0

    # Display the reading on the display (320x480)
    # display_number(mylcd, number: int, position_x : int, position_y : int, char_x_width : int, char_y_height : int, color)

    # Erase old number (8 erases all segments in the digit)
    display_number(mylcd, 888, digits_x_pos, digits_y_pos, digit_width, digit_height, BLACK)

    # Draw new number
    display_number(mylcd, pounds, digits_x_pos, digits_y_pos, digit_width, digit_height, RED)

    # print('Displayed ' + str(pounds))

    #
    # Now lets check the touch screen
    #
    # Not sure how touch is really using this
    coord = [0xFFFF, 0xFFFF]
    loopcount = 0

    while True :

        # Instead of just delay, we will read the touch screen here while the number
        # shows for a bit (it has pretty bad flicker when updating, it is a really slow display)
        # 5 reads is about a second.  The touch screen is slow also.

        loopcount += 1
        if loopcount > 45 :
            break

        if mytouch.Touch_Pressed(coord, 200) :

            # print('Got Touch: ' + str(coord))

            mytouch.Read_Touch(coord, 200)

            x = coord[0]
            y = coord[1]

            #
            # Look for Tare button press
            #
            
            if pressed_tare_button(x, y) :
                print('Tare touch: ' + str(coord))

                # Toggle the tare button color to busy
                paint_tare_button('IN_PROGRESS', mylcd)
                
                # Get the new tare 
                tare_count = get_sensor_tare_raw_counts(hx) # Done at boot or with button push
                tare_lbs = get_tare_lbs(dolly_tare_state, cart_tare_state)

                # Toggle the tare button color to normal
                paint_tare_button('READY', mylcd)

                # Display the Tare info string
                display_tare_info(mylcd, tare_lbs)
                display_sensor_info(mylcd, tare_count)

                print('New Tare: ' + str(tare_lbs))

            #
            # Look for Dolly button push
            #
            
            if pressed_dolly_button(x, y) :
                print('Joleen, Joleen! : ' + str(coord))

                dolly_tare_state = not dolly_tare_state

                # Display the right dolly state button
                if dolly_tare_state :
                    paint_dolly_button('ON', mylcd)

                    # Dolly tare on forces cart tare off
                    cart_tare_state = False
                    paint_cart_button('OFF', mylcd)
                else :
                    paint_dolly_button('OFF', mylcd)

                # Display the Tare info string
                tare_lbs = get_tare_lbs(dolly_tare_state, cart_tare_state)
                display_tare_info(mylcd, tare_lbs)

            #
            # Look for Cart button push
            #

            if pressed_cart_button(x, y) :
                print('Cart touch: ' + str(coord))

                cart_tare_state = not cart_tare_state

                # Display the right dolly state button
                if cart_tare_state :
                    paint_cart_button('ON', mylcd)
                                        
                    # Dolly tare on forces cart tare off
                    dolly_tare_state = False
                    paint_dolly_button('OFF', mylcd)
                else :
                    paint_cart_button('OFF', mylcd)

                # Display the Tare info string
                tare_lbs = get_tare_lbs(dolly_tare_state, cart_tare_state)
                display_tare_info(mylcd, tare_lbs)

            # Debounce the display a little
            Delay_Ms(1000)




  


        






