from Tkinter import *
import tkMessageBox
import tkFileDialog
import ttk
import serial.tools.list_ports
import lpc

class Application(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.connection = None
        self.port_list = []
        for port in serial.tools.list_ports.comports():
            self.port_list.append(port[0])
        self.port_list.sort()
        self.pack()
        self.createWidgets()

    def OnValidate(self, addr, maxN, entry):
        reg = 0
        try:
            if addr.startswith('0x'):
                reg = int(addr, 16)
                if reg > maxN:
                    tkMessageBox.showerror('Error', 'Invalid {}.'.format(entry))
                    return None   
            elif addr.startswith('0'):
                reg = int(addr, 8)
                if reg > maxN:
                    tkMessageBox.showerror('Error', 'Invalid {}.'.format(entry))
                    return False
            else:
                reg = int(addr)
                if reg > maxN:
                    tkMessageBox.showerror('Error', 'Invalid {}.'.format(entry))
                    return False
        except ValueError:
            tkMessageBox.showerror('Error', 'Invalid {}.'.format(entry))
            return False
        return reg

    def createWidgets(self):
        Label(self, text='''Set addresses:''').grid(row=0, column=0, sticky=W)
        Label(self, text='''Device address''').grid(row=1, column=0, sticky=W)
        self.devEntry = Entry(self, width = 10)
        self.devEntry.grid(row=1, column=1, sticky=W)
        self.devEntry.insert(END, '0x5a')
        self.devEntry.focus_set()

        Label(self, text='''Register address''').grid(row=2, column=0, sticky=W)
        self.regEntry = Entry(self, width = 10)
        self.regEntry.grid(row=2, column=1, sticky=W)
        self.regEntry.insert(END, '0')
        self.regEntry.focus_set()
        self.v = IntVar()
        self.v.set(2) # 1-write, 2-read, 3-upgrade
        Radiobutton(self, text='Write', variable=self.v, value=1).grid(row=3, column=0, sticky=W)
        Radiobutton(self, text='Read', variable=self.v, value=2).grid(row=4, column=0, sticky=W)
        Radiobutton(self, text='Upgrade', variable=self.v, value=3).grid(row=5, column=0, sticky=W)
        t = StringVar()
        self.writeEntry = Entry(self, width = 40, textvariable=t)
        self.writeEntry.grid(row=3, column=1, columnspan=3, rowspan =2, sticky=W)
        t.set('Write data')
        self.writeEntry.focus_set()

        def browsefunc():
            filename = tkFileDialog.askopenfilename()
            pathlabel.config(text=filename)   
        Button(self, text = 'BROWSE', command = browsefunc).grid(row=5, column=1)
        Label(self, text='''Filepath:''').grid(row=6, column=0, sticky=W)
        pathlabel = Label(self)
        pathlabel.grid(row=6, column=1, columnspan=2, sticky=W)
        Label(self, text='''Speed:''').grid(row=7, column=0, sticky=W)
        Label(self, text='''KHz''').grid(row=7, column=2, sticky=W)
        self.speedbox_value = StringVar()
        self.speedbox = ttk.Combobox(self, textvariable=self.speedbox_value, values=[5, 50, 100, 400])
        self.speedbox.current(0)
        self.speedbox.grid(row=7, column=1)

        def startConnect():
            if self.connect['text'] == 'Connect':
                try:
                    self.connection = lpc.LPC(self.combox.get(), self.speedbox.get())
                except Exception:
                    tkMessageBox.showerror('Error', 'Open port error')
                    return
                self.connection.enter_in_i2c_mode()
                self.connect.config(text = 'Disconnect')
                self.status.config(text ='Connected to {}'.format(self.combox.get()))
            else:
                del self.connection
                self.connection = None
                self.status.config(text = 'Not connected')
                self.connect.config(text = 'Connect')

        self.connect = Button(self, text = 'Connect', command = startConnect)
        self.connect.grid(row=8, column=0)
        self.combox_value = StringVar()
        self.combox = ttk.Combobox(self, textvariable=self.combox_value, values=self.port_list)
        self.combox.current(0)
        self.combox.grid(row=8, column=1)
        def action():
            dev_val = self.OnValidate(self.devEntry.get(), 127, 'device address')
            reg_val = self.OnValidate(self.regEntry.get(), 65535, 'register address')
            write_val = None
            opt = self.v.get()
            if dev_val != None and reg_val != None:           
                # try:
                if self.connection == None:
                    tkMessageBox.showerror('Error', 'sdfsdf')
                if opt == 1: #write
                    write_val = self.OnValidate(self.writeEntry.get(), 4294967295, 'write value')
                    val = [(write_val >> 24) & 0xFF, (write_val >> 16) & 0xFF, (write_val >> 8) & 0xFF, write_val & 0xFF]
                    self.connection.write_cmd(dev_val, reg_val, val)
                elif opt == 2: #read                        
                    data = self.connection.read_cmd(dev_val, reg_val)
                    t.set(str(data))
                elif opt == 3: #upgrade
                    return  
                # except Exception:
                #     tkMessageBox.showerror('Error', 'Action problem')
                #     return
        self.ACTION = Button(self, text = 'ACTION', fg = 'red', command = action).grid(row=9, column=2, sticky=W)
        self.QUIT = Button(self, text = 'QUIT', fg = 'red', command = self.quit).grid(row=9, column=3, sticky=W)
        self.status = Label(self, text='Not connected', bd=1, relief=SUNKEN, anchor=W)
        self.status.grid(row=20, column=0, columnspan=10, sticky=W)
        
root = Tk()
root.geometry('570x400+300+300')
root.option_add('*Dialog.msg.width', 30)
app = Application(master=root)
app.mainloop()