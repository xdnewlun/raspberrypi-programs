# lcd.py
# written by Roger Woollett

import RPi.GPIO as gp
from time import sleep

gp.setwarnings(False)
class LCD():
   # class to control a Hitachi type LCD display
   # It should work for 16 or 20 character by 2 or 4 line displays

   row_offsets16 = (0,0x40,0x10,0x50)
   row_offsets20 = (0,0x40,0x14,0x54)
   cmd_set_address = 0x80
   cmd_clear = 0b00000001
   cmd_8bit = 0b00110000
   cmd_4bit = 0b00100000
   cmd_on = 0b00001000
   cmd_mode = 0b00000100
   cmd_8bit_init = 0b0011
   cmd_4bit_init = 0b0010

   def __init__(self,p1,p2,p3,p4,cmd,strobe,d20x4 = False):
      # p1 is most significant bit (pin 14 on the LCD)
      # cmd is pin 4 on the LCD
      # strobe is pin 6 on the LCD
      # 20 char by 4 line screens need different offsets
      # so set d20x4 True for these screens
      
      gp.setmode(gp.BCM)
      
      self.data_pins = (p4,p3,p2,p1)
      self.cmd_reg = cmd
      self.strobe = strobe
      
      for pin in self.data_pins:
         gp.setup(pin,gp.OUT)
      
      gp.setup(cmd,gp.OUT)
      gp.setup(strobe,gp.OUT)
      
      if d20x4:
         self.row_offsets = LCD.row_offsets20
      else:
         self.row_offsets = LCD.row_offsets16
      
      self.init()
      
   def init(self):
      # called once 
      # this sequence seems to be what is required
      # and it seems to work
      # python + pigpio seems to be slow enough not to need delays
      self._set_data(False)            # set command mode
      self._send_nibble(LCD.cmd_8bit_init) # set 8 bit mode
      self._send_nibble(LCD.cmd_8bit_init) # and again
      self._send_nibble(LCD.cmd_8bit_init) # and again

      self._send_nibble(LCD.cmd_4bit_init)  # switch to 4 bit
      self._send_command(LCD.cmd_4bit | 0b1000) # set two line mode
      
      self.on()
      
   def on(self,on = True,cursor = False,blink = False):
      # turn screen on and set cursor details
      self._send_command(LCD.cmd_on |(on << 2) | (cursor << 1) | blink)
      
   def clear(self):
      # clear the screen
      self._send_command(LCD.cmd_clear)
      
   def send_string(self,text):
      # send string to current cursor position
      self._set_data(True)
      for ch in (text):
         self._send_byte(ord(ch))
         
   def send_char(self,char):
      # send a single character to the display
      # normal code will use send_string
      self._send_data(char)
      
   def entry_mode(self,shift = False,leftshift = False):
      # sets if new data shifts display and which way
      self._send_command(LCD.cmd_entry_mode | (leftshift <<1) | shift)
         
   def set_cursor(self,row,column):
      address = column + self.row_offsets[row]
      self._send_command(LCD.cmd_set_address | address)
      
   def _send_command(self,cmd):
      self._set_data(False)
      self._send_byte(cmd)
      
   def _send_data(self,data):
      self._set_data(True)
      self._send_byte(data)
      
   def _send_byte(self,data):
      self._send_nibble((data & 0xf0) >> 4)
      self._send_nibble(data & 0xf)
      
   def _set_data(self,data):
      # call with True for Data, False for command
      gp.output(self.cmd_reg,data)
      
   def _send_nibble(self,data):
      gp.output(self.strobe,1)
      sleep(0.001)
      for i in range(0,4):
         gp.output(self.data_pins[i],(data >> i) & 1)
      #sleep(0.001)
      gp.output(self.strobe,0)
      
         
   def close(self):
      self.clear()
      
      # clear data pins
      for i in range(0,4):
         gp.output(self.data_pins[i],0)
      
      gp.cleanup()   