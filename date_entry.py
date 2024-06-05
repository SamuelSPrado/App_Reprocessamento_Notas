import tkinter as tk
from datetime import datetime

class DateEntry(tk.Entry):
    def __init__(self, master=None, **kwargs):
        self.var = tk.StringVar()
        super().__init__(master, textvariable=self.var, **kwargs)
        self.var.trace_add("write", self.validate_date)

    def validate_date(self, *args):
        value = self.var.get()
        if len(value) == 2:
            if not value.isdigit():
                self.var.set("")
                return
            if int(value) > 31 or int(value) == 0:
                self.var.set("")
                return
            self.var.set(value + "/")
        elif len(value) == 5:
            if not value[3:].isdigit():
                self.var.set(value[:3])
                return
            if int(value[3:]) > 12 or int(value[3:]) == 0:
                self.var.set(value[:3])
                return
            self.var.set(value + "/")
        elif len(value) == 10:
            parts = value.split("/")
            if len(parts) != 3:
                self.var.set("")
                return
            day, month, year = parts
            if not (day.isdigit() and month.isdigit() and year.isdigit()):
                self.var.set("")
                return
            try:
                datetime(int(year), int(month), int(day))
            except ValueError:
                self.var.set("")
                return