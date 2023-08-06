from tkinter import *
import tkinter as Tk
import tkinter.ttk as ttk
import time
from amarettopy.gui.util  import *
from amarettopy import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import logging

logger = logging.getLogger("amarettopy")

class GraphTab(Tk.Frame):

    def __init__(self, amaretto, master=None):

        Tk.Frame.__init__(self, master)
        self.amaretto = amaretto

        self.t0 = None
        self.fig = None

        global tickListener

        tickListener.append(self)
        
        self.refVal = None
        self.state = STATE_UNKNOWN


    def onTick(self, servoStatus):

        if servoStatus is None:
            self.t0 = None
            self.refVal = None
            
            return

        if self.amaretto.has_reference():
            self.refVal = servoStatus[3]
            s = self.amaretto.state()
            d = dict([(STATE_CURRENT_SERVO, 0),
              (STATE_VELOCITY_SERVO, 1),
              (STATE_POSITION_SERVO, 2),
              ])
            self.servoIdx = d[s]

        else:
            self.refVal = None


        t   = time.time()
        if self.t0 is None:
            self.t0  = t
            self.ts   = []
            self.poss = []
            self.vels = []
            self.curs = []
            if self.fig is not None:
                plt.close(self.fig)
            self.fig, self.ax = plt.subplots(3, 1)

        t0 = self.t0

        cur = servoStatus[2]
        vel = servoStatus[1]
        pos = servoStatus[0]

        self.ts.append(t-t0)
        self.curs.append(cur)
        self.vels.append(vel)
        self.poss.append(pos)

        XRANGE =  5 # [sec]

        if t - t0 >= XRANGE:
            for x in self.ts[:]:
                if x < t-t0-XRANGE:
                    del(self.ts[0])
                    del(self.curs[0])
                    del(self.vels[0])
                    del(self.poss[0])
                else:
                    break

        lastsens = [cur, vel, pos]
        sens = [self.curs, self.vels, self.poss]
        labels = ['cur', 'vel', 'pos']
        self.ax[0].tick_params(labelbottom=False)
        self.ax[1].tick_params(labelbottom=False)


        for i in range(3):
            self.ax[i].clear()
            YRANGE2 = 10

            if t - t0 >= XRANGE:
                self.ax[i].set_xlim(t - self.t0 - XRANGE, t-self.t0)
            else:
                self.ax[i].set_xlim(0, XRANGE)

            if self.refVal is not None and self.servoIdx == i:

                yrange = max(YRANGE2, abs(max(sens[i]) - self.refVal), abs(min(sens[i]) - self.refVal))
                self.ax[i].set_ylim(self.refVal-yrange, self.refVal+yrange)

                self.ax[i].plot(self.ts, sens[i], 'b', self.ts, [self.refVal]*len(self.ts), 'r')
                self.ax[i].set_title( labels[i] + '{:5}, ref({:5})'.format(lastsens[i], self.refVal, color='r', fontsize=1))
            else:
                self.ax[i].plot(self.ts, sens[i], 'b')
                self.ax[i].set_title( labels[i] + '{:5}'.format(lastsens[i], color='r', fontsize=1))

        self.ax[2].set_xlabel("Time [sec]", fontsize=10)

        logger.info("Graph values: cur:%s vel:%s pos:%s " % (cur, vel, pos))
        plt.pause(0.01)

