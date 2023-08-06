from tkinter import messagebox
import sys,os
from amarettopy import *
import logging

logger = logging.getLogger("amarettopy")

class AmarettoGuiInfo:
    targetDevId = 1

amarettoGuiInfo = AmarettoGuiInfo()
tickListener = []

def tryAmaretto(f):
    try:
        return f()
    except MCPError as e:
        messagebox.showerror('communication exception', e.__class__.__name__)

        logger.error('communication exception: %s'%e.__class__.__name__)
    except Exception as e:
        messagebox.showerror('exception',str(e))
        
        logger.error('exception: %s'% str(e))
    return None
