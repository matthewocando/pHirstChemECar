# pHIRST CHEM-E-CAR STOPPING MECHANISM 
## DATA COLLECTION

The script `pressure-sensor.ino` is an arduino script that takes pressure data from the **Sparkfun Qwiic MicroPressure Sensor**, and sends it live through a COM port to which the arduino is connected. When uploaded, pins **A4** and **A5** serve as **SDA** and **SCL** lines respectively.

The script `p_readout.py` provides a GUI for collecting pressure data live. The GUI provides a live pressure readout, as well as a timer. THe `START` button begins data collection, while `STOP` halts it. Pressure data is recorded in approximately 100ms intervals. Data is automatically saved to a .csv after the `SAVE` button is pressed. The .csv name can be specified in the text entry field next to the save option.

The script can also use _polynomial regression_ to fit a polynomial curve to the data. Note that this has been removed temporarly, and will be added when needed.

## IMPORTANT NOTES

1) The COM port needs to be specified in the .py script depending on what port the arduino is connected to. The default is set to COM5.

2) The arduino script does not need to be uploaded each time the arduino is connected, unless some code was changed. There is no need to run the arduino IDE everytime the arduino is connected.

3) The code has been tested on an arduino NANO and arduino UNO and confirmed to work.
