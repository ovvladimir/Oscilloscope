import sys
import time
from tkinter import Button, Tk, scrolledtext, Label, ttk, PhotoImage
import serial
import serial.tools.list_ports


def win_close():
    run[0] = False


def com(*args):
    if port_run:
        board.baudrate = int(box.get())
        label['text'] = f'{board.baudrate}   {port_name}'


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
root.iconphoto(False, PhotoImage(
    data='iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAE+ElEQVRYR8V'
    'XbVBUVRg+59zd5WP5RiSIERAcdjFTUECibS8IFNYwwg4D09RMSj9sJst+NTpo/Wh'
    'qpqYfOWN/+iAjdQIB04xAxUVkYpGQaQERWClQCoUV+TDg7jm3c4BLd5dFPmRm75/'
    'de9/3vuc5z/O+7z0vBMu8eJ5XCIqgUIWIgjkR+GMA1RACFXtdFME0B8QJDMEDGyS'
    'DStv9AaPRaFtOaLiUE8/neWEEYpUcCgcAKZbyn7UTm4DJXxwBHUZj2fjj3nkMgDy'
    'O58EWwHExCEG0vIXtvQgRCcD4ltEIzACUYWcxnAJguxYR0nEc8lvNwo7vYExGICH'
    '1zthYAGAbv8fPF7mnchx0X4vFpRgYi5MPyeSVVuPZEXlcOwCzO+cy1npxOQhI8EU'
    '5EzIAeZw+DWWuFe2LscfkqKslNVJOzAOgu9+GlArtWtK+WCwi2G5SFlqZfQYAo55'
    'm+8urzfaVgp6rjgtMihkAurS8RCWniFppoCfxF7DNUl9b1gRZh0PK4Bx5k4mztGm'
    'eHrmn6QyNaOoJ2TjguJCu43qi779joddi4mpGvPwfSXYoCCil+0bC+odWjUIkHpN'
    'K1VBXSKSpMyyqfyFYYiPCYCVMSc/b4AYVKXKH7T1/xCb0thfd8/Gvrkh66YTchmw'
    '2uM9Y/qUI4fQ3vOFdKt2MWT0x7mZornnfc3pKQ29pdwYCpVdFf0nfupCTVXF8lSO'
    'IKdHWAPW78hM4hKLtapPupLCu4rgIASnWG94mCgWNM3sxdpJum48O+gT+XJmUeUp'
    '6nmOqeTV4dPgVq9r76qUtz5VYPX0ntHcsEcmW1oNKjNfVaRMPOTKBCemBaWn5mYB'
    'DgY7oDL9V7Q0aH8lojH72w9bIzV2S3WCqfj1o1JrVsCnuiDlCY5Gev3m59AskEvU'
    'JXfZbU26egvRc396YrB3oPTDgF1R+LiG93G4dTIZhamp+LlQgN0cAkgyDPgFVlUk'
    'vlszYMQaFxvJjjGI5/cy0/+Lp76eUqrvFvOGQPJa2vytC3/n7x0NefrVnkrO+ltt'
    'Yd4T8roJ8Z+U3pzWVAWK62AGm9TN/3tr4fHfLR39T+n+S0T8HoIQmXf93vOGwfBF'
    'Nf08433n9E6uX35XS5Kyv5DZWjosCYI65VIb1VIaG6K0fmCNju7NNNQWho8PZ1zb'
    'FF7VFxNyWB6MMrA6APq0gZ7HeH9/Tpk3sNR+hMlyo3JF+cl9dxedQFDnKyEEp+yU'
    'QS0kwTCUocybBYknIAjMZ9hrLjwMIBaNmx6cZHabP/vEJPH82KfO0Y84UXi49xon'
    'Es/iFnP2Cym3+NKRrb9q5ecDyzl2/oIrzCelnFiShszKUOxlMv74RNPogk5ZXfcD'
    'EmO5qTHxRxwZ7+pl/jqn6teBR6+4htW9t9VbdD2Nq78mYO5awlK6W91TY9hQrw5t'
    'hUX12ScjK0FkjkjvF9dK67zEfZZk/zXH3v9UvpJ/5+46PeuxpvnTYQ5hiLR0TCKe'
    'QKHowW19A8I+/bE8758jaTCNy1orljkyG3TfqcumZDA17+/Q2aBKaHQNJ9yphmkv'
    'pbNkZOG6NVWLi/kipGrYEhzc6Juys/1wrZn9d+jFiAFz+OZ4D4boDyawmLj6SSVK'
    '48FA6y4NLj+VSObl0MPm/xl04mskbzfxwCuhwyi1zOMV0OAVPPJza9zu78RwBf4C'
    'hmsyN54iO54Cj4zlZ+Xj+H/3+j8E4wZA4AAAAAElFTkSuQmCC'))

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
