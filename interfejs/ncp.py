import serial

CMD_READ_8BIT   = 1
CMD_READ_16BIT  = 134
CMD_READ_32BIT  = 136
CMD_WRITE_8BIT  = 2
CMD_WRITE_16BIT = 135
CMD_WRITE_32BIT = 137
CMD_READ_TXA    = 7
CMD_WRITE_TXA   = 13

class NCP:

	def __init__(self, port, baudrate = 115200, timeout = 1):
		self.serial = serial.Serial(port, baudrate, timeout = timeout)

	def send_cmd(self, cmd, data):

		# Prepare frame and send
		frame = [170]					# start byte
		frame.append(cmd)				# command
		if cmd > 127:
			frame.append(len(data))		# size
		for byte in data:				# rest of data
			frame.append(byte)
		frame.append(self._crc(frame))  # CRC
		self.serial.write(bytearray(frame))

		# Check response
		if cmd == CMD_READ_16BIT or cmd == CMD_WRITE_16BIT:
			read_len = 8
		elif cmd == CMD_READ_32BIT or cmd == CMD_WRITE_32BIT:
			read_len = 12
		else:
			read_len = 5
		resp = list(bytearray(self.serial.read(read_len)))
		if len(resp) < 5:
			raise Exception('Receive timeout')
		if resp[-1] != self._crc(resp[:-1]):
			raise Exception('Invalid response CRC')
		if resp[1] != cmd:
			raise Exception('Response error "%s"' % (self._error(resp[2])))
		
		# Return value
		return resp[2:-1]
	
	def read_8bit(self, reg):
		if reg > 255:
			raise Exception("8bit register address should be < 256")
		val = self.send_cmd(CMD_READ_8BIT, [reg, 0])[1]
		return [val]
	
	def read_16bit(self, reg):
		if reg > 65535:
			raise Exception("16bit register address should be < 65536")
		val = self.send_cmd(CMD_READ_16BIT, [(reg >> 8) & 0xFF, reg & 0xFF])[3:5]
		return val
	
	def read_32bit(self, reg):
		val = self.send_cmd(CMD_READ_32BIT, [(reg >> 24) & 0xFF, (reg >> 16) & 0xFF, (reg >> 8) & 0xFF, reg & 0xFF])[5:9]
		return val
	
	def write_8bit(self, reg, val):
		if reg > 255:
			raise Exception("8bit register address should be < 256")
		val = self.send_cmd(CMD_WRITE_8BIT, [reg, val])[1]
		return [val]
	
	def write_16bit(self, reg, val):
		if reg > 65535:
			raise Exception("16bit register address should be < 65536")
		val = self.send_cmd(CMD_WRITE_16BIT, [(reg >> 8) & 0xFF, reg & 0xFF, val[0], val[1]])[3:5]
		return val
	
	def write_32bit(self, reg, val):
		val = self.send_cmd(CMD_WRITE_32BIT, [(reg >> 24) & 0xFF, (reg >> 16) & 0xFF, (reg >> 8) & 0xFF, reg & 0xFF, val[0], val[1], val[2], val[3]])[5:9]
		return val

	def _error(self, error):
		return {
			1 : 'function not supported',
			2 : 'register or operation not supported',
			3 : 'incorrect CRC',
			4 : 'one desired value  is out of range',
			5 : 'desired order was not executed',
			6 : 'register read only',
			7 : 'read/write EEPROM memory error',
			8 : 'timeout'
		} [error]

	def _crc(self, buff):
		crc = 0xFF
		for byte in buff:
			crc = crc ^ byte
		return crc
