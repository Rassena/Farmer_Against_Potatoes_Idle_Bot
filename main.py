import time
import win32ui

name = "Farmer Against Potatoes Idle" #just an example of a window I had open at the time
w = win32ui.FindWindow( None, name )
t1 = time.time()
count = 0
while count < 1000:
    dc = w.GetWindowDC()
    dc.GetPixel (60,20)
    dc.DeleteDC()
    count +=1
t2 = time.time()
tf = t2-t1
it_per_sec = int(count/tf)
print (str(it_per_sec) + " iterations per second")