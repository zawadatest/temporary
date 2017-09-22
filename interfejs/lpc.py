import serial
import time
import crcmod

class LPC:

	def __init__(self, port, speed, baudrate = 115200, timeout = 1):
		self.options = {5 : '1',
					50 : '2',
					100 : '3',
					400 : '4',
		}
		self.speed = self.options[int(speed)]
		self.serial = serial.Serial(port, baudrate, timeout = timeout)

	def enter_in_i2c_mode(self):
		self.serial.write('m\n')
		time.sleep(0.1)
		self.serial.write('4\n')
		time.sleep(0.1)
		self.serial.write('{}\n'.format(self.speed))
		self.serial.flushInput()
		time.sleep(0.1)

	def parse(self, buff):
		words = buff.split()
		data = []
		for c in words:
			if c=="READ:":
				i = words.index('READ:')
				for i in range(i, i+10):
					x = words[i]
					if x.startswith('0x'):
						data.append(x)
				return data
		return

	def write_cmd(self, dev_addr, reg_addr, data):
		dev_addr = dev_addr << 1 #write
		adr2 = ((reg_addr >> 8) & 0xFF)
		adr1 = ((reg_addr) & 0xFF)
		cmd = [dev_addr, adr1, adr2]
		cmd.extend(reversed(data[0:4]))
		bytestring =  ''.join(map(chr, cmd))
		frame = ' '.join('0x{:02x}'.format(x) for x in cmd)
		crc8 = crcmod.predefined.mkCrcFun('crc-8')
		crc = crc8(bytestring, 0x00)
		crc = crc & 0xFF
		crc_str = '0x{:02x}'.format(crc)
		frame_str = '[{} {}]\n'.format(frame, crc_str)
		self.serial.write(frame_str)
		time.sleep(0.1)

	def read_cmd(self, dev_addr, reg_addr):
		self.serial.flushInput()
		dev_addr = dev_addr << 1 #write
		cmd = [dev_addr]
		x = [dev_addr]
		dev_addr = dev_addr | 1 #read
		adr2 = ((reg_addr >> 8) & 0xFF)
		adr1 = ((reg_addr) & 0xFF)
		cmd.append(adr1)
		cmd.append(adr2)
		bytestring =  ''.join(map(chr, cmd))
		frame = ' '.join('0x{:02x}'.format(x) for x in cmd)
		crc8 = crcmod.predefined.mkCrcFun('crc-8')
		crc = crc8(bytestring, 0x00)
		crc = crc & 0xFF
		crc_str = '0x{:02x}'.format(crc)
		frame_str = '[{} [{} r:5]\n'.format(frame, hex(dev_addr))
		self.serial.write(frame_str)
		buff = ''
		while len(buff) < 48:
			buff = self.serial.readline()

		data_array = self.parse(buff)
		if data_array:
			crc_buff = data_array[-1]
			x.append(adr1)
			x.append(adr2)
			x.append(dev_addr)
			x.extend(int(z,16) for z in data_array[:-1])
			bytestring = ''.join(map(chr, x))
			crc = crc8(bytestring, 0x00)
			crc = crc & 0xFF
			crc_data = '0x{:02x}'.format(crc)
			if crc == int(crc_buff, 16):
				data = data_array[-2]
				for i in reversed(data_array[:-2]):
					data += i[2:]
				print data
				return data
			else:
				return 'Bad CRC'
		else:
			return 'Could not read from register'