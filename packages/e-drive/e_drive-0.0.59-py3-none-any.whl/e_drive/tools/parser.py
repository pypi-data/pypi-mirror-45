import sys
from e_drive.drone import *
from e_drive.tools.update import Updater
from e_drive.gui.card import CardReader
from e_drive.gui.cards import CardReaderAndList

import colorama
from colorama import Fore, Back, Style

# Parser Start


class Parser():

    def __init__(self):

        self.program_name   = None
        self.arguments      = None
        self.count          = 0

        self.flagRawCardShowRange   = False


    def run(self):
        
        self.program_name   = sys.argv[0]
        self.arguments      = sys.argv[1:]
        self.count          = len(self.arguments)

        colorama.init()

        if (self.count > 0) and (self.arguments != None):

            print("Count:{0} ".format(self.count) , end='')

            for arg in self.arguments:
                print("/ {0} ".format(arg), end='')

            print("")

            # >python -m e_drive upgrade
            # >python -m e_drive update
            if      (self.arguments[0] == "upgrade") or (self.arguments[0] == "update"):
                updater = Updater()
                updater.update()
                return

            # >python -m e_drive request State 10 0.2
            elif    ((self.count == 4) and 
                    (self.arguments[0] == "request") and
                    (self.arguments[1] == "State")):         # time interval
                #print("* State - Ready     Blue    Red     Black   Black   None_             1830   1631   2230      76      ")    
                print ("         |Mode     |Color                          |Card           |IR           |Bright|Battery|RSSI|")
                print ("         |Drive    |Front  |Rear   |Left   |Right  |               |  Left| Right|ness  |       |    |")
                self.request(DataType.State, int(self.arguments[2]), float(self.arguments[3]))
                return

            # >python -m e_drive request Motion 10 0.2
            elif    ((self.count == 4) and 
                    (self.arguments[0] == "request") and
                    (self.arguments[1] == "Motion")):         # time interval
                #print("* Motion      -38      64     -32     457     -40    -400      16       0   20500")    
                print ("         |Accel                  |Gyro                   |Angle                  |")
                print ("         |      X|      Y|      Z|   Roll|  Pitch|    Yaw|   Roll|  Pitch|    Yaw|")
                self.request(DataType.Motion, int(self.arguments[2]), float(self.arguments[3]))
                return

            # >python -m e_drive request RawLineTracer 10 0.2
            elif    ((self.count == 4) and 
                    (self.arguments[0] == "request") and
                    (self.arguments[1] == "RawLineTracer")):         # time interval
                #print("* RawLineTracer     36   140   219    36    30   340    33    45 Black       Black       Blue        Red")
                print ("               |Raw         |Front            |Rear             |Color                                           |")
                print ("               |  Left|Right|    H|    S|    V|    H|    S|    V|Left       |Right      |Front      |Rear        |")
                self.request(DataType.RawLineTracer, int(self.arguments[2]), float(self.arguments[3]))
                return

            # >python -m e_drive request RawCard 10 0.2
            elif    ((self.count == 4) and 
                    (self.arguments[0] == "request") and
                    (self.arguments[1] == "RawCard")):         # time interval
                #print("* RawCard   335  503  766  692  309  395 100  39  96  40   9  17 303  61  39 344  77  15   Magenta         Red")
                print ("          |Front Raw     |Rear Raw      |Front RGB  |Rear RGB   |Front HSV  |Rear HSV   |Front Color  |Rear Color   |")
                print ("          |   R    G    B|   R    G    B|  R   G   B|  R   G   B|  H   S   V|  H   S   V|             |             |")
                self.flagRawCardShowRange = False
                self.request(DataType.RawCard, int(self.arguments[2]), float(self.arguments[3]))
                return

            # >python -m e_drive request RawCardRange 10 0.2
            elif    ((self.count == 4) and 
                    (self.arguments[0] == "request") and
                    (self.arguments[1] == "RawCardRange")):         # time interval
                #print("* RawCardRange    200  2000   200  2000   200  2000   200     0   200     0   200     0")
                print ("               |Front                              |Rear                               |")
                print ("               |Red        |Green      |Blue       |Red        |Green      |Blue       |")
                print ("               |  Min|  Max|  Min|  Max|  Min|  Max|  Min|  Max|  Min|  Max|  Min|  Max|")
                self.flagRawCardShowRange = True
                self.request(DataType.RawCard, int(self.arguments[2]), float(self.arguments[3]))
                return

            # 조종
            # python -m e_drive control [accel] [wheel] [time(msec)]
            # 지정한 시간이 종료되면 입력값을 모두 0으로 변경하고 멈춤
            # >python -m e_drive control 40 0 3
            elif    ((self.count == 4) and 
                    (self.arguments[0] == "control")):
                print (Fore.YELLOW + "control" + Style.RESET_ALL)
                self.control(int(self.arguments[1]), int(self.arguments[2]), int(self.arguments[3]))
                return

            # python -m e_drive buzzer [hz] [time(msec)]
            # >python -m e_drive buzzer 400 2000
            elif    ((self.count == 3) and 
                    (self.arguments[0] == "buzzer")):
                print (Fore.WHITE + "Buzz Sound: " + Fore.YELLOW + "{0}".format(int(self.arguments[1])) + Fore.WHITE + "Hz, " + Fore.CYAN + "{0}".format(int(self.arguments[2])) + Fore.WHITE + "ms" + Style.RESET_ALL)
                self.buzzer(int(self.arguments[1]), int(self.arguments[2]))
                return

            # >python -m e_drive light body flicker 100 50 50 10
            # >python -m e_drive light body flickerdouble 100 50 50 10
            # >python -m e_drive light body dimming 3 50 50 10
            # >python -m e_drive light body sunrise 5 50 50 10
            # >python -m e_drive light body sunset 5 50 50 10
            # >python -m e_drive light body rainbow 8 50 50 10
            # >python -m e_drive light body rainbow2 8 50 50 10
            elif    ((self.count == 7) and 
                    (self.arguments[0] == "light")):
                print (Fore.WHITE + "Light: " + Fore.YELLOW + "{0}, {1}, {2}, ({3}, {4}, {5})".format(self.arguments[1], self.arguments[2], int(self.arguments[3]), int(self.arguments[4]), int(self.arguments[5]), int(self.arguments[6])) + Style.RESET_ALL)
                self.lightModeRgb(self.arguments[1], self.arguments[2], int(self.arguments[3]), int(self.arguments[4]), int(self.arguments[5]), int(self.arguments[6]))
                return

            # >python -m e_drive light front hold 100
            # >python -m e_drive light head hold 100
            # >python -m e_drive light tail hold 100
            # >python -m e_drive light left hold 100
            # >python -m e_drive light right hold 100
            elif    ((self.count == 4) and 
                    (self.arguments[0] == "light")):
                print (Fore.WHITE + "Light: " + Fore.YELLOW + "{0}, {1}, {2}".format(self.arguments[1], self.arguments[2], int(self.arguments[3])) + Style.RESET_ALL)
                self.lightModeSingle(self.arguments[1], self.arguments[2], int(self.arguments[3]))
                return


            # 블루투스 장치 연결
            # >python -m e_drive connect
            elif    ((self.count == 1) and 
                    (self.arguments[0] == "connect")):
                print (Fore.YELLOW + "connect" + Style.RESET_ALL)
                self.connect()
                return

            # 블루투스 장치 연결
            # >python -m e_drive disconnect
            elif    ((self.count == 1) and 
                    (self.arguments[0] == "disconnect")):
                print (Fore.YELLOW + "disconnect" + Style.RESET_ALL)
                self.disconnect()
                return

            # >python -m e_drive card
            elif    ((self.count == 1) and 
                    (self.arguments[0] == "card")):
                print (Fore.YELLOW + "card" + Style.RESET_ALL)
                self.guiCardReader()
                return

            # >python -m e_drive cards
            elif    ((self.count == 1) and 
                    (self.arguments[0] == "cards")):
                print (Fore.YELLOW + "cards" + Style.RESET_ALL)
                self.guiCardReaderAndList()
                return

        # 아무것도 실행되지 않은 경우
        self.help()


    def request(self, dataType, repeat, interval):

        #drone = Drone(True, True, True, True, True)
        drone = Drone()
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)
        
        # 이벤트 핸들링 함수 등록
        drone.setEventHandler(DataType.State, self.eventState)
        drone.setEventHandler(DataType.Motion, self.eventMotion)
        drone.setEventHandler(DataType.RawLineTracer, self.eventRawLineTracer)
        drone.setEventHandler(DataType.RawCard, self.eventRawCard)

        # 데이터 요청
        for i in range(repeat):
            drone.sendRequest(DeviceType.Drone, dataType)
            sleep(interval)


    def control(self, accel, wheel, timeRunMs):

        #drone = Drone(True, True, True, True, True)
        drone = Drone()
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)

        # 데이터 요청
        drone.sendControlWhile(accel, wheel, timeRunMs)
        drone.sendControlWhile(0, 0, 200)


    def lightModeRgb(self, strLightPart, strLightMode, interval, r, g, b):

        #drone = Drone(True, True, True, True, True)
        drone = Drone()
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)
        
        if ( (not isinstance(interval, int)) or
            (not isinstance(r, int)) or
            (not isinstance(g, int)) or
            (not isinstance(b, int)) ):
            return None

        lightModeHigh = LightModeDrone.None_

        if      strLightPart == "front":
            lightModeHigh = LightModeDrone.FrontNone
        elif    strLightPart == "body":
            lightModeHigh = LightModeDrone.BodyNone
        elif    strLightPart == "head":
            lightModeHigh = LightModeDrone.HeadNone
        elif    strLightPart == "tail":
            lightModeHigh = LightModeDrone.TailNone
        elif    strLightPart == "left":
            lightModeHigh = LightModeDrone.LeftNone
        elif    strLightPart == "right":
            lightModeHigh = LightModeDrone.RightNone

        lightModeLow = LightModeDrone.None_

        if      strLightMode == "hold":
            lightModeLow = LightModeDrone.BodyHold
        elif    strLightMode == "flicker":
            lightModeLow = LightModeDrone.BodyFlicker
        elif    strLightMode == "flickerdouble":
            lightModeLow = LightModeDrone.BodyFlickerDouble
        elif    strLightMode == "dimming":
            lightModeLow = LightModeDrone.BodyDimming
        elif    strLightMode == "sunrise":
            lightModeLow = LightModeDrone.BodySunrise
        elif    strLightMode == "sunset":
            lightModeLow = LightModeDrone.BodySunset
        elif    strLightMode == "rainbow":
            lightModeLow = LightModeDrone.BodyRainbow
        elif    strLightMode == "rainbow2":
            lightModeLow = LightModeDrone.BodyRainbow2

        lightMode = LightModeDrone(lightModeHigh.value + ((lightModeLow.value) & 0x0F))

        if lightModeHigh != LightModeDrone.None_ and lightModeLow != LightModeDrone.None_:
            drone.sendLightModeColor(lightMode, interval, r, g, b)


    def lightModeSingle(self, strLightPart, strLightMode, interval):

        #drone = Drone(True, True, True, True, True)
        drone = Drone()
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)
        
        if ( (not isinstance(interval, int)) ):
            return None

        lightModeHigh = LightModeDrone.None_

        if      strLightPart == "front":
            lightModeHigh = LightModeDrone.FrontNone
        elif    strLightPart == "body":
            lightModeHigh = LightModeDrone.BodyNone
        elif    strLightPart == "head":
            lightModeHigh = LightModeDrone.HeadNone
        elif    strLightPart == "tail":
            lightModeHigh = LightModeDrone.TailNone
        elif    strLightPart == "left":
            lightModeHigh = LightModeDrone.LeftNone
        elif    strLightPart == "right":
            lightModeHigh = LightModeDrone.RightNone

        lightModeLow = LightModeDrone.None_

        if      strLightMode == "hold":
            lightModeLow = LightModeDrone.BodyHold
        elif    strLightMode == "flicker":
            lightModeLow = LightModeDrone.BodyFlicker
        elif    strLightMode == "flickerdouble":
            lightModeLow = LightModeDrone.BodyFlickerDouble
        elif    strLightMode == "dimming":
            lightModeLow = LightModeDrone.BodyDimming
        elif    strLightMode == "sunrise":
            lightModeLow = LightModeDrone.BodySunrise
        elif    strLightMode == "sunset":
            lightModeLow = LightModeDrone.BodySunset
        elif    strLightMode == "rainbow":
            lightModeLow = LightModeDrone.BodyRainbow
        elif    strLightMode == "rainbow2":
            lightModeLow = LightModeDrone.BodyRainbow2

        lightMode = LightModeDrone(lightModeHigh.value + ((lightModeLow.value) & 0x0F))

        if lightModeHigh != LightModeDrone.None_ and lightModeLow != LightModeDrone.None_:
            drone.sendLightMode(lightMode, interval)


    def buzzer(self, hz, time):

        #drone = Drone(True, True, True, True, True)
        drone = Drone()
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)
        
        if ( (not isinstance(hz, int)) or (not isinstance(time, int)) ):
            return None

        header = Header()
        
        header.dataType = DataType.Buzzer
        header.length   = Buzzer.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Drone
        
        data = Buzzer()

        data.mode       = BuzzerMode.Hz
        data.value      = hz
        data.time       = time

        drone.transfer(header, data)
        sleep(time / 1000)


    def connect(self):

        #drone = Drone(True, True, True, True, True)
        drone = Drone(flagShowErrorMessage=True, flagShowLogMessage=True)
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)
        
        # 장치에 연결
        drone.connect()    # 마지막으로 연결된 시리얼 포트와 검색된 장치(페트론) 중 가장 신호가 강한 장치에 연결
        #drone.connect(portName="COM14", deviceName="PETRONE 6504")      # 시리얼 포트와 장치(페트론)를 지정하여 연결
        
        print("3");    sleep(1)
        print("2");    sleep(1)
        print("1");    sleep(1)
        print("0");
        
        # 장치에 연결된 경우 정보 요청
        if drone.isConnected():
            sleep(1)

        drone.close()


    def disconnect(self):

        #drone = Drone(True, True, True, True, True)
        drone = Drone(flagShowErrorMessage=True, flagShowLogMessage=True)
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)
        
        drone.sendLinkDisconnect()
        sleep(0.2)

        drone.close()



    def guiCardReader(self):

        cr = CardReader()
        cr.run()


    def guiCardReaderAndList(self):

        crl = CardReaderAndList()
        crl.run()


    def help(self):

        print(Fore.YELLOW + "* Command List " + Style.RESET_ALL)

        print("")
        print(Fore.CYAN + "  - Firmware Upgrade" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive " + Fore.YELLOW + "upgrade" + Style.RESET_ALL)

        print("")
        print(Fore.CYAN + "  - Request Data" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive " + Fore.YELLOW + "request State 10 0.2" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive " + Fore.YELLOW + "request Motion 10 0.2" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive " + Fore.YELLOW + "request RawLineTracer 10 0.2" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive " + Fore.YELLOW + "request RawCard 10 0.2" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive " + Fore.YELLOW + "request RawCardRange 10 0.2" + Style.RESET_ALL)

        print("")
        print(Fore.CYAN + "  - Control" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive control [" + Fore.YELLOW + "accel" + Fore.WHITE + "] [" + Fore.GREEN + "wheel" + Fore.WHITE + "] [" + Fore.YELLOW + "time(msec)" + Fore.WHITE + "]" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive " + Fore.YELLOW + "control 40 0 3000" + Style.RESET_ALL)

        print("")
        print(Fore.CYAN + "  - Buzzer" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive " + Fore.YELLOW + "buzzer 400 2000" + Style.RESET_ALL)

        print("")
        print(Fore.CYAN + "  - Light single" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive " + Fore.YELLOW + "light front hold 100" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive " + Fore.YELLOW + "light head hold 100" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive " + Fore.YELLOW + "light tail hold 100" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive " + Fore.YELLOW + "light left hold 100" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive " + Fore.YELLOW + "light right hold 100" + Style.RESET_ALL)

        print("")
        print(Fore.CYAN + "  - Light RGB" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive " + Fore.YELLOW + "light body hold 100 50 50 10" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive " + Fore.YELLOW + "light body flicker 100 50 50 10" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive " + Fore.YELLOW + "light body flickerdouble 100 50 50 10" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive " + Fore.YELLOW + "light body dimming 3 50 50 10" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive " + Fore.YELLOW + "light body sunrise 5 50 50 10" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive " + Fore.YELLOW + "light body sunset 5 50 50 10" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive " + Fore.YELLOW + "light body rainbow 8 50 50 10" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive " + Fore.YELLOW + "light body rainbow2 8 50 50 10" + Style.RESET_ALL)

        print("")
        print(Fore.CYAN + "  - Bluetooth" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive " + Fore.YELLOW + "connect" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive " + Fore.YELLOW + "disconnect" + Style.RESET_ALL)

        print("")
        print(Fore.CYAN + "  - GUI" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive " + Fore.YELLOW + "card" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drive " + Fore.YELLOW + "cards" + Style.RESET_ALL)


    def eventState(self, state):

        print("* State   " +
                Fore.YELLOW + "{0:10}".format(state.modeDrive.name) +
                Fore.WHITE + "{0:8}".format(state.colorFront.name) +
                Fore.WHITE + "{0:8}".format(state.colorRear.name) +
                Fore.WHITE + "{0:8}".format(state.colorLeft.name) +
                Fore.WHITE + "{0:8}".format(state.colorRight.name) +
                Fore.CYAN + "{0:15}".format(state.card.name) +
                Fore.CYAN + "{0:7}".format(state.irFrontLeft) +
                Fore.CYAN + "{0:7}".format(state.irFrontRight) +
                Fore.GREEN + "{0:7}".format(state.brightness) +
                Fore.GREEN + "{0:8}".format(state.battery) + 
                Fore.GREEN + "{0:5}".format(state.rssi) + Style.RESET_ALL)


    def eventMotion(self, motion):

        print("* Motion " +
                Fore.YELLOW + "{0:8}".format(motion.accelX) +
                Fore.YELLOW + "{0:8}".format(motion.accelY) +
                Fore.YELLOW + "{0:8}".format(motion.accelZ) +
                Fore.WHITE + "{0:8}".format(motion.gyroRoll) +
                Fore.WHITE + "{0:8}".format(motion.gyroPitch) +
                Fore.WHITE + "{0:8}".format(motion.gyroYaw) +
                Fore.CYAN + "{0:8}".format(motion.angleRoll) +
                Fore.CYAN + "{0:8}".format(motion.anglePitch) +
                Fore.CYAN + "{0:8}".format(motion.angleYaw) + Style.RESET_ALL)


    def eventRawLineTracer(self, rawLineTracer):

        print("* RawLineTracer " +
                Fore.RED        + "{0:6}".format(rawLineTracer.left) +
                Fore.RED        + "{0:6}".format(rawLineTracer.right) +
                Fore.YELLOW     + "{0:6}".format(rawLineTracer.frontH) +
                Fore.YELLOW     + "{0:6}".format(rawLineTracer.frontS) +
                Fore.YELLOW     + "{0:6}".format(rawLineTracer.frontV) +
                Fore.CYAN       + "{0:6}".format(rawLineTracer.rearH) +
                Fore.CYAN       + "{0:6}".format(rawLineTracer.rearS) +
                Fore.CYAN       + "{0:6} ".format(rawLineTracer.rearV) +
                Fore.MAGENTA    + "{0:12}".format(rawLineTracer.leftColor.name) +
                Fore.MAGENTA    + "{0:12}".format(rawLineTracer.rightColor.name) +
                Fore.GREEN      + "{0:12}".format(rawLineTracer.frontColor.name) +
                Fore.GREEN      + "{0:12}".format(rawLineTracer.rearColor.name) + Style.RESET_ALL)


    def eventRawCard(self, rawCard):

        if self.flagRawCardShowRange:
    
            print("* RawCardRange " +
                    Fore.RED    + "{0:6}".format(rawCard.range[0][0][0]) +
                    Fore.RED    + "{0:6}".format(rawCard.range[0][0][1]) +
                    Fore.GREEN  + "{0:6}".format(rawCard.range[0][1][0]) +
                    Fore.GREEN  + "{0:6}".format(rawCard.range[0][1][1]) +
                    Fore.BLUE   + "{0:6}".format(rawCard.range[0][2][0]) +
                    Fore.BLUE   + "{0:6}".format(rawCard.range[0][2][1]) +
                    Fore.RED    + "{0:6}".format(rawCard.range[1][0][0]) +
                    Fore.RED    + "{0:6}".format(rawCard.range[1][0][1]) +
                    Fore.GREEN  + "{0:6}".format(rawCard.range[1][1][0]) +
                    Fore.GREEN  + "{0:6}".format(rawCard.range[1][1][1]) +
                    Fore.BLUE   + "{0:6}".format(rawCard.range[1][2][0]) +
                    Fore.BLUE   + "{0:6}".format(rawCard.range[1][2][1]) + Style.RESET_ALL)

        else:
    
            print("* RawCard " +
                    Fore.RED    + "{0:5}".format(rawCard.rgbRaw[0][0]) +
                    Fore.GREEN  + "{0:5}".format(rawCard.rgbRaw[0][1]) +
                    Fore.BLUE   + "{0:5}".format(rawCard.rgbRaw[0][2]) +
                    Fore.RED    + "{0:5}".format(rawCard.rgbRaw[1][0]) +
                    Fore.GREEN  + "{0:5}".format(rawCard.rgbRaw[1][1]) +
                    Fore.BLUE   + "{0:5}".format(rawCard.rgbRaw[1][2]) +
                    Fore.RED    + "{0:4}".format(rawCard.rgb[0][0]) +
                    Fore.GREEN  + "{0:4}".format(rawCard.rgb[0][1]) +
                    Fore.BLUE   + "{0:4}".format(rawCard.rgb[0][2]) +
                    Fore.RED    + "{0:4}".format(rawCard.rgb[1][0]) +
                    Fore.GREEN  + "{0:4}".format(rawCard.rgb[1][1]) +
                    Fore.BLUE   + "{0:4}".format(rawCard.rgb[1][2]) +
                    Fore.RED    + "{0:4}".format(rawCard.hsv[0][0]) +
                    Fore.GREEN  + "{0:4}".format(rawCard.hsv[0][1]) +
                    Fore.BLUE   + "{0:4}".format(rawCard.hsv[0][2]) +
                    Fore.RED    + "{0:4}".format(rawCard.hsv[1][0]) +
                    Fore.GREEN  + "{0:4}".format(rawCard.hsv[1][1]) +
                    Fore.BLUE   + "{0:4} ".format(rawCard.hsv[1][2]) +
                    Fore.CYAN   + "{0:14}".format(rawCard.color[0].name) +
                    Fore.CYAN   + "{0:14}".format(rawCard.color[1].name) + Style.RESET_ALL)


# Parser End
