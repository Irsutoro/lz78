import tkinter as tk
import lz78
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import ast

state = 'none'
res = None

top = tk.Tk()

input_frame = tk.Frame(top)
input_frame.pack()

button_frame = tk.Frame(top)
button_frame.pack()

output_frame = tk.Frame(top)
output_frame.pack()

last_frame = tk.Frame(top)
last_frame.pack()

input_label = tk.Label(input_frame, text="Dane wejściowe")
input_label.pack( side = tk.LEFT)
input_entry = tk.Entry(input_frame, bd =5)
input_entry.pack(side = tk.RIGHT)

decode_button = tk.Button(button_frame, text ="Decode from file", command = lambda: decode_from_file())
decode_button.pack(side = tk.LEFT)

encode_file_button = tk.Button(button_frame, text ="Encode file", command = lambda: encode_file())
encode_file_button.pack(side = tk.LEFT)

output = tk.Text(output_frame, height=20)
output.pack()

def encode_file():
    filename = askopenfilename()
    file = open(filename, "r")
    text = file.read()
    file.close()
    result = lz78.encode(text)
    output.delete('1.0', tk.END)
    output.insert(tk.INSERT, repr(result))
    global state
    global res
    state = 'encoded'
    res = result

def encode(data):
    result = lz78.encode(data)
    output.delete('1.0', tk.END)
    output.insert(tk.INSERT, repr(result))
    global state
    global res
    state = 'encoded'
    res = result

def decode(data):
    global state
    state = 'decoded'
    inp = ast.literal_eval(data)
    result = lz78.decode(inp)
    output.delete('1.0', tk.END)
    output.insert(tk.INSERT, result)
    global res
    res = result

def decode_from_file():
    global state
    state = 'decoded'
    filename = askopenfilename()
    result = lz78.decode(lz78.from_file(filename))
    output.delete('1.0', tk.END)
    output.insert(tk.INSERT, result)
    global res
    res = result


encode_button = tk.Button(button_frame, text ="Encode", command = lambda: encode(input_entry.get()))
encode_button.pack(side = tk.LEFT)

decode_button = tk.Button(button_frame, text ="Decode", command = lambda: decode(input_entry.get()))
decode_button.pack(side = tk.LEFT)

def save(data, filename):
    if filename:
        if state == 'decoded':
            file = open(filename, "w")
            file.write(data)
            file.close()
        elif state == 'encoded':
            lz78.to_file(data, filename)



filename_label = tk.Label(last_frame, text="Filename")
filename_label.pack(side = tk.LEFT)
filename_entry = tk.Entry(last_frame, bd =5)
filename_entry.pack(side = tk.LEFT)

save_to_file_button = tk.Button(last_frame, text = "Save", command = lambda: save(res, filename_entry.get()))
save_to_file_button.pack(side = tk.LEFT)


top.mainloop()


