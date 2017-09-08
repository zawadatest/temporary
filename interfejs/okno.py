from Tkinter import *
import tkMessageBox
import tkFileDialog
import ttk
import serial.tools.list_ports
import lpc

class Application(Frame):
    def Dialog1Display(self, h, w):
        Dialog1 = Toplevel(self, height=h, width=w)
        Dialog1.title("Error")

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.connection = None
        self.port_list = []
        for port in serial.tools.list_ports.comports():
            self.port_list.append(port[0])
        self.port_list.sort()
        self.aadr=0
        self.pack()
        self.createWidgets()

    def OnValidate(self, addr, maxN, entry):
        reg = 0
        try:
            if addr.startswith('0x'):
                reg = int(addr, 16)
                if reg > maxN:
                    tkMessageBox.showerror('Error', 'Invalid {}.'.format(entry))
                    return False   
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
        return True

    def createWidgets(self):
        self.v = IntVar()
        Label(self, text='''Set addresses:''').grid(row=0, column=0, sticky=W)
        
        Label(self, text='''Device address''').grid(row=1, column=0, sticky=W)
        self.devEntry = Entry(self, width = 10)
        self.devEntry.grid(row=1, column=1, sticky=W)
        self.devEntry.focus_set()
        
        def callback():
            return self.OnValidate(self.devEntry.get(), 127, 'device address')

        Label(self, text='''Register address''').grid(row=2, column=0, sticky=W)
        self.regEntry = Entry(self, width = 10)
        self.regEntry.grid(row=2, column=1, sticky=W)
        self.regEntry.focus_set()
        def callback2():
            return self.OnValidate(self.regEntry.get(), 65535, 'register address')
        
        Radiobutton(self, text='Write', variable=self.v, value=1).grid(row=3, column=0, sticky=W)
        Radiobutton(self, text='Read', variable=self.v, value=2).grid(row=4, column=0, sticky=W)
        Radiobutton(self, text='Upgrade', variable=self.v, value=3).grid(row=5, column=0, sticky=W)
        t = StringVar()
        self.writeEntry = Entry(self, width = 40, textvariable=t)
        self.writeEntry.grid(row=3, column=1, columnspan=3, rowspan =2, sticky=W)
        t.set('write data')
        self.writeEntry.focus_set()
        def callback3():
            return self.OnValidate(self.writeEntry.get(), 4294967295, 'write value')
        
        
        
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
                    tkMessageBox.showerror('Error', 'Open port error')
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
            print self.v.get()
            if callback():
                if callback2():
                    if self.v.get() == 0: #not checked
                        tkMessageBox.showerror('Error', 'Check option')
                        return
                    if self.v.get() == 1:
                        callback3()
                        return
                else:
                    return
            #try:
            if self.v.get() == 1: #write
                data = self.OnValidate(self.writeEntry.get(), 4294967295, 'write value')
                val = [(data >> 24) & 0xFF, (data >> 16) & 0xFF, (data >> 8) & 0xFF, data & 0xFF]
                self.connection.write_cmd(int(self.devEntry.get()), int(self.regEntry.get()), val)
            elif self.v.get() == 2: #read
                print int(self.devEntry.get(),16)
                data = self.connection.read_cmd(int(self.devEntry.get(),16), int(self.regEntry.get()))
                t.set(str(data))
            elif self.v.get() == 3: #upgrade
                return  
            #except Exception:
            #    tkMessageBox.showerror('Error', 'Not connected. You have to connect.')
            #    return
        self.ACTION = Button(self, text = 'ACTION', fg = 'red', command = action)
        self.ACTION.grid(row=9, column=2, sticky=W)
        self.QUIT = Button(self, text = 'QUIT', fg = 'red', command = self.quit)
        self.QUIT.grid(row=9, column=3, sticky=W)
        


root = Tk()
root.geometry('570x400+300+300')
root.option_add('*Dialog.msg.width', 30)
app = Application(master=root)
app.mainloop()