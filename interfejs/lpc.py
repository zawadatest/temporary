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

	def send_cmd(self, dev_addr, reg_addr, data):
		read_addr = dev_addr << 1 | 1
		#write_addr = addr << 1
		#write
		dev_addr = dev_addr << 1
		adr2 = ((reg_addr >> 8) & 0xFF)
		adr1 = ((reg_addr) & 0xFF)
		cmd = [dev_addr]
		cmd.append(adr1)
		cmd.append(adr2)
		cmd.extend(data[0:4])
		bytestring =  ''.join(map(chr, cmd))
		frame = ' '.join('0x{:02x}'.format(x) for x in cmd)
		crc8 = crcmod.predefined.mkCrcFun('crc-8')
		crc = crc8(bytestring, 0x00)
		crc = crc & 0xFF
		crc_str = '0x{:02x}'.format(crc)
		frame_str = '[{} {}[{} r:{}]\n'.format(frame, hex(crc), hex(read_addr), 5 )
		self.serial.write(frame_str)
