import time
from tkinter import Button, Tk, scrolledtext, Label, ttk
import serial
import serial.tools.list_ports
import sys


def win_close():
    run[0] = False


def com(*args):
    board.baudrate = int(box.get())
    label['text'] = f'{board.baudrate}   {board.port}'


for port in list(serial.tools.list_ports.comports()):
    board = serial.Serial(port[0], baudrate=115200, timeout=.1)
    # print(port)
time.sleep(2)

root = Tk()
# root.withdraw()  # не показывать окно
root.title('Monitor')
root.geometry('+1+1')
root.protocol('WM_DELETE_WINDOW', win_close)
root.resizable(False, False)
root['bg'] = '#44475a'
text = scrolledtext.ScrolledText(root, font='arial 16', padx=10, fg='white', bg='#44475a')
text.pack(padx=10, pady=10)
box = ttk.Combobox(text, values=("9600", "115200"))
box.place(width=105, relx=0.9, rely=0)
box.current(0 if board.baudrate == 9600 else 1)
box.bind("<<ComboboxSelected>>", com)
label = Label(
    text, font='arial 10', bg='#44475a', fg='white', text=f'{board.baudrate}   {board.port}')
label.place(relx=0.9, rely=0.04)
buttton = Button(root, text="Quit", command=win_close)
buttton.pack(fill='x')
text.delete(1.0, 'end')

run = [True]
while run[0]:
    # data = board.read()
    # if data is not None:
    if board.in_waiting:
        data = board.readline()
        text.insert('end', data)
        text.see("end")
    root.update()
    # time.sleep(.01)

board.close()
root.destroy()
sys.exit(0)
