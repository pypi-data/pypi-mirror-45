import sys,os
from tkinter import *
import tkinter.ttk as ttk
import tkinter as Tk
from amarettopy.gui.util  import *
from tkinter import simpledialog
from amarettopy import *
from tkinter import messagebox
import logging

logger = logging.getLogger("amarettopy")

class FaultStatusFrame(Tk.Frame):

    def __init__(self, amaretto, master=None):
        Tk.Frame.__init__(self, master)
        self.amaretto = amaretto

        self.logo_R = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'imgs', "LED-RED.gif"))
        self.logo_O = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'imgs', "LED-OFF.gif"))
        self.logo_G = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'imgs', "LED-GREEN.gif"))

        self.isConnected = False
        self.faults  = 0

        self.states = dict([
            (0x00, "Stable"),
            (0x01, "FOC Duration"),
            (0x02, "Over Voltage"),
            (0x04, "Under Voltage"),
            (0x08, "Over Temperature"),
            (0x10, "Start-up Failure"),
            (0x20, "Stop Timeout"),
            (0x40, "Break In"),
            (0x80, "Software Error"),
            ])

        for i,(k,v) in enumerate(self.states.items()):

            stat =Label(self, text=v, font=("Arial Bold", 8))
            stat.grid(column=2, row=i+1, sticky=N+S+W)

            led = Label(self, image=self.logo_O)
            led.grid(column=1, row=i+1, sticky=N+S+E)


    def lightOff(self):
        led = Label(self, image=self.logo_O)
        led.grid(column=1, row=1, sticky=N+S+E)
        for i,(k,v) in enumerate(self.states.items()):
            led = Label(self, image=self.logo_O)
            led.grid(column=1, row=i+1, sticky=N+S+E)

    def lightOn(self):
        if self.faults == 0:
            led = Label(self, image=self.logo_G)
            led.grid(column=1, row=1, sticky=N+S+E)
            for i,(k,v) in enumerate(self.states.items()):
                if i == 0: continue
                led = Label(self, image=self.logo_O)
                led.grid(column=1, row=i+1, sticky=N+S+E)
        else:
            for i,(k,v) in enumerate(self.states.items()):
                if (k & self.faults) > 0:
                    led = Label(self, image=self.logo_R)
                    led.grid(column=1, row=i+1, sticky=N+S+E)
                else:
                    led = Label(self, image=self.logo_O)
                    led.grid(column=1, row=i+1, sticky=N+S+E)

    def onTick(self, servoStatus):
        if (self.isConnected):
            if (servoStatus is None):
                self.lightOff()
            elif (self.faults != servoStatus[5]):
                self.faults = servoStatus[5]
                self.lightOn()
        elif (servoStatus is not None):
            self.lightOn()

        self.isConnected = servoStatus is not None

class SelectFaultDialog:
    
    def __init__(self, parent):
        top = self.top = Tk.Toplevel(parent)
        top.grab_set()
        top.focus_set()

        self.faults = None

        self.states = dict([
            (0x01, "FOC Duration"),
            (0x02, "Over Voltage"),
            (0x04, "Under Voltage"),
            (0x08, "Over Temperature"),
            (0x10, "Start-up Failure"),
            (0x20, "Stop Timeout"),
            (0x40, "Break In"),
            (0x80, "Software Error"),
            ])

        self.vars = []
        self.checkButtons = []

        for (faultNo, faultName) in self.states.items():
            var = Tk.BooleanVar()
            checkButton = Tk.Checkbutton(top, text=faultName, variable=var)
            checkButton.pack(anchor = "w")
            self.vars.append(var)
            self.checkButtons.append(checkButton)

        self.submitButton = Tk.Button(top, text='Submit', command=self.send)
        self.submitButton.pack()

    def send(self):
        self.faults = 0

        for i, var in enumerate(self.vars):
            if var.get() == True:
                self.faults += list(self.states.keys())[i]

        self.top.destroy()

class ModeControlFrame(Tk.Frame):
    
    def __init__(self, amaretto, master=None):
        Tk.Frame.__init__(self, master)
        self.amaretto = amaretto
        self.currentState = STATE_UNKNOWN
        self.currentTemp = "?"

        self.clearButton= Tk.Button(self, text='ClearFault', width= "10", command=self.clear)
        self.clearButton.pack(pady=5)

        self.holdButton= Tk.Button(self, text='Hold', width= "10", command=self.hold)
        self.holdButton.pack(pady=5)

        self.freeButton= Tk.Button(self, text='Free', width= "10", command=self.free)
        self.freeButton.pack(pady=5)

        self.readyButton= Tk.Button(self, text='Ready', width= "10", command=self.ready)
        self.readyButton.pack(pady=5)

        self.modeSelector()

        self.button= Tk.Button(self,text='SetRef', width= "5", command=self.modal_open)
        self.button.pack()

        self.stopButton= Tk.Button(self, text='Stop', width= "10", command=self.stop)
        self.stopButton.pack(pady=5)

        self.resetButton= Tk.Button(self, text='Reset', width= "10", command=self.reset)
        self.resetButton.pack(pady=5)

        self.setFaultButton= Tk.Button(self, text='SetFault', width= "10", command=self.fault_open)
        self.setFaultButton.pack(pady=5)

        self.calibrationButton= Tk.Button(self, text='Calibration', width= "10", command=self.calibration)
        self.calibrationButton.pack(pady=5)

        self.resetRot= Tk.Button(self, text='ResetRot', width= "10", command=self.reset_rotation)
        self.resetRot.pack(pady=5)

        self.statText = StringVar()
        self.statText.set(state2str(self.currentState))
        self.stat = Label(self, textvariable=self.statText, font=("Arial Bold", 10))
        self.stat.pack(pady=10)

        self.tempText = StringVar()
        self.tempText.set((self.currentTemp,"°C"))
        self.temp =Label(self, textvariable=self.tempText, font=("Arial Bold", 15), fg="black")
        self.temp.pack(pady=10)

    def hold(self):
        
        logger.info("Hold button clicked ")
        tryAmaretto(lambda: self.amaretto.hold(amarettoGuiInfo.targetDevId))

    def free(self):
        
        logger.info("Free button clicked ")
        tryAmaretto(lambda: self.amaretto.free(amarettoGuiInfo.targetDevId))
        logger.info("State free")
    
    def calibration(self):
        
        logger.info("Calibration button clicked ")
        tryAmaretto(lambda: self.amaretto.calibration(amarettoGuiInfo.targetDevId))    

    def ready(self):
        
        logger.info("Ready button clicked ")
        tryAmaretto(lambda: self.amaretto.ready(amarettoGuiInfo.targetDevId))

    def clear(self):
        
        logger.info("Clear button clicked ")
        tryAmaretto(lambda: self.amaretto.clear_fault(amarettoGuiInfo.targetDevId))

    def stop(self):
        
        logger.info("Stop button clicked ")
        tryAmaretto(lambda: self.amaretto.stop(amarettoGuiInfo.targetDevId))

    def reset_rotation(self):
        
        logger.info("ResetRot button clicked ")
        tryAmaretto(lambda: self.amaretto.reset_rotation(amarettoGuiInfo.targetDevId))

    def reset(self):
        
        logger.info("Reset button clicked ")
        tryAmaretto(lambda: self.amaretto.reset(amarettoGuiInfo.targetDevId))

    def fault_open(self):
        
        logger.error("SetFault button clicked")
        inputDialog = SelectFaultDialog(self)
        self.wait_window(inputDialog.top)

        if inputDialog.faults is None:
            return
        
        tryAmaretto(lambda: self.amaretto.fault(amarettoGuiInfo.targetDevId, inputDialog.faults))
        logger.error("Fault Error1 %s" % str(inputDialog.faults))

    def modal_open(self):
        answer = simpledialog.askfloat("Input", "RefVal = ", parent=self,
                                        minvalue= -100000.0, maxvalue=100000.0)
        if answer is None:
            return
        if not self.amaretto.is_open():
            messagebox.showerror('error', 'no connection   ')
            logger.error('Connection Error')
            return

        ret = None
        if self.mode == 'current':
            ret = tryAmaretto(lambda: self.amaretto.set_ref_current(amarettoGuiInfo.targetDevId, answer))
            logger.info("Current: %s" %answer)
        elif self.mode == 'velocity':
            ret = tryAmaretto(lambda: self.amaretto.set_ref_velocity(amarettoGuiInfo.targetDevId, answer))
            logger.info("velocity: %s" %answer)
        elif self.mode == 'position':
            ret = tryAmaretto(lambda: self.amaretto.set_ref_position(amarettoGuiInfo.targetDevId, answer))
            logger.info("Position: %s" %answer)

    def modeSelector(self):
        self.mode = 'velocity'
        self.box_value = StringVar()
        self.box = ttk.Combobox(self, textvariable=self.box_value, width= "10")
        self.box.bind("<<ComboboxSelected>>",self.on_select)
        self.box['values'] = ['current', 'velocity', 'position']
        self.box.current(1)
        self.box.pack(pady=5)
        logger.info("Mode Selector")
    def on_select(self, event):
        logger.info("Reference Mode Selected")
        self.mode = self.box.get()
        logger.info("Mode: %s" %self.mode)
    def updateStatus(self):
        self.statText.set(state2str(self.currentState))
        logger.info("current servo status: %s" %self.currentState)

    def updateTemp(self):
        self.tempText.set((self.currentTemp,"°C"))

    def onTick(self, servoStatus):
        if servoStatus is not None:
            newState = self.amaretto.state()
            logger.info('Servo status: %s'%newState)

            if (servoStatus[4] != self.currentTemp):
                self.currentTemp = servoStatus[4]
                self.updateTemp()
                logger.info('CurrentTemp: %s'%self.currentTemp)

            if newState != self.currentState:
                self.currentState = newState
                self.updateStatus()
                logger.info('Newstate-updatestatus %s'%self.updateStatus())


class SidePanel(Tk.Frame):

    def __init__(self, amaretto, master):
        Tk.Frame.__init__(self, master)

        global tickListener
        tickListener.append(self)

        self.modeControl = ModeControlFrame(amaretto, self)
        self.modeControl.pack()
        self.faultsStatus = FaultStatusFrame(amaretto, self)
        self.faultsStatus.pack()

    def onTick(self, servoStatus):
        self.modeControl.onTick(servoStatus)
        self.faultsStatus.onTick(servoStatus)


