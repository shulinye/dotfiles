#!/usr/bin/python3

from datetime import datetime, timedelta
from enum import Enum
import os

class Constants(Enum):
    today = datetime.today()
    NOTESDIR = os.path.join('/home/shulinye/',"Notes")
    JOURNALDIR= os.path.join(NOTESDIR,"Journal")
    DIR = os.path.join(JOURNALDIR, today.strftime("%Y/%m"))
    TODAY = os.path.join(DIR, today.strftime("%d.txt"))
    YESTERDAY = os.path.join(JOURNALDIR, (today - timedelta(1)).strftime("%Y/%m/%d.txt"))
    TODO = os.path.join(NOTESDIR, "1_-_to-Do.txt")
    DAILY = os.path.join(NOTESDIR, "1_-_to-Do/Daily_Tasks.txt")
    WEEKLY = os.path.join(NOTESDIR, "1_-_to-Do/Weekly_Tasks.txt")
    DoW = 1

if not os.path.exists(Constants.DIR.value):
    os.mkdir(Constants.DIR.value) #todo, fix permissions
