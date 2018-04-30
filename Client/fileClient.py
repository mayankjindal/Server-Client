import tkinter as tk
from tkinter import filedialog, messagebox
import socket
import os

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.client = "/home/mayank/Client/"
        self.create_widgets()
        self.connect()

    def connect(self):
        self.host = '10.7.3.128'
        self.port = 5000
        self.s = socket.socket()
        self.s.connect((self.host, self.port))

    def create_widgets(self):
        self.label_1 = tk.Label(self, text="File Path:")
        self.label_1.grid(row=1, column=1)
        self.label_2 = tk.Label(self, text="File Path:")
        self.label_2.grid(row=2, column=1)
        self.entry_1 = tk.Entry(self)
        self.entry_1.grid(row=1, column=2)
        self.entry_2 = tk.Entry(self)
        self.entry_2.grid(row=2, column=2)
        self.browse_1 = tk.Button(self, text="Browse File(For Upload)", command=self.browsefunc)
        self.browse_1.grid(row=1, column=3)
        self.browse_2 = tk.Button(self, text="Send File Path(For Download)", command=self.take_file) 
        self.browse_2.grid(row=2, column=3)
        self.up = tk.Button(self, text = "Upload", command=self.Call_Upload)
        self.down = tk.Button(self, text = "Download", command=self.Call_Download)
        self.up.grid(row=3, column=1)
        self.down.grid(row=3, column=3)
        self.quit = tk.Button(self, text="Quit", fg="red", command=root.destroy)
        self.quit.grid(row=6, column=2)
        #self.yes = tk.Button(self, text="Yes", command=self.yes)
        #self.no = tk.Button(self, text="Yes", command=self.no)

    def browsefunc(self):
        self.up_file = filedialog.askopenfilename()
        self.entry_1.insert(tk.INSERT, self.up_file)
        
    def take_file(self):
        self.down_file = self.entry_2.get()

    def Call_Upload(self):
        self.s.send("U".encode('utf-8'))
        self.Upload()

    def Call_Download(self):
        self.s.send("D".encode('utf-8'))
        self.Download()

    def Download(self):
 
        filename = ''
        temp = ''
        for i in range(len(self.down_file)-1, 0, -1):
            if self.down_file[i] == '/':
                break
            temp += self.down_file[i]
        for i in range(len(temp)-1, -1, -1):
            filename += temp[i]
        print(filename)
        if(filename != 'q'):
            self.s.send(self.down_file.encode('utf-8'))
            data = self.s.recv(1024).decode('utf-8')

            if(data[:6] == 'EXISTS'):
                filesize = int(data[6:])
                message = messagebox.askyesno("Confirm", "File exists, " + str(filesize) + "Bytes, download? (Y/N)? -> ")
                
                if message == True:
                    self.s.send("OK".encode('utf-8'))
                    f = open(self.client+'new_'+filename, 'wb')
                    data = self.s.recv(1024)
                    totalRecv = len(data)
                    f.write(data)
                    while(totalRecv < filesize):
                        data = self.s.recv(1024)
                        totalRecv += len(data)
                        f.write(data)
                        print("{0:.2f}".format((totalRecv/float(filesize))*100)+ "% Done")
                    print("Download Complete!")
                    f.close()
            else:
                print("File Does Not Exist!")
        self.s.close()
        self.connect()

    def Upload(self):
	
        filename = ''
        temp = ''
        for i in range(len(self.up_file)-1, 0, -1):
            if self.up_file[i] == '/':
                break
            temp += self.up_file[i]
        for i in range(len(temp)-1, -1, -1):
            filename += temp[i]
        print(filename)
        filesize = str(os.path.getsize(self.up_file))
        print(filesize)
        if(filename != 'q'):
            self.s.send(self.up_file.encode('utf-8'))
            message = messagebox.askyesno("Confirm", "File exists, " + str(filesize) + "Bytes, upload? (Y/N)? -> ")
            m = str(filesize + "OK")
            print(m)         
            if message == True:

                self.s.send(m.encode('utf-8'))  
                with open(self.up_file, 'rb') as f:
                    bytesToSend = f.read(1024)
                    self.s.send(bytesToSend)
                    totalRecv = len(filesize)
                    while(totalRecv < int(filesize)):
                        totalRecv += len(filesize)
                        bytesToSend = f.read(1024)
                        self.s.send(bytesToSend)
                print("Upload Complete!")
            f.close()
        self.s.close()
        self.connect()

root = tk.Tk()
root.title("File Sharing")
app = Application(master=root)
app.mainloop()

