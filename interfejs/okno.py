from Tkinter import *
import tkMessageBox
import tkFileDialog
import ttk

class Application(Frame):

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
        Label(self, text="""Set addresses:""").grid(row=0, column=0, sticky=W)
        
        Label(self, text="""Device address""").grid(row=1, column=0, sticky=W)
        self.e = Entry(self, width = 10)
        self.e.grid(row=1, column=1)
        self.e.focus_set()
        
        def callback():
            print self.OnValidate(self.e.get(), 127)

        self.validate = Button(self, text = "validate 7 bit addr", command = callback)
        self.validate.grid(row=1, column=2)
        Label(self, text="""Register address""").grid(row=2, column=0, sticky=W)
        self.e2 = Entry(self, width = 10)
        self.e2.grid(row=2, column=1)
        self.e2.focus_set()
        def callback2():
            print self.OnValidate(self.e2.get(), 65535)
        
        self.validate2 = Button(self, text = "validate 16 bit addr", command = callback2)
        self.validate2.grid(row=2, column=2)
        Radiobutton(self, text="Write", variable=self.v, value=1).grid(row=3, column=0, sticky=W)
        Radiobutton(self, text="Read", variable=self.v, value=2).grid(row=4, column=0, sticky=W)
        Radiobutton(self, text="Upgrade", variable=self.v, value=3).grid(row=5, column=0, sticky=W)
        
        def upgrade():
            print "Upgrade"
            file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Choose a file') 
        
        def browsefunc():
            filename = tkFileDialog.askopenfilename()
            pathlabel.config(text=filename)   
        self.upgrade = Button(self, text = "BROWSE", command = browsefunc)
        self.upgrade.grid(row=5, column=1)
        Label(self, text="""Filepath:""").grid(row=6, column=0, sticky=W)
        pathlabel = Label(self)
        pathlabel.grid(row=6, column=2)
        Label(self, text="""Speed:""").grid(row=7, column=0, sticky=W)
        Label(self, text="""KHz""").grid(row=7, column=2, sticky=W)
        self.box_value = StringVar()
        self.box = ttk.Combobox(self, textvariable=self.box_value)
        self.box['values'] = ('5', '50', '100', '400')
        self.box.current(0)
        self.box.grid(row=7, column=1)
        self.ACTION = Button(self, text = "ACTION", fg = "red")
        self.ACTION.grid(row=9, column=2, sticky=W)
        self.QUIT = Button(self, text = "QUIT", fg = "red", command = self.quit)
        self.QUIT.grid(row=9, column=2, sticky=E)
        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
root.geometry("570x400+300+300")
app = Application(master=root)
app.mainloop()