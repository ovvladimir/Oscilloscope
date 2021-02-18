import sys
import time
from tkinter import Button, Tk, scrolledtext, Label, ttk
import serial
import serial.tools.list_ports
from PIL import Image, ImageDraw, ImageFont, ImageTk


def win_close():
    run[0] = False


def com(*args):
    if port_run:
        board.baudrate = int(box.get())
        label['text'] = f'{board.baudrate}   {port_name}'


def icon():
    unicod = '\u0076\u006F'  # 'vo'
    size = 16
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    font = ImageFont.load_default()
    ts = font.getsize(unicod)
    draw.ellipse((0, 0, size - 2, size - 2), fill=(68, 71, 90, 90))
    draw.text(
        ((size - ts[0]) // 2, (size - ts[1]) // 2 - 1),
        unicod, font=font, fill=(255, 0, 0))
    root.iconphoto(False, ImageTk.PhotoImage(im))


port_run = False
for port in list(serial.tools.list_ports.comports()):
    board = serial.Serial(port[0], baudrate=115200, timeout=.1)
    port_name, port_speed = board.port, board.baudrate
    port_run = True
    # print(port)
if not port_run:
    port_name, port_speed = 'COMx', 'NONE'
time.sleep(1)

root = Tk()
root.title('Monitor')
root.geometry('+1+1')
root.protocol('WM_DELETE_WINDOW', win_close)
root.resizable(False, False)
root['bg'] = '#44475a'
text = scrolledtext.ScrolledText(root, font='arial 16', padx=10, fg='white', bg='#44475a')
text.pack(padx=10, pady=10)
box = ttk.Combobox(text, values=("9600", "115200"))
box.place(relx=1, rely=0, anchor='ne')
box.current(0 if port_speed == 9600 else 1)
box.bind("<<ComboboxSelected>>", com)
label = Label(
    text, font='arial 10', bg='#44475a', fg='white', text=f'{port_speed}   {port_name}')
label.place(relx=1, rely=1, anchor='se')
buttton = Button(root, text="Quit", command=win_close)
buttton.pack(fill='x')
text.delete(1.0, 'end')
icon()

run = [True]
while run[0]:
    # data = board.read()
    # if data is not None:
    if port_run and board.in_waiting:
        data = board.readline()
        text.insert('end', data)
        text.see("end")
    root.update()
    # time.sleep(.01)

if port_run:
    board.close()
root.destroy()
sys.exit(0)
