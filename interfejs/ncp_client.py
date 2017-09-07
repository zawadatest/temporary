import serial.tools.list_ports
import ncp
import wx
import struct
import time

class MainWindow(wx.Frame):
		
	def __init__(self, *args, **kw):
		super(MainWindow, self).__init__(*args, **kw)
		
		self.connecton = None
		
		self.port_list = []
		for port in serial.tools.list_ports.comports():
			self.port_list.append(port[0])
		self.port_list.sort()
		
		self.InitUI()
		
	def onFunChange(self, e):
		if 'read' in self.fun_radio.GetStringSelection():
			self.value_text.SetValue('')
			self.value_text.SetEditable(False)
		else:
			self.value_text.SetEditable(True)
			
	def onSendClick(self, e):
		
		if self.connecton is None:
			wx.MessageBox('Not connected', 'Error', wx.OK | wx.ICON_ERROR)
			return
		
		if self.type_radio.GetStringSelection() == 'float' and \
				(self.fun_radio.GetStringSelection() != 'read 32bit' and self.fun_radio.GetStringSelection() != 'write 32bit'):
			wx.MessageBox('Float type required 32bit register', 'Error', wx.OK | wx.ICON_ERROR)
			return
		
		text = self.reg_text.Value
		try:
			if text.startswith('0x'):
				reg = int(text, 16)
			else:
				reg = int(text)
		except ValueError:
			wx.MessageBox('Invalid register address', 'Error', wx.OK | wx.ICON_ERROR)
			return
		
		if 'write' in self.fun_radio.GetStringSelection():
			text = self.value_text.Value
			try:
				
				if self.type_radio.GetStringSelection() == 'float':
					val = float(text)
				elif text.startswith('0x'):
					val = int(text, 16)
				else:
					val = int(text)
			
				if self.type_radio.GetStringSelection() == 'unsigned':
					if self.fun_radio.GetStringSelection() == 'write 8bit':
						val = bytearray(struct.pack('B', val))[0]
					elif self.fun_radio.GetStringSelection() == 'write 16bit':
						val = bytearray(struct.pack('>H', val))
					else:
						val = bytearray(struct.pack('>L', val))
				elif self.type_radio.GetStringSelection() == 'signed':
					if self.fun_radio.GetStringSelection() == 'write 8bit':
						val = bytearray(struct.pack('b', val))[0]
					elif self.fun_radio.GetStringSelection() == 'write 16bit':
						val = bytearray(struct.pack('>h', val))
					else:
						val = bytearray(struct.pack('>l', val))
				elif self.type_radio.GetStringSelection() == 'float':
					val = bytearray(struct.pack('>f', val))
				
			except (ValueError, struct.error):
				wx.MessageBox('Invalid register value', 'Error', wx.OK | wx.ICON_ERROR)
				return
		
		try:
			if self.fun_radio.GetStringSelection() == 'read 8bit':
				read_val = bytearray(self.connecton.read_8bit(reg))
			elif self.fun_radio.GetStringSelection() == 'read 16bit':
				read_val = bytearray(self.connecton.read_16bit(reg))
			elif self.fun_radio.GetStringSelection() == 'read 32bit':
				read_val = bytearray(self.connecton.read_32bit(reg))
			if self.fun_radio.GetStringSelection() == 'write 8bit':
				self.connecton.write_8bit(reg, val)
			elif self.fun_radio.GetStringSelection() == 'write 16bit':
				self.connecton.write_16bit(reg, val)
			elif self.fun_radio.GetStringSelection() == 'write 32bit':
				self.connecton.write_32bit(reg, val)
		except Exception as e:
			self.log.AppendText(time.strftime("%X> ") + str(e) + '\n')
			return
		
		self.log.AppendText(time.strftime("%X> ") + 'Operation successful\n')
		
		if 'read_val' in locals():
			if self.type_radio.GetStringSelection() == 'unsigned':
				if len(read_val) == 1:
					val = struct.unpack('B', read_val)[0]
				elif len(read_val) == 2:
					val = struct.unpack('>H', read_val)[0]
				else:
					val = struct.unpack('>L', read_val)[0]
			elif self.type_radio.GetStringSelection() == 'signed':
				if len(read_val) == 1:
					val = struct.unpack('b', read_val)[0]
				elif len(read_val) == 2:
					val = struct.unpack('>h', read_val)[0]
				else:
					val = struct.unpack('>l', read_val)[0]
			elif self.type_radio.GetStringSelection() == 'float':
				val = struct.unpack('>f', read_val)[0]
			self.value_text.SetValue(str(val))
		
	def onConnectClick(self, e):
		if self.con_button.Label == 'Connect':
			try:
				self.connecton = ncp.NCP(self.port_text.GetStringSelection())
			except Exception:
				wx.MessageBox('Open port error', 'Error', wx.OK | wx.ICON_ERROR)
				return
			self.con_button.SetLabel('Disconnect')
			self.sb.SetStatusText('Connected to ' + self.port_text.GetStringSelection())
		else:
			del self.connecton
			self.connecton = None
			self.sb.SetStatusText('Not connected')
			self.con_button.SetLabel('Connect')
	
	def InitUI(self):

		panel = wx.Panel(self)

		fun_choices = ['read 8bit', 'write 8bit', 'read 16bit', 'write 16bit', 'read 32bit', 'write 32bit']
		self.fun_radio = wx.RadioBox(panel, label = 'NCP function', choices = fun_choices, majorDimension = 2, style = wx.RA_SPECIFY_COLS)
		self.fun_radio.Bind(wx.EVT_RADIOBOX, self.onFunChange)
		
		type_choices = ['unsigned', 'signed', 'float']
		self.type_radio = wx.RadioBox(panel, label = 'Register type', choices = type_choices)
		
		vbox1 = wx.BoxSizer(wx.VERTICAL)
		vbox1.Add(self.fun_radio, 0)
		vbox1.Add(self.type_radio, 0)
		
		reg_label = wx.StaticText(panel, label = 'Register address')
		self.reg_text = wx.TextCtrl(panel)
		value_label = wx.StaticText(panel, label = 'Register value')
		self.value_text = wx.TextCtrl(panel)
		self.value_text.SetEditable(False)
		button = wx.Button(panel, label = 'Send', size=(70, 30))
		button.Bind(wx.EVT_BUTTON, self.onSendClick)
		
		self.con_button = wx.Button(panel, label = 'Connect', size=(100, 30))
		self.con_button.Bind(wx.EVT_BUTTON, self.onConnectClick)
		self.port_text = wx.ComboBox(panel, wx.ID_ANY, choices = self.port_list, style=wx.CB_READONLY)
		
		self.log = wx.TextCtrl(panel,style = wx.TE_MULTILINE|wx.TE_READONLY)
		
		vbox2 = wx.BoxSizer(wx.VERTICAL)
		vbox2.Add(reg_label, 0)
		vbox2.Add(self.reg_text, 0, wx.EXPAND)
		vbox2.Add(value_label, 0)
		vbox2.Add(self.value_text, 0, wx.EXPAND)
		vbox2.Add(button, 0, wx.TOP | wx.CENTER, 10)
		
		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		hbox1.Add(vbox1)
		hbox1.Add(vbox2)
		
		hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		hbox2.Add(self.con_button, 0, wx.ALL | wx.CENTER, 10)
		hbox2.Add(self.port_text, 0, wx.ALL | wx.CENTER, 10)
		
		vbox3 = wx.BoxSizer(wx.VERTICAL)
		vbox3.Add(hbox1)
		vbox3.Add(hbox2)
		vbox3.Add(self.log, 1, wx.ALL | wx.EXPAND, 10)
		
		panel.SetSizer(vbox3)
		
		self.sb = self.CreateStatusBar()
		self.sb.SetStatusText('Not connected')
		
		self.SetTitle("NCP client")
		size = wx.Size(370,400)
		self.SetSize(size)
		self.Centre()
		self.Show(True)
	

app = wx.App()
MainWindow(None)
app.MainLoop()
