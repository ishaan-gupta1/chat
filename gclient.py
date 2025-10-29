import socket
import threading
import tkinter as tk
import datetime as dt
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = "192.168.50.8"
PORT = 5052
client.connect((IP, PORT))
print("Connected")

window = tk.Tk()
window.title("Chat")
chatBox = tk.Text(window, state="disabled")
chatBox.pack()
entry = tk.Entry(window)
entry.pack(side=tk.LEFT)
username = "User"


def sendMessage():
    msg = f'{dt.datetime.now().strftime('[%I:%M %p]')} {username}: {entry.get()}'
    if msg:
        try:
            client.sendall(msg.encode("utf-8"))
            chatBox.config(state="normal")
            chatBox.insert(tk.END, f'{msg}\n')
            chatBox.config(state='disabled')
            chatBox.see(tk.END)
            entry.delete(0, tk.END)
        except:
            chatBox.config(state="normal")
            chatBox.insert(tk.END, 'Connection lost\n')
            chatBox.config(state="disabled")
            chatBox.see(tk.END)


entry.bind("<Return>", lambda event: sendMessage())
sendBtn = tk.Button(window, text='send', command=sendMessage)
sendBtn.pack(side=tk.LEFT)


def recieveMessage():
    while 1:
        try:
            reply = client.recv(1024).decode()
            if not reply:
                break
            chatBox.config(state="normal")
            chatBox.insert(tk.END, f'{reply}\n')
            chatBox.config(state="disabled")
            chatBox.see(tk.END)
        except OSError:
            print("Disconnected")
            client.close()
            break

def connect():
    global client
    try:
        client.close()
    except:
        pass
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((IP, PORT))
        threading.Thread(target=recieveMessage, daemon=True).start()
        chatBox.config(state="normal")
        chatBox.insert(tk.END, "Connected\n")
        chatBox.config(state="disabled")
    except:
        chatBox.config(state="normal")
        chatBox.insert(tk.END, "Unable to reach server, try again later\n")
        chatBox.config(state="disabled")


reconnectBtn = tk.Button(window, text='reconnect', command=connect)
reconnectBtn.pack(side=tk.LEFT)

def clear():
    chatBox.delete("1.0", tk.END)


clearBtn = tk.Button(window, text='clear', command=clear)
clearBtn.pack(side=tk.LEFT)

threading.Thread(target=recieveMessage, daemon=True).start()

window.mainloop()

client.close()
