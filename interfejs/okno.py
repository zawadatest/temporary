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

    def OnValidate(self, addr, maxN):
        reg = 0
        try:
            if addr.startswith('0x'):
                reg = int(addr, 16)
                if reg > maxN:
                    tkMessageBox.showerror('Invalid register address', 'Error')   
                    return     
            elif addr.startswith('0'):
                reg = int(addr, 8)
                if reg > maxN:
                    tkMessageBox.showerror('Invalid register address', 'Error')
                    return
            else:
                reg = int(addr)
                if reg > maxN:
                    tkMessageBox.showerror('Invalid register address', 'Error')
                    return
        except ValueError:
            tkMessageBox.showerror('Invalid register address', 'Error')
            return

        return reg

    def createWidgets(self):
        self.v = IntVar()
        Label(self, text='''Set addresses:''').grid(row=0, column=0, sticky=W)
        
        Label(self, text='''Device address''').grid(row=1, column=0, sticky=W)
        self.devEntry = Entry(self, width = 10)
        self.devEntry.grid(row=1, column=1)
        self.devEntry.focus_set()
        
        def callback():
            print self.OnValidate(self.devEntry.get(), 127)

        self.validate = Button(self, text = 'validate 7 bit addr', command = callback)
        self.validate.grid(row=1, column=2)
        Label(self, text='''Register address''').grid(row=2, column=0, sticky=W)
        self.regEntry = Entry(self, width = 10)
        self.regEntry.grid(row=2, column=1)
        self.regEntry.focus_set()
        def callback2():
            print self.OnValidate(self.regEntry.get(), 65535)
        
        self.validate2 = Button(self, text = 'validate 16 bit addr', command = callback2)
        self.validate2.grid(row=2, column=2)
        Radiobutton(self, text='Write', variable=self.v, value=1).grid(row=3, column=0, sticky=W)
        self.writeEntry = Entry(self, width = 10)
        self.writeEntry.grid(row=3, column=1)
        self.writeEntry.focus_set()
        def callback3():
            print self.OnValidate(self.writeEntry.get(), 4294967295)
        self.validate3 = Button(self, text = 'validate 32 bit', command = callback3)
        self.validate3.grid(row=3, column=2)

        Radiobutton(self, text='Read', variable=self.v, value=2).grid(row=4, column=0, sticky=W)
        Radiobutton(self, text='Upgrade', variable=self.v, value=3).grid(row=5, column=0, sticky=W)
        
        def upgrade():
            print 'Upgrade'
            file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Choose a file') 
        self.status = Label(self, text='Not connected', bd=1, relief=SUNKEN, anchor=W)
        self.status.grid(row=20, column=0, columnspan=10, sticky=W)
        
        def browsefunc():
            filename = tkFileDialog.askopenfilename()
            pathlabel.config(text=filename)   
        self.upgrade = Button(self, text = 'BROWSE', command = browsefunc)
        self.upgrade.grid(row=5, column=1)
        Label(self, text='''Filepath:''').grid(row=6, column=0, sticky=W)
        pathlabel = Label(self)
        pathlabel.grid(row=6, column=1, columnspan=2, sticky=W)
        Label(self, text='''Speed:''').grid(row=7, column=0, sticky=W)
        Label(self, text='''KHz''').grid(row=7, column=2, sticky=W)
        self.speedbox_value = StringVar()
        self.speedbox = ttk.Combobox(self, textvariable=self.speedbox_value)
        self.speedbox['values'] =[5, 50, 100, 400]
        self.speedbox.current(0)
        self.speedbox.grid(row=7, column=1)

        def startConnect():
            if self.connect['text'] == 'Connect':
                try:
                    self.connection = lpc.LPC(self.combox.get(), self.speedbox.get())
                except Exception:
                    tkMessageBox.showerror('Open port error', 'Error')
                    return
                self.connection.enter_in_i2c_mode()
                self.connect['text'] = 'Disconnect'
                self.status.config(text ='Connected to {}'.format(self.combox.get()))
            else:
                del self.connection
                self.connection = None
                self.status.config(text = 'Not connected')
                self.connect['text'] = 'Connect'

        self.connect = Button(self, text = 'Connect', command = startConnect)
        self.connect.grid(row=8, column=0)
        self.combox_value = StringVar()
        self.combox = ttk.Combobox(self, textvariable=self.combox_value)
        self.combox['values'] = self.port_list
        self.combox.current(0)
        self.combox.grid(row=8, column=1)
        def action():
            data = self.OnValidate(self.writeEntry.get(), 4294967295)
            val = [(data >> 24) & 0xFF, (data >> 16) & 0xFF, (data >> 8) & 0xFF, data & 0xFF]
            self.connection.send_cmd(int(self.devEntry.get()), int(self.regEntry.get()), val)
        self.ACTION = Button(self, text = 'ACTION', fg = 'red', command = action)
        self.ACTION.grid(row=9, column=2, sticky=W)
        self.QUIT = Button(self, text = 'QUIT', fg = 'red', command = self.quit)
        self.QUIT.grid(row=9, column=2, sticky=E)
        


root = Tk()
root.geometry('570x400+300+300')
app = Application(master=root)
app.mainloop()