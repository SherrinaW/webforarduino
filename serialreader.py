import serial
import time


def main():
    ser = serial.Serial('/dev/cu.usbmodem14131', 9600, timeout=0)
    while 1:
        try:
            line = ser.readline()
            line = line.decode('ascii').strip()
            if line != "":
                print(line, flush=True)
            time.sleep(1)
        except ser.SerialTimeoutException:
            print('Data could not be read')
            time.sleep(1)


if __name__ == "__main__":
    main()
