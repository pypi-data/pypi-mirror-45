import RPi.GPIO as GPIO
import smbus, time, datetime, os, essentials

def Command(Command):
    os.system(Command + " > Command.txt")
    read = essentials.read_file("Command.txt")
    os.remove("Command.txt")
    return read


class RPI_16x2LCD:
    def __init__(self):
        """Auto Detects an LCD on creation
        LCD = RPI_16x2LCD()"""

        print("Getting LCD Address")
        alldata = Command("i2cdetect -y 1")
        alldata = alldata.split("\n")[1:]
        self.LCD_Address = ""
        for item in alldata:
            temp = "".join(item.split(":")[1:]).split(" ")
            for part in temp:
                if part != "" and part != "--":
                    print("DETECTED LCD ADR:", part)
                    self.LCD_Address = int("0x" + part.upper(), 16)
                    
        print("Testing LCD")
        try:
            self.__LCD_ENABLE__ = 0b00000100
            self.__E_PULSE__ = 0.0005
            self.__E_DELAY__ = 0.0005
            self.__LCD_bus__ = smbus.SMBus(1)
            self.__lcd_byte__(0x33, 0)
            self.__lcd_byte__(0x32, 0)
            self.__lcd_byte__(0x06, 0)
            self.__lcd_byte__(0x0C, 0)
            self.__lcd_byte__(0x28, 0)
            self.__lcd_byte__(0x01, 0)
            time.sleep(self.__E_DELAY__)
            self.LCDMess("LCD TEST", 1)
            self.LCDMess("MkNxGn", 1)
        except Exception as e:
            print("LCD Failure", e)
            exit(1)
        print("LCD Test Complete!")

    def __lcd_byte__(self, bits, mode):
        bits_high = mode | (bits & 0xF0) | 0x08
        bits_low = mode | ((bits<<4) & 0xF0) | 0x08
        self.__LCD_bus__.write_byte(self.LCD_Address, bits_high)
        self.__lcd_toggle_enable__(bits_high)
        self.__LCD_bus__.write_byte(self.LCD_Address, bits_low)
        self.__lcd_toggle_enable__(bits_low)

    def __lcd_toggle_enable__(self, bits):
        time.sleep(self.__E_DELAY__)
        self.__LCD_bus__.write_byte(self.LCD_Address, (bits | self.__LCD_ENABLE__))
        time.sleep(self.__E_PULSE__)
        self.__LCD_bus__.write_byte(self.LCD_Address,(bits & ~self.__LCD_ENABLE__))
        time.sleep(self.__E_DELAY__)

    def LCDMess(self, message, line):
        """Write a string to the LCD Line Number [line]
        LCD.LCDMess('hello!', 1)
        """
        if line == 1:
            line = 0x80
        else:
            line = 0xC0
        message = message.ljust(16, " ")
        self.__lcd_byte__(line, 0)
        for i in range(16):
            self.__lcd_byte__(ord(message[i]),1)
            
    def LCDClear(self):
        """Clear the LCD
        LCD.LCDClear()"""
        self.__lcd_byte__(0x01, 0)
        
    def DisplayTime(self):
        """Write the date and time on the LCD
        LCD.DisplayTime"""
        Now = datetime.datetime.now()
        Day = str(Now.strftime('%a'))
        Time = str(Now.strftime('%I:%M:%S %p'))
        Date = str(Now.strftime('%m/%d/%y'))
        self.LCDMess(Day + "     " + Date, 1)
        self.LCDMess("   " + Time, 2)
        return "Set"

