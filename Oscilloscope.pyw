import sys
import os

from random import randint
from math import sin
from tkinter import Tk, Canvas, LabelFrame, Button, FLAT, GROOVE, \
    RAISED, SUNKEN, CENTER, W, E, N, messagebox, ttk

import serial
import serial.tools.list_ports

serial_run = False
for port in list(serial.tools.list_ports.comports()):
    SERIAL_PORT, SERIAL_NAME = port[0], port[1]
    serial_run = True
if not serial_run:
    SERIAL_PORT, SERIAL_NAME = 'COMx', 'NONE'
    serial_run = False

data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 't.txt')


class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("Oscilloscope")
        self.window.protocol('WM_DELETE_WINDOW', self.closed)
        self.window.resizable(False, False)

        self.frame = LabelFrame(
            self.window, relief=FLAT, text=SERIAL_NAME, fg='brown')
        self.frame.pack()

        self.can = Canvas(self.frame, borderwidth=2, relief=GROOVE)
        self.can.config(width=500, height=500, background="black")
        self.can.grid(row=0, column=0, columnspan=4, pady=(2, 0))

        self.gbtn1 = Button(self.frame, text="Start", fg='blue')
        self.gbtn1["command"] = self.draw
        self.gbtn1.grid(row=1, column=0, sticky=W + E)

        self.gbtn2 = Button(self.frame, text="Serial", fg='blue')
        self.gbtn2["command"] = self.get_data_from_com
        self.gbtn2.grid(row=1, column=1, sticky=W + E)

        self.gbtn3 = Button(self.frame, text="File", fg='blue')
        self.gbtn3["command"] = self.draw_file
        self.gbtn3.grid(row=1, column=2, sticky=W + E)

        self.gbtn4 = Button(self.frame, text="EXIT", fg='blue')
        self.gbtn4["command"] = self.closed
        self.gbtn4.grid(row=1, column=3, sticky=W + E)

        self.serial_speed = ttk.Combobox(
            self.window, values=("9600", "115200"), state="readonly",
            foreground='brown')
        self.serial_speed.place(relx=1, rely=0, anchor=N + E)
        self.serial_speed.current(1)
        self.serial_speed.bind("<<ComboboxSelected>>", self.com)
        self.serial_speed.bind("<FocusIn>", self.defocus)

        self.draw_axis()
        self.run = False
        self.itable = []
        self.age = 0
        self.ser = None
        self.window.mainloop()

    def message(self):
        self.window.withdraw()
        messagebox.showinfo("", "E X I T")

    def closed(self):
        self.run = False
        # self.message()
        self.window.destroy()

    def defocus(self, *args):
        self.window.focus()

    def com(self, *args):
        if self.run and serial_run:
            self.ser.baudrate = int(self.serial_speed.get())

    def draw(self):
        self.run = False
        self.gbtn2.configure(relief=RAISED)
        self.draw_axis()

        x1, x2, y1, y2 = -10, 10, -10, 10

        dx = (x2 - x1) / 500.
        coords = []

        for i in range(500):
            x = x1 + dx * i
            y = sin(x)
            j = 500 - 500 * (y - y1) / (y2 - y1)
            coords.append(j)

        for i in range(499):
            a = coords[i]
            b = coords[i + 1]
            self.can.create_line(i, a, i + 1, b, fill='green')

    def draw_file(self):
        self.run = False
        self.gbtn2.configure(relief=RAISED)
        self.get_data()

    def draw_axis(self):
        self.can.delete("all")
        self.can.create_line(250, 0, 250, 500, fill='brown')
        self.can.create_line(0, 250, 500, 250, fill='brown')

    def drawdata(self, data, led_):
        self.can.create_oval(
            10, 10, 30, 30,
            fill='red' if led_ else 'black', outline='white', width=3)

        center = 0
        self.itable.append(data)
        i = self.age
        if self.itable[1:]:
            a = self.itable[0]
            b = self.itable[1]

            self.can.create_line(
                i - 1 + center, 500 - a, i + center, 500 - b,
                fill='blue', width=2)

            del self.itable[0]
        self.age += 1

    def get_data(self):
        self.draw_axis()
        self.age = 0
        self.itable.clear()

        with open(data_file, 'w') as f:
            for n in range(500):
                num = randint(n // 2, 400)
                f.write(f'{num} ')

        with open(data_file, 'r') as f:
            dataset = list(map(float, f.read().split()))
            for data in dataset:
                self.drawdata(data, False)

    def get_data_from_com(self):
        self.run = True
        self.gbtn2.configure(relief=SUNKEN)
        self.draw_axis()
        self.age = 0
        self.itable.clear()

        if serial_run:
            serial.speed = int(self.serial_speed.get())
            self.ser = serial.Serial(SERIAL_PORT, serial.speed, timeout=.1)

            while self.run:
                num = ''
                if self.ser.in_waiting:
                    s = self.ser.readline()
                    s = s.decode(errors='ignore')
                    led = True if 'LED ON' in s else False
                    for char in s:
                        if char.isdigit():
                            num = num + char
                    if num == '':
                        num = '250'
                    self.drawdata(float(num), led)
                self.window.update()

            self.ser.close()
        else:
            self.can.create_text(
                250, 250, text="NO CONNECTION", justify=CENTER,
                font="arial 22", fill="white")


def main():
    App()


if __name__ == "__main__":
    main()
    print('[EXIT]')
    sys.exit(0)
