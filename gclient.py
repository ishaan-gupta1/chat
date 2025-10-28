import socket
import threading
import tkinter as tk
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client.connect(("192.168.x.x", 5052))
print("Connected")

window = tk.Tk()
window.title("Chat")
chatBox = tk.Text(window, state="disabled", width=50, height=15)
chatBox.pack()
entry = tk.Entry(window)
entry.pack(side=tk.LEFT)
username = "User"

def sendMessage():
    msg = f'{username}: {entry.get()}'
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


threading.Thread(target=recieveMessage, daemon=True).start()

window.mainloop()

client.close()