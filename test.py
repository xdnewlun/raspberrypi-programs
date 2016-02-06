import signal as sig
from time import  sleep
from lcd import LCD
run = True

def on_exit(a,b):
    global run
    run = False
    
sig.signal(sig.SIGINT,on_exit)
print("Ctrl+C to exit")

# see comments in lcd.py
lcd = LCD(22,21,17,23,25,24)

# change these line to test
# 1st line = 0
# 2nd line = 1
#lcd.set_cursor(0,2) # line,column
#lcd.send_string('Xander Newlun')
lcd.set_cursor(0,2)
lcd.send_string('Hello World')
while run:
    sleep(1)
    
lcd.close()
print('Done')