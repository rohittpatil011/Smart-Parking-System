import RPi.GPIO as GPIO
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont

# OLED display setup
RST = None
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# IR sensor setup (modify pin numbers for each sensor)
IR_PIN1 = 17
IR_PIN2 = 27  # Change this pin number for the second sensor

GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_PIN1, GPIO.IN)
GPIO.setup(IR_PIN2, GPIO.IN)

try:
  while True:
    # Read the state of both IR sensors
    ir_state1 = GPIO.input(IR_PIN1)
    ir_state2 = GPIO.input(IR_PIN2)
  
    # Clear the image
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Check slot 1 and draw text accordingly
    if ir_state1 == GPIO.HIGH:
      text1 = "Slot 1 : Empty"
    else:
      text1 = "Slot 1 : Occupied"
    draw.text((0, 0), text1, font=font, fill=255)

    # Check slot 2 and draw text accordingly (adjust position for better layout)
    if ir_state2 == GPIO.HIGH:
      text2 = "Slot 2 : Empty"
    else:
      text2 = "Slot 2 : Occupied"
    draw.text((width // 2, 0), text2, font=font, fill=255)

    # Update the OLED display
    disp.image(image)
    disp.display()

    # Delay for stability
    time.sleep(0.1)

except KeyboardInterrupt:
  GPIO.cleanup()