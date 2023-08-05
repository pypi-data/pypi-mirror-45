import os
import abc 
import numpy as np
from struct import *
from enum import Enum

from e_drive.system import *


# ISerializable Start


class ISerializable:
    
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getSize(self):
        pass

    @abc.abstractmethod
    def ToArray(self):
        pass


# ISerializable End



# DataType Start


class DataType(Enum):
    
    None_                       = 0x00      # 없음
    
    Ping                        = 0x01      # 통신 확인
    Ack                         = 0x02      # 데이터 수신에 대한 응답
    Error                       = 0x03      # 오류(reserve, 비트 플래그는 추후에 지정)
    Request                     = 0x04      # 지정한 타입의 데이터 요청
    Message                     = 0x05      # 문자열 데이터
    Address                     = 0x06      # 장치 주소(MAC이 있는 경우 MAC) 혹은 고유번호(MAC이 없는 경우 UUID)
    Information                 = 0x07      # 펌웨어 및 장치 정보
    Update                      = 0x08      # 펌웨어 업데이트
    UpdateLocation              = 0x09      # 펌웨어 업데이트 위치 정정
    Encrypt                     = 0x0A      # 펌웨어 암호화
    SystemCount                 = 0x0B      # 시스템 카운트
    SystemInformation           = 0x0C      # 시스템 정보
    Registration                = 0x0D      # 제품 등록
    Administrator               = 0x0E      # 관리자 권한 획득
    Monitor                     = 0x0F      # 디버깅용 값 배열 전송. 첫번째 바이트에 타입, 두 번째 바이트에 페이지 지정(수신 받는 데이터의 저장 경로 구분)
    Control                     = 0x10      # 조종

    Command                     = 0x11      # 명령

    # Light
    LightManual                 = 0x20      # LED 수동 제어
    LightMode                   = 0x21      # LED 모드
    LightEvent                  = 0x22      # LED 이벤트
    LightDefault                = 0x23      # LED 초기 모드

    # 센서 RAW 데이터
    RawMotion                   = 0x30      # Motion 센서 데이터 RAW 값
    RawLineTracer               = 0x31      # 라인트레이서 데이터 RAW 값
    RawCard                     = 0x32      # 카드 데이터 RAW 값
    RawCardList                 = 0x33      # 카드 리스트 데이터 RAW 값
    RawCardFunctionList         = 0x34      # 카드 함수 리스트 데이터 RAW 값

    # 상태, 센서
    State                       = 0x40      # 드론의 상태(비행 모드 방위기준 배터리량)
    Attitude                    = 0x41      # 드론의 자세(Angle)
    Position                    = 0x42      # 위치
    Motion                      = 0x43      # Motion 센서 데이터 처리한 값(IMU)
    Range                       = 0x44      # 거리센서 데이터

    # 설정
    Count                       = 0x50      # 카운트
    Bias                        = 0x51      # 엑셀, 자이로 바이어스 값
    Trim                        = 0x52      # 트림

    # Devices
    Motor                       = 0x60      # 모터 제어 및 현재 제어값 확인
    MotorSingle                 = 0x61      # 한 개의 모터 제어
    Buzzer                      = 0x62      # 버저 제어

    # Input
    Button                      = 0x70      # 버튼 입력

    # Information Assembled
    InformationAssembledForController   = 0xA0      # 자주 갱신되는 비행 데이터 모음
    InformationAssembledForEntry        = 0xA1      # 자주 갱신되는 비행 데이터 모음
    InformationAssembledForByBlocks     = 0xA2      # 자주 갱신되는 비행 데이터 모음

    # LINK 모듈
    LinkState                           = 0xE0     # 링크 모듈의 상태
    LinkEvent                           = 0xE1     # 링크 모듈의 이벤트
    LinkEventAddress                    = 0xE2     # 링크 모듈의 이벤트 + 주소
    LinkRssi                            = 0xE3     # 링크와 연결된 장치의 RSSI값
    LinkDiscoveredDevice                = 0xE4     # 검색된 장치
    LinkPasscode                        = 0xE5     # 페어링 시 필요한 Passcode 설정
    
    EndOfType                           = 0xDC


# DataType End



# CommandType Start


class CommandType(Enum):
    
    None_                   = 0x00      # 없음

    Stop                    = 0x01      # 정지
    ClearBias               = 0x02      # 자이로 바이어스 리셋(트림도 같이 초기화 됨)
    ClearTrim               = 0x03      # 트림 초기화
    DriveEvent              = 0x04      # 주행 이벤트 실행

    SetDefault              = 0x0F      # 기본 설정으로 초기화

    # LINK 모듈
    LinkSystemReset         = 0xE0      # 시스템 재시작
    LinkDiscoverStart       = 0xE1      # 장치 검색 시작
    LinkDiscoverStop        = 0xE2      # 장치 검색 중단
    LinkConnect             = 0xE3      # 지정한 인덱스의 장치 연결
    LinkDisconnect          = 0xE4      # 연결 해제
    LinkRssiPollingStart    = 0xE5      # RSSI 수집 시작
    LinkRssiPollingStop     = 0xE6      # RSSI 수집 중단

    EndOfType               = 0xE7


# CommandType End



# Header Start


class Header(ISerializable):

    def __init__(self):
        self.dataType    = DataType.None_
        self.length      = 0
        self.from_       = DeviceType.None_
        self.to_         = DeviceType.None_


    @classmethod
    def getSize(cls):
        return 4


    def toArray(self):
        return pack('<BBBB', self.dataType.value, self.length, self.from_.value, self.to_.value)


    @classmethod
    def parse(cls, dataArray):
        header = Header()

        if len(dataArray) != cls.getSize():
            return None

        header.dataType, header.length, header.from_, header.to_ = unpack('<BBBB', dataArray)

        header.dataType = DataType(header.dataType)
        header.from_ = DeviceType(header.from_)
        header.to_ = DeviceType(header.to_)

        return header


# Header End



# Common Start


class Ping(ISerializable):

    def __init__(self):
        self.systemTime     = 0


    @classmethod
    def getSize(cls):
        return 8


    def toArray(self):
        return pack('<Q', self.systemTime)


    @classmethod
    def parse(cls, dataArray):
        data = Ping()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.systemTime, = unpack('<Q', dataArray)
        return data



class Ack(ISerializable):

    def __init__(self):
        self.systemTime     = 0
        self.dataType       = DataType.None_
        self.crc16          = 0


    @classmethod
    def getSize(cls):
        return 11


    def toArray(self):
        return pack('<QBH', self.systemTime, self.dataType.value, self.crc16)


    @classmethod
    def parse(cls, dataArray):
        data = Ack()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.systemTime, data.dataType, data.crc16 = unpack('<QBH', dataArray)
        data.dataType = DataType(data.dataType)

        return data



class Error(ISerializable):

    def __init__(self):
        self.systemTime             = 0
        self.errorFlagsForSensor    = 0
        self.errorFlagsForState     = 0


    @classmethod
    def getSize(cls):
        return 16


    def toArray(self):
        return pack('<QII', self.systemTime, self.errorFlagsForSensor, self.errorFlagsForState)


    @classmethod
    def parse(cls, dataArray):
        data = Error()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.systemTime, data.errorFlagsForSensor, data.errorFlagsForState = unpack('<QII', dataArray)

        return data



class Request(ISerializable):

    def __init__(self):
        self.dataType    = DataType.None_


    @classmethod
    def getSize(cls):
        return 1


    def toArray(self):
        return pack('<B', self.dataType.value)


    @classmethod
    def parse(cls, dataArray):
        data = Request()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.dataType, = unpack('<B', dataArray)
        data.dataType = DataType(data.dataType)

        return data



class Message():

    def __init__(self):
        self.message    = ""


    def getSize(self):
        return len(self.message)


    def toArray(self):
        dataArray = bytearray()
        dataArray.extend(self.message.encode('ascii', 'ignore'))
        return dataArray


    @classmethod
    def parse(cls, dataArray):
        data = Message()
        
        if len(dataArray) == 0:
            return ""

        data.message = dataArray[0:len(dataArray)].decode()
        
        return data



class SystemInformation(ISerializable):

    def __init__(self):
        self.crc32bootloader    = 0
        self.crc32application   = 0


    @classmethod
    def getSize(cls):
        return 8


    def toArray(self):
        return pack('<II', self.crc32bootloader, self.crc32application)


    @classmethod
    def parse(cls, dataArray):
        data = SystemInformation()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.crc32bootloader, data.crc32application = unpack('<II', dataArray)

        return data



class Version(ISerializable):

    def __init__(self):
        self.build          = 0
        self.minor          = 0
        self.major          = 0

        self.v              = 0         # build, minor, major을 하나의 UInt32로 묶은 것(버젼 비교 시 사용)


    @classmethod
    def getSize(cls):
        return 4


    def toArray(self):
        return pack('<HBB', self.build, self.minor, self.major)


    @classmethod
    def parse(cls, dataArray):
        data = Version()
        
        if len(dataArray) != cls.getSize():
            return None

        data.v, = unpack('<I', dataArray)

        data.build, data.minor, data.major = unpack('<HBB', dataArray)

        return data



class Information(ISerializable):

    def __init__(self):
        self.modeUpdate     = ModeUpdate.None_

        self.modelNumber    = ModelNumber.None_
        self.version        = Version()

        self.year           = 0
        self.month          = 0
        self.day            = 0


    @classmethod
    def getSize(cls):
        return 13


    def toArray(self):
        dataArray = bytearray()
        dataArray.extend(pack('<B', self.modeUpdate.value))
        dataArray.extend(pack('<I', self.modelNumber.value))
        dataArray.extend(self.version.toArray())
        dataArray.extend(pack('<H', self.year))
        dataArray.extend(pack('<B', self.month))
        dataArray.extend(pack('<B', self.day))
        return dataArray


    @classmethod
    def parse(cls, dataArray):
        data = Information()
        
        if len(dataArray) == cls.getSize():
            
            indexStart = 0;        indexEnd = 1;                    data.modeUpdate,    = unpack('<B', dataArray[indexStart:indexEnd])
            indexStart = indexEnd; indexEnd += 4;                   data.modelNumber,   = unpack('<I', dataArray[indexStart:indexEnd])
            indexStart = indexEnd; indexEnd += Version.getSize();   data.version        = Version.parse(dataArray[indexStart:indexEnd])
            indexStart = indexEnd; indexEnd += 2;                   data.year,          = unpack('<H', dataArray[indexStart:indexEnd])
            indexStart = indexEnd; indexEnd += 1;                   data.month,         = unpack('<B', dataArray[indexStart:indexEnd])
            indexStart = indexEnd; indexEnd += 1;                   data.day,           = unpack('<B', dataArray[indexStart:indexEnd])

            data.modeUpdate     = ModeUpdate(data.modeUpdate)
            data.modelNumber    = ModelNumber(data.modelNumber)

            return data

        elif len(dataArray) == InformationCC2541.getSize():

            return InformationCC2541.parse(dataArray)

        return None



class InformationCC2541(ISerializable):

    def __init__(self):
        self.modeUpdate     = ModeUpdate.None_

        self.modelNumber    = ModelNumber.None_
        self.version        = Version()

        self.year           = 0
        self.month          = 0
        self.day            = 0

        self.imageType      = ImageType.None_


    @classmethod
    def getSize(cls):
        return 14


    def toArray(self):
        dataArray = bytearray()
        dataArray.extend(pack('<B', self.modeUpdate.value))
        dataArray.extend(pack('<I', self.modelNumber.value))
        dataArray.extend(self.version.toArray())
        dataArray.extend(pack('<H', self.year))
        dataArray.extend(pack('<B', self.month))
        dataArray.extend(pack('<B', self.day))
        dataArray.extend(pack('<B', self.imageType.value))
        return dataArray


    @classmethod
    def parse(cls, dataArray):
        data = InformationCC2541()
        
        if len(dataArray) != cls.getSize():
            return None
        
        indexStart = 0;        indexEnd = 1;                    data.modeUpdate,    = unpack('<B', dataArray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += 4;                   data.modelNumber,   = unpack('<I', dataArray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += Version.getSize();   data.version        = Version.parse(dataArray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += 2;                   data.year,          = unpack('<H', dataArray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += 1;                   data.month,         = unpack('<B', dataArray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += 1;                   data.day,           = unpack('<B', dataArray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += 1;                   data.imageType,     = unpack('<B', dataArray[indexStart:indexEnd])

        data.modeUpdate     = ModeUpdate(data.modeUpdate)
        data.modelNumber    = ModelNumber(data.modelNumber)

        data.imageType      = ImageType(data.imageType)

        return data



class UpdateLocation(ISerializable):

    def __init__(self):
        self.indexBlockNext    = 0


    @classmethod
    def getSize(cls):
        return 2


    def toArray(self):
        return pack('<H', self.indexBlockNext)


    @classmethod
    def parse(cls, dataArray):
        data = UpdateLocation()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.indexBlockNext, = unpack('<H', dataArray)

        return data



class Address(ISerializable):

    def __init__(self):
        self.address    = bytearray()


    @classmethod
    def getSize(cls):
        return 16


    def toArray(self):
        return self.address


    @classmethod
    def parse(cls, dataArray):
        data = Address()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.address = dataArray[0:16]
        return data



class RegistrationInformation(ISerializable):

    def __init__(self):
        self.address        = bytearray()
        self.year           = 0
        self.month          = 0
        self.key            = 0
        self.flagValid      = 0


    @classmethod
    def getSize(cls):
        return 21


    def toArray(self):
        dataArray = bytearray()
        dataArray.extend(self.address)
        dataArray.extend(pack('<HBB?', self.year, self.month, self.key, self.flagValid))
        return dataArray


    @classmethod
    def parse(cls, dataArray):
        data = RegistrationInformation()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.address = dataArray[0:16]
        data.year, data.month, data.key, data.flagValid = unpack('<HBB?', dataArray[16:21])
        return data



class Command(ISerializable):

    def __init__(self):
        self.commandType    = CommandType.None_
        self.option         = 0


    @classmethod
    def getSize(cls):
        return 2


    def toArray(self):
        return pack('<BB', self.commandType.value, self.option)


    @classmethod
    def parse(cls, dataArray):
        data = Command()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.commandType, data.option = unpack('<BB', dataArray)
        data.commandType = CommandType(data.commandType)

        return data



class CommandLightEvent(ISerializable):

    def __init__(self):
        self.command    = Command()
        self.event      = LightEvent()


    @classmethod
    def getSize(cls):
        return Command.getSize() + LightEvent.getSize()


    def toArray(self):
        dataArray = bytearray()
        dataArray.extend(self.command.toArray())
        dataArray.extend(self.event.toArray())
        return dataArray


    @classmethod
    def parse(cls, dataArray):
        data = CommandLightEvent()
        
        if len(dataArray) != cls.getSize():
            return None
        
        indexStart = 0;        indexEnd = Command.getSize();         data.command    = Command.parse(dataArray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += LightEvent.getSize();     data.event      = LightEvent.parse(dataArray[indexStart:indexEnd])
        
        return data
        


class CommandLightEventColor(ISerializable):

    def __init__(self):
        self.command    = Command()
        self.event      = LightEvent()
        self.color      = Color()


    @classmethod
    def getSize(cls):
        return Command.getSize() + LightEvent.getSize() + Color.getSize()


    def toArray(self):
        dataArray = bytearray()
        dataArray.extend(self.command.toArray())
        dataArray.extend(self.event.toArray())
        dataArray.extend(self.color.toArray())
        return dataArray


    @classmethod
    def parse(cls, dataArray):
        data = CommandLightEventColor()
        
        if len(dataArray) != cls.getSize():
            return None

        indexStart = 0;        indexEnd = Command.getSize();       data.command    = Command.parse(dataArray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += LightEvent.getSize();   data.event      = LightEvent.parse(dataArray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += Color.getSize();        data.color      = Color.parse(dataArray[indexStart:indexEnd])
        
        return data
        


class CommandLightEventColors(ISerializable):

    def __init__(self):
        self.command    = Command()
        self.event      = LightEvent()
        self.colors     = Colors.Black


    @classmethod
    def getSize(cls):
        return Command.getSize() + LightEvent.getSize() + 1


    def toArray(self):
        dataArray = bytearray()
        dataArray.extend(self.command.toArray())
        dataArray.extend(self.event.toArray())
        dataArray.extend(pack('<B', self.colors.value))
        return dataArray


    @classmethod
    def parse(cls, dataArray):
        data = Command()
        
        if len(dataArray) != cls.getSize():
            return None
        
        indexStart = 0;        indexEnd = Command.getSize();       data.command    = Command.parse(dataArray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += LightEvent.getSize();   data.event      = LightEvent.parse(dataArray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += 1;                      data.colors,    = unpack('<B', dataArray[indexStart:indexEnd])

        data.colors     = Colors(data.colors)

        return data


# Common End



# Monitor Start


class MonitorHeaderType(Enum):
    
    Monitor0            = 0x00
    Monitor4            = 0x01
    Monitor8            = 0x02

    EndOfType           = 0x03



class MonitorDataType(Enum):
    
    U8          = 0x00,
    S8          = 0x01,
    U16         = 0x02,
    S16         = 0x03,
    U32         = 0x04,
    S32         = 0x05,
    U64         = 0x06,
    S64         = 0x07,
    F32         = 0x08,
    F64         = 0x09,

    EndOfType   = 0x0A



class MonitorType(ISerializable):

    def __init__(self):
        self.monitorHeaderType    = MonitorHeaderType.Monitor8


    @classmethod
    def getSize(cls):
        return 1


    def toArray(self):
        return pack('<B', self.monitorHeaderType.value)


    @classmethod
    def parse(cls, dataArray):
        data = MonitorType()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.monitorHeaderType, = unpack('<B', dataArray)

        data.monitorHeaderType  = MonitorHeaderType(data.monitorHeaderType)

        return data



class Monitor0(ISerializable):

    def __init__(self):
        self.monitorDataType        = MonitorDataType.F32
        self.index                  = 0


    @classmethod
    def getSize(cls):
        return 2


    def toArray(self):
        return pack('<BB', self.monitorDataType.value, self.index)


    @classmethod
    def parse(cls, dataArray):
        data = Monitor0()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.monitorDataType, data.index = unpack('<BB', dataArray)

        data.monitorDataType  = MonitorDataType(data.monitorDataType)

        return data



class Monitor4(ISerializable):

    def __init__(self):
        self.systemTime             = 0
        self.monitorDataType        = MonitorDataType.F32
        self.index                  = 0


    @classmethod
    def getSize(cls):
        return 6


    def toArray(self):
        return pack('<IBB', self.systemTime, self.monitorDataType.value, self.index)


    @classmethod
    def parse(cls, dataArray):
        data = Monitor4()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.systemTime, data.monitorDataType, data.index = unpack('<IBB', dataArray)

        data.monitorDataType  = MonitorDataType(data.monitorDataType)

        return data



class Monitor8(ISerializable):
    
    def __init__(self):
        self.systemTime             = 0
        self.monitorDataType        = MonitorDataType.F32
        self.index                  = 0


    @classmethod
    def getSize(cls):
        return 10


    def toArray(self):
        return pack('<QBB', self.systemTime, self.monitorDataType.value, self.index)


    @classmethod
    def parse(cls, dataArray):
        data = Monitor8()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.systemTime, data.monitorDataType, data.index = unpack('<QBB', dataArray)

        data.monitorDataType  = MonitorDataType(data.monitorDataType)

        return data



# Monitor End



# Control Start


class ControlDouble8(ISerializable):

    def __init__(self):
        self.accel      = 0
        self.wheel      = 0


    @classmethod
    def getSize(cls):
        return 2


    def toArray(self):
        return pack('<bb', self.accel, self.wheel)


    @classmethod
    def parse(cls, dataArray):
        data = ControlDouble8()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.accel, data.wheel = unpack('<bb', dataArray)
        return data



class ControlDouble8AndRequestData(ISerializable):

    def __init__(self):
        self.accel      = 0
        self.wheel      = 0
        self.dataType   = DataType.None_


    @classmethod
    def getSize(cls):
        return 3


    def toArray(self):
        return pack('<bbb', self.accel, self.wheel, self.dataType)


    @classmethod
    def parse(cls, dataArray):
        data = ControlDouble8AndRequestData()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.accel, data.wheel, data.dataType = unpack('<bbb', dataArray)
        
        data.dataType = DataType(data.dataType)
        
        return data



class ControlPosition(ISerializable):

    def __init__(self):
        self.positionX          = 0
        self.positionY          = 0
        self.positionZ          = 0

        self.velocity           = 0

        self.heading            = 0
        self.rotationalVelocity = 0


    @classmethod
    def getSize(cls):
        return 20


    def toArray(self):
        return pack('<ffffhh', self.positionX, self.positionY, self.positionZ, self.velocity, self.heading, self.rotationalVelocity)


    @classmethod
    def parse(cls, dataArray):
        data = ControlPosition()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.positionX, data.positionY, data.positionZ, data.velocity, data.heading, data.rotationalVelocity = unpack('<ffffhh', dataArray)
        return data


# Control End



# Light Start


class LightModeDrone(Enum):
    
    None_                   = 0x00
    
    FrontNone               = 0x10
    FrontManual             = 0x11      # 수동 제어
    FrontHold               = 0x12      # 지정한 색상을 계속 켬
    FrontFlicker            = 0x13      # 깜빡임			
    FrontFlickerDouble      = 0x14      # 깜빡임(두 번 깜빡이고 깜빡인 시간만큼 꺼짐)			
    FrontDimming            = 0x15      # 밝기 제어하여 천천히 깜빡임
    FrontSunrise            = 0x16      # 꺼진 상태에서 점점 밝아짐
    FrontSunset             = 0x17      # 켜진 상태에서 점점 어두워짐

    BodyNone                = 0x20
    BodyManual              = 0x21      # 수동 제어
    BodyHold                = 0x22      # 지정한 색상을 계속 켬
    BodyFlicker             = 0x23      # 깜빡임
    BodyFlickerDouble       = 0x24      # 깜빡임(두 번 깜빡이고 깜빡인 시간만큼 꺼짐)
    BodyDimming             = 0x25      # 밝기 제어하여 천천히 깜빡임
    BodySunrise             = 0x26      # 꺼진 상태에서 점점 밝아짐
    BodySunset              = 0x27      # 켜진 상태에서 점점 어두워짐
    BodyRainbow             = 0x28      # 무지개색
    BodyRainbow2            = 0x29      # 무지개색

    HeadNone                = 0x30
    HeadManual              = 0x31      # 수동 제어
    HeadHold                = 0x32      # 지정한 색상을 계속 켬
    HeadFlicker             = 0x33      # 깜빡임
    HeadFlickerDouble       = 0x34      # 깜빡임(두 번 깜빡이고 깜빡인 시간만큼 꺼짐)
    HeadDimming             = 0x35      # 밝기 제어하여 천천히 깜빡임
    HeadSunrise             = 0x36      # 꺼진 상태에서 점점 밝아짐
    HeadSunset              = 0x37      # 켜진 상태에서 점점 어두워짐

    TailNone                = 0x40
    TailManual              = 0x41      # 수동 제어
    TailHold                = 0x42      # 지정한 색상을 계속 켬
    TailFlicker             = 0x43      # 깜빡임
    TailFlickerDouble       = 0x44      # 깜빡임(두 번 깜빡이고 깜빡인 시간만큼 꺼짐)
    TailDimming             = 0x45      # 밝기 제어하여 천천히 깜빡임
    TailSunrise             = 0x46      # 꺼진 상태에서 점점 밝아짐
    TailSunset              = 0x47      # 켜진 상태에서 점점 어두워짐

    LeftNone                = 0x50
    LeftManual              = 0x51      # 수동 제어
    LeftHold                = 0x52      # 지정한 색상을 계속 켬
    LeftFlicker             = 0x53      # 깜빡임
    LeftFlickerDouble       = 0x54      # 깜빡임(두 번 깜빡이고 깜빡인 시간만큼 꺼짐)
    LeftDimming             = 0x55      # 밝기 제어하여 천천히 깜빡임
    LeftSunrise             = 0x56      # 꺼진 상태에서 점점 밝아짐
    LeftSunset              = 0x57      # 켜진 상태에서 점점 어두워짐

    RightNone               = 0x60
    RightManual             = 0x61      # 수동 제어
    RightHold               = 0x62      # 지정한 색상을 계속 켬
    RightFlicker            = 0x63      # 깜빡임
    RightFlickerDouble      = 0x64      # 깜빡임(두 번 깜빡이고 깜빡인 시간만큼 꺼짐)
    RightDimming            = 0x65      # 밝기 제어하여 천천히 깜빡임
    RightSunrise            = 0x66      # 꺼진 상태에서 점점 밝아짐
    RightSunset             = 0x67      # 켜진 상태에서 점점 어두워짐

    EndOfType               = 0x70



class LightFlagsDrone(Enum):
    
    None_       = 0x0000
    
    Front       = 0x0001
    
    BodyRed     = 0x0002
    BodyGreen   = 0x0004
    BodyBlue    = 0x0008
    
    Head        = 0x0010
    Tail        = 0x0020
    Left        = 0x0040
    Right       = 0x0080



class Color(ISerializable):

    def __init__(self):
        self.r      = 0
        self.g      = 0
        self.b      = 0


    @classmethod
    def getSize(cls):
        return 3


    def toArray(self):
        return pack('<BBB', self.r, self.g, self.b)


    @classmethod
    def parse(cls, dataArray):
        data = Color()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.r, data.g, data.b = unpack('<BBB', dataArray)
        return data



class Colors(Enum):

    AliceBlue              = 0
    AntiqueWhite           = 1
    Aqua                   = 2
    Aquamarine             = 3
    Azure                  = 4
    Beige                  = 5
    Bisque                 = 6
    Black                  = 7
    BlanchedAlmond         = 8
    Blue                   = 9
    BlueViolet             = 10
    Brown                  = 11
    BurlyWood              = 12
    CadetBlue              = 13
    Chartreuse             = 14
    Chocolate              = 15
    Coral                  = 16
    CornflowerBlue         = 17
    Cornsilk               = 18
    Crimson                = 19
    Cyan                   = 20
    DarkBlue               = 21
    DarkCyan               = 22
    DarkGoldenRod          = 23
    DarkGray               = 24
    DarkGreen              = 25
    DarkKhaki              = 26
    DarkMagenta            = 27
    DarkOliveGreen         = 28
    DarkOrange             = 29
    DarkOrchid             = 30
    DarkRed                = 31
    DarkSalmon             = 32
    DarkSeaGreen           = 33
    DarkSlateBlue          = 34
    DarkSlateGray          = 35
    DarkTurquoise          = 36
    DarkViolet             = 37
    DeepPink               = 38
    DeepSkyBlue            = 39
    DimGray                = 40
    DodgerBlue             = 41
    FireBrick              = 42
    FloralWhite            = 43
    ForestGreen            = 44
    Fuchsia                = 45
    Gainsboro              = 46
    GhostWhite             = 47
    Gold                   = 48
    GoldenRod              = 49
    Gray                   = 50
    Green                  = 51
    GreenYellow            = 52
    HoneyDew               = 53
    HotPink                = 54
    IndianRed              = 55
    Indigo                 = 56
    Ivory                  = 57
    Khaki                  = 58
    Lavender               = 59
    LavenderBlush          = 60
    LawnGreen              = 61
    LemonChiffon           = 62
    LightBlue              = 63
    LightCoral             = 64
    LightCyan              = 65
    LightGoldenRodYellow   = 66
    LightGray              = 67
    LightGreen             = 68
    LightPink              = 69
    LightSalmon            = 70
    LightSeaGreen          = 71
    LightSkyBlue           = 72
    LightSlateGray         = 73
    LightSteelBlue         = 74
    LightYellow            = 75
    Lime                   = 76
    LimeGreen              = 77
    Linen                  = 78
    Magenta                = 79
    Maroon                 = 80
    MediumAquaMarine       = 81
    MediumBlue             = 82
    MediumOrchid           = 83
    MediumPurple           = 84
    MediumSeaGreen         = 85
    MediumSlateBlue        = 86
    MediumSpringGreen      = 87
    MediumTurquoise        = 88
    MediumVioletRed        = 89
    MidnightBlue           = 90
    MintCream              = 91
    MistyRose              = 92
    Moccasin               = 93
    NavajoWhite            = 94
    Navy                   = 95
    OldLace                = 96
    Olive                  = 97
    OliveDrab              = 98
    Orange                 = 99
    OrangeRed              = 100
    Orchid                 = 101
    PaleGoldenRod          = 102
    PaleGreen              = 103
    PaleTurquoise          = 104
    PaleVioletRed          = 105
    PapayaWhip             = 106
    PeachPuff              = 107
    Peru                   = 108
    Pink                   = 109
    Plum                   = 110
    PowderBlue             = 111
    Purple                 = 112
    RebeccaPurple          = 113
    Red                    = 114
    RosyBrown              = 115
    RoyalBlue              = 116
    SaddleBrown            = 117
    Salmon                 = 118
    SandyBrown             = 119
    SeaGreen               = 120
    SeaShell               = 121
    Sienna                 = 122
    Silver                 = 123
    SkyBlue                = 124
    SlateBlue              = 125
    SlateGray              = 126
    Snow                   = 127
    SpringGreen            = 128
    SteelBlue              = 129
    Tan                    = 130
    Teal                   = 131
    Thistle                = 132
    Tomato                 = 133
    Turquoise              = 134
    Violet                 = 135
    Wheat                  = 136
    White                  = 137
    WhiteSmoke             = 138
    Yellow                 = 139
    YellowGreen            = 140
    
    EndOfType              = 141



class LightManual(ISerializable):

    def __init__(self):
        self.flags          = 0
        self.brightness     = 0


    @classmethod
    def getSize(cls):
        return 3


    def toArray(self):
        return pack('<HB', self.flags, self.brightness)


    @classmethod
    def parse(cls, dataArray):
        data = LightManual()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.flags, data.brightness = unpack('<HB', dataArray)
        return data



class LightMode(ISerializable):

    def __init__(self):
        self.mode        = 0
        self.interval    = 0


    @classmethod
    def getSize(cls):
        return 3


    def toArray(self):
        return pack('<BH', self.mode, self.interval)


    @classmethod
    def parse(cls, dataArray):
        data = LightMode()
        
        if len(dataArray) != cls.getSize():
            return None

        data.mode, data.interval = unpack('<BH', dataArray)
        return data



class LightEvent(ISerializable):

    def __init__(self):
        self.event      = 0
        self.interval   = 0
        self.repeat     = 0


    @classmethod
    def getSize(cls):
        return 4


    def toArray(self):
        return pack('<BHB', self.event, self.interval, self.repeat)


    @classmethod
    def parse(cls, dataArray):
        data = LightEvent()
        
        if len(dataArray) != cls.getSize():
            return None

        data.event, data.interval, data.repeat = unpack('<BHB', dataArray)

        return data



class LightModeColor(ISerializable):
    
    def __init__(self):
        self.mode       = LightMode()
        self.color      = Color()


    @classmethod
    def getSize(cls):
        return LightMode.getSize() + Color.getSize()


    def toArray(self):
        dataArray = bytearray()
        dataArray.extend(self.mode.toArray())
        dataArray.extend(self.color.toArray())
        return dataArray


    @classmethod
    def parse(cls, dataArray):
        data = LightModeColor()
        
        if len(dataArray) != cls.getSize():
            return None

        indexStart = 0;        indexEnd = LightMode.getSize();      data.mode       = LightMode.parse(dataArray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += Color.getSize();         data.color      = Color.parse(dataArray[indexStart:indexEnd])
        return data



class LightModeColors(ISerializable):
    
    def __init__(self):
        self.mode       = LightMode()
        self.colors     = Colors.Black


    @classmethod
    def getSize(cls):
        return LightMode.getSize() + 1


    def toArray(self):
        dataArray = bytearray()
        dataArray.extend(self.mode.toArray())
        dataArray.extend(pack('<B', self.colors.value))
        return dataArray


    @classmethod
    def parse(cls, dataArray):
        data = LightModeColors()
        
        if len(dataArray) != cls.getSize():
            return None

        indexStart = 0;        indexEnd = LightMode.getSize();      data.mode       = LightMode.parse(dataArray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += 1;                       data.colors,    = unpack('<B', dataArray[indexStart:indexEnd])

        data.colors     = Colors(data.colors)

        return data



class LightEventColor(ISerializable):
    
    def __init__(self):
        self.event      = LightEvent()
        self.color      = Color()


    @classmethod
    def getSize(cls):
        return LightEvent.getSize() + Color.getSize()


    def toArray(self):
        dataArray = bytearray()
        dataArray.extend(self.event.toArray())
        dataArray.extend(self.color.toArray())
        return dataArray


    @classmethod
    def parse(cls, dataArray):
        data = LightEventColor()
        
        if len(dataArray) != cls.getSize():
            return None

        indexStart = 0;        indexEnd = LightEvent.getSize();     data.event      = LightEvent.parse(dataArray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += Color.getSize();         data.command    = Color.parse(dataArray[indexStart:indexEnd])
        
        return data



class LightEventColors(ISerializable):
    
    def __init__(self):
        self.event      = LightEvent()
        self.colors     = Colors.Black


    @classmethod
    def getSize(cls):
        return LightEvent.getSize() + 1


    def toArray(self):
        dataArray = bytearray()
        dataArray.extend(self.event.toArray())
        dataArray.extend(pack('<B', self.colors.value))
        return dataArray


    @classmethod
    def parse(cls, dataArray):
        data = LightEventColors()
        
        if len(dataArray) != cls.getSize():
            return None

        indexStart = 0;        indexEnd = LightEvent.getSize();     data.event      = LightEvent.parse(dataArray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += 1;                       data.colors,    = unpack('<B', dataArray[indexStart:indexEnd])

        data.colors     = Colors(data.colors)

        return data


# Light End



# Buzzer Start


class BuzzerMode(Enum):

    Stop                = 0     # 정지(Mode에서의 Stop은 통신에서 받았을 때 Buzzer를 끄는 용도로 사용, set으로만 호출)

    Mute                = 1     # 묵음 즉시 적용
    MuteReserve         = 2     # 묵음 예약

    Scale               = 3     # 음계 즉시 적용
    ScaleReserve        = 4     # 음계 예약

    Hz                  = 5     # 주파수 즉시 적용
    HzReserve           = 6     # 주파수 예약

    EndOfType           = 7



class BuzzerScale(Enum):

    C1 = 0x00; CS1 = 0x01; D1 = 0x02; DS1 = 0x03; E1 = 0x04; F1 = 0x05; FS1 = 0x06; G1 = 0x07; GS1 = 0x08; A1 = 0x09; AS1 = 0x0A; B1 = 0x0B
    C2 = 0x0C; CS2 = 0x0D; D2 = 0x0E; DS2 = 0x0F; E2 = 0x10; F2 = 0x11; FS2 = 0x12; G2 = 0x13; GS2 = 0x14; A2 = 0x15; AS2 = 0x16; B2 = 0x17
    C3 = 0x18; CS3 = 0x19; D3 = 0x1A; DS3 = 0x1B; E3 = 0x1C; F3 = 0x1D; FS3 = 0x1E; G3 = 0x1F; GS3 = 0x20; A3 = 0x21; AS3 = 0x22; B3 = 0x23
    C4 = 0x24; CS4 = 0x25; D4 = 0x26; DS4 = 0x27; E4 = 0x28; F4 = 0x29; FS4 = 0x2A; G4 = 0x2B; GS4 = 0x2C; A4 = 0x2D; AS4 = 0x2E; B4 = 0x2F

    C5 = 0x30; CS5 = 0x31; D5 = 0x32; DS5 = 0x33; E5 = 0x34; F5 = 0x35; FS5 = 0x36; G5 = 0x37; GS5 = 0x38; A5 = 0x39; AS5 = 0x3A; B5 = 0x3B
    C6 = 0x3C; CS6 = 0x3D; D6 = 0x3E; DS6 = 0x3F; E6 = 0x40; F6 = 0x41; FS6 = 0x42; G6 = 0x43; GS6 = 0x44; A6 = 0x45; AS6 = 0x46; B6 = 0x47
    C7 = 0x48; CS7 = 0x49; D7 = 0x4A; DS7 = 0x4B; E7 = 0x4C; F7 = 0x4D; FS7 = 0x4E; G7 = 0x4F; GS7 = 0x50; A7 = 0x51; AS7 = 0x52; B7 = 0x53
    C8 = 0x54; CS8 = 0x55; D8 = 0x56; DS8 = 0x57; E8 = 0x58; F8 = 0x59; FS8 = 0x5A; G8 = 0x5B; GS8 = 0x5C; A8 = 0x5D; AS8 = 0x5E; B8 = 0x5F

    EndOfType   = 0x60

    Mute        = 0xEE  # 묵음
    Fin         = 0xFF  # 악보의 끝



class Buzzer(ISerializable):

    def __init__(self):
        self.mode       = BuzzerMode.Stop
        self.value      = 0
        self.time       = 0


    @classmethod
    def getSize(cls):
        return 5


    def toArray(self):
        return pack('<BHH', self.mode.value, self.value, self.time)


    @classmethod
    def parse(cls, dataArray):
        data = Buzzer()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.mode, data.value, data.time = unpack('<BHH', dataArray)

        data.mode = BuzzerMode(data.mode)

        return data


# Buzzer End



# Button Start



class ButtonFlagDrone(Enum):

    None_               = 0x0000
    
    Reset               = 0x0001



class ButtonEvent(Enum):

    None_               = 0x00
    
    Down                = 0x01  # 누르기 시작
    Press               = 0x02  # 누르는 중
    Up                  = 0x03  # 뗌
    
    EndContinuePress    = 0x04  # 연속 입력 종료



class Button(ISerializable):

    def __init__(self):
        self.button     = 0
        self.event      = ButtonEvent.None_


    @classmethod
    def getSize(cls):
        return 3


    def toArray(self):
        return pack('<HB', self.button, self.event.value)


    @classmethod
    def parse(cls, dataArray):
        data = Button()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.button, data.event = unpack('<HB', dataArray)

        data.event = ButtonEvent(data.event)
        
        return data


# Button End



# Sensor Raw Start


class RawMotion(ISerializable):

    def __init__(self):
        self.accelX     = 0
        self.accelY     = 0
        self.accelZ     = 0
        self.gyroRoll   = 0
        self.gyroPitch  = 0
        self.gyroYaw    = 0


    @classmethod
    def getSize(cls):
        return 12


    def toArray(self):
        return pack('<hhhhhh', self.accelX, self.accelY, self.accelZ, self.gyroRoll, self.gyroPitch, self.gyroYaw)


    @classmethod
    def parse(cls, dataArray):
        data = RawMotion()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.accelX, data.accelY, data.accelZ, data.gyroRoll, data.gyroPitch, data.gyroYaw = unpack('<hhhhhh', dataArray)
        
        return data



class RawLineTracer(ISerializable):

    def __init__(self):
        self.left       = 0
        self.right      = 0

        self.frontH     = 0
        self.frontS     = 0
        self.frontV     = 0

        self.rearH      = 0
        self.rearS      = 0
        self.rearV      = 0

        self.leftColor  = 0
        self.rightColor = 0
        self.frontColor = 0
        self.rearColor  = 0


    @classmethod
    def getSize(cls):
        return 16


    def toArray(self):
        return pack('<hhhbbhbbBBBB', self.left, self.right, self.frontH, self.frontS, self.frontV, self.rearH, self.rearS, self.rearV, self.leftColor.value, self.rightColor.value, self.frontColor.value, self.rearColor.value)


    @classmethod
    def parse(cls, dataArray):
        data = RawLineTracer()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.left, data.right, data.frontH, data.frontS, data.frontV, data.rearH, data.rearS, data.rearV, data.leftColor, data.rightColor, data.frontColor, data.rearColor = unpack('<hhhbbhbbBBBB', dataArray)
        
        data.leftColor  = CardColor(data.leftColor)
        data.rightColor = CardColor(data.rightColor)
        data.frontColor = CardColor(data.frontColor)
        data.rearColor  = CardColor(data.rearColor)

        return data



class RawCard(ISerializable):

    def __init__(self):
        self.range      = [[[0 for i in range(2)] for j in range(3)] for k in range(2)]
        self.rgbRaw     = [[0 for i in range(3)] for j in range(2)]

        self.rgb        = [[0 for i in range(3)] for j in range(2)]     # 0 ~ 255
        self.hsv        = [[0 for i in range(3)] for j in range(2)]     # H: 0 ~ 360, S: 0 ~ 100, V: 0 ~ 100
        self.color      = [0 for i in range(2)]

        self.card       = 0


    @classmethod
    def getSize(cls):
        return 57


    def toArray(self):
        #             123456789012345678901234567890123
        return pack('<hhhhhhhhhhhhhhhhhhBBBBBBhhhhhhBBB',
                    self.range[0][0][0], self.range[0][0][1], self.range[0][1][0], self.range[0][1][1], self.range[0][2][0], self.range[0][2][1],
                    self.range[1][0][0], self.range[0][0][1], self.range[1][1][0], self.range[0][1][1], self.range[1][2][0], self.range[0][2][1],
                    self.rgbRaw[0][0], self.rgbRaw[0][1] , self.rgbRaw[0][2], self.rgbRaw[1][0], self.rgbRaw[1][1] , self.rgbRaw[1][2],
                    self.rgb[0][0], self.rgb[0][1] , self.rgb[0][2], self.rgb[1][0], self.rgb[1][1] , self.rgb[1][2],
                    self.hsv[0][0], self.hsv[0][1] , self.hsv[0][2], self.hsv[1][0], self.hsv[1][1] , self.hsv[1][2],
                    self.color[0].value, self.color[1].value , self.card.value)


    @classmethod
    def parse(cls, dataArray):
        data = RawCard()
        
        if len(dataArray) != cls.getSize():
            return None
        
        (   data.range[0][0][0], data.range[0][0][1], data.range[0][1][0], data.range[0][1][1], data.range[0][2][0], data.range[0][2][1],
            data.range[1][0][0], data.range[0][0][1], data.range[1][1][0], data.range[0][1][1], data.range[1][2][0], data.range[0][2][1],
            data.rgbRaw[0][0], data.rgbRaw[0][1] , data.rgbRaw[0][2], data.rgbRaw[1][0], data.rgbRaw[1][1] , data.rgbRaw[1][2],
            data.rgb[0][0], data.rgb[0][1] , data.rgb[0][2], data.rgb[1][0], data.rgb[1][1] , data.rgb[1][2],
            data.hsv[0][0], data.hsv[0][1] , data.hsv[0][2], data.hsv[1][0], data.hsv[1][1] , data.hsv[1][2],
            data.color[0], data.color[1] , data.card) = unpack('<hhhhhhhhhhhhhhhhhhBBBBBBhhhhhhBBB', dataArray)

        data.color[0]   = CardColor(data.color[0])
        data.color[1]   = CardColor(data.color[1])
        data.card       = Card(data.card)
        
        return data



class RawCardList(ISerializable):

    def __init__(self):
        self.index      = 0
        self.size       = 0

        self.card       = [[0 for i in range(2)] for j in range(40)]        # [i][0]: card, [i][1]: option


    @classmethod
    def getSize(cls):
        return 82


    def toArray(self):
        dataArray = bytearray()
        dataArray.extend(pack('<BB', self.index, self.size))

        for i in range(0, 40):
            dataArray.extend(pack('<BB', self.card[i][0], self.card[i][1]))
        
        return dataArray


    @classmethod
    def parse(cls, dataArray):
        data = RawCardList()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.index, data.size = unpack('<BB', dataArray[0:2])

        for i in range(0, 40):
            indexArray = 2 + (i * 2);
            data.card[i][0], data.card[i][1] = unpack('<BB', dataArray[indexArray:(indexArray + 2)])
        
        return data


# Sensor Raw End



# Information Start


class State(ISerializable):

    def __init__(self):
        self.modeSystem     = ModeSystem.None_
        self.modeDrive      = ModeDrive.None_

        self.irFrontLeft    = 0
        self.irFrontRight   = 0

        self.colorFront     = 0
        self.colorRear      = 0
        self.colorLeft      = 0
        self.colorRight     = 0

        self.card           = 0

        self.brightness     = 0
        self.battery        = 0


    @classmethod
    def getSize(cls):
        return 14


    def toArray(self):
        return pack('<BBHHBBBBBHB', self.modeSystem.value, self.modeDrive.value, self.irFrontLeft, self.irFrontRight, self.colorFront.value, self.colorRear.value, self.colorLeft.value, self.colorRight.value, self.card.value, self.brightness, self.battery)


    @classmethod
    def parse(cls, dataArray):
        data = State()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.modeSystem, data.modeDrive, data.irFrontLeft, data.irFrontRight, data.colorFront, data.colorRear, data.colorLeft, data.colorRight, data.card, data.brightness, data.battery = unpack('<BBHHBBBBBHB', dataArray)

        data.modeSystem     = ModeSystem(data.modeSystem)
        data.modeDrive      = ModeDrive(data.modeDrive)
        data.colorFront     = CardColor(data.colorFront)
        data.colorRear      = CardColor(data.colorRear)
        data.colorLeft      = CardColor(data.colorLeft)
        data.colorRight     = CardColor(data.colorRight)
        data.card           = Card(data.card)
        
        return data



class Attitude(ISerializable):

    def __init__(self):
        self.roll       = 0
        self.pitch      = 0
        self.yaw        = 0


    @classmethod
    def getSize(cls):
        return 6


    def toArray(self):
        return pack('<hhh', self.roll, self.pitch, self.yaw)


    @classmethod
    def parse(cls, dataArray):
        data = Attitude()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.roll, data.pitch, data.yaw = unpack('<hhh', dataArray)
        
        return data
        


class Position(ISerializable):

    def __init__(self):
        self.x      = 0
        self.y      = 0
        self.z      = 0


    @classmethod
    def getSize(cls):
        return 12


    def toArray(self):
        return pack('<fff', self.x, self.y, self.z)


    @classmethod
    def parse(cls, dataArray):
        data = Position()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.x, data.y, data.z = unpack('<fff', dataArray)
        
        return data



class Motion(ISerializable):

    def __init__(self):
        self.accelX     = 0
        self.accelY     = 0
        self.accelZ     = 0
        self.gyroRoll   = 0
        self.gyroPitch  = 0
        self.gyroYaw    = 0
        self.angleRoll  = 0
        self.anglePitch = 0
        self.angleYaw   = 0


    @classmethod
    def getSize(cls):
        return 18


    def toArray(self):
        return pack('<hhhhhhhhh', self.accelX, self.accelY, self.accelZ, self.gyroRoll, self.gyroPitch, self.gyroYaw, self.angleRoll, self.anglePitch, self.angleYaw)


    @classmethod
    def parse(cls, dataArray):
        data = Motion()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.accelX, data.accelY, data.accelZ, data.gyroRoll, data.gyroPitch, data.gyroYaw, data.angleRoll, data.anglePitch, data.angleYaw = unpack('<hhhhhhhhh', dataArray)
        
        return data



class Range(ISerializable):

    def __init__(self):
        self.frontLeft  = 0
        self.frontRight = 0


    @classmethod
    def getSize(cls):
        return 4


    def toArray(self):
        return pack('<hh', self.frontLeft, self.frontRight)


    @classmethod
    def parse(cls, dataArray):
        data = Range()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.frontLeft, data.frontRight = unpack('<hh', dataArray)
        
        return data



class Trim(ISerializable):

    def __init__(self):
        self.wheel      = 0


    @classmethod
    def getSize(cls):
        return 1


    def toArray(self):
        return pack('<h', self.wheel)


    @classmethod
    def parse(cls, dataArray):
        data = Trim()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.wheel, = unpack('<h', dataArray)
        
        return data


# Information End



# Sensor Start


class Vector(ISerializable):

    def __init__(self):
        self.x      = 0
        self.y      = 0
        self.z      = 0


    @classmethod
    def getSize(cls):
        return 6


    def toArray(self):
        return pack('<hhh', self.x, self.y, self.z)


    @classmethod
    def parse(cls, dataArray):
        data = Vector()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.x, data.y, data.z = unpack('<hhh', dataArray)
        
        return data



class Count(ISerializable):

    def __init__(self):
        self.timeSystem     = 0
        self.timeDrive      = 0

        self.countStart     = 0
        self.countStop      = 0
        self.countAccident  = 0


    @classmethod
    def getSize(cls):
        return 14


    def toArray(self):
        return pack('<QQHHH', self.timeSystem, self.timeDrive, self.countStart, self.countStop, self.countAccident)


    @classmethod
    def parse(cls, dataArray):
        data = Count()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.timeSystem, data.timeDrive, data.countStart, data.countStop, data.countAccident = unpack('<QQHHH', dataArray)
        
        return data



class Bias(ISerializable):
    
    def __init__(self):
        self.accelX     = 0
        self.accelY     = 0
        self.accelZ     = 0
        self.gyroRoll   = 0
        self.gyroPitch  = 0
        self.gyroYaw    = 0


    @classmethod
    def getSize(cls):
        return 12


    def toArray(self):
        return pack('<hhhhhh', self.accelX, self.accelY, self.accelZ, self.gyroRoll, self.gyroPitch, self.gyroYaw)


    @classmethod
    def parse(cls, dataArray):
        data = Bias()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.accelX, data.accelY, data.accelZ, data.gyroRoll, data.gyroPitch, data.gyroYaw = unpack('<hhhhhh', dataArray)
        
        return data


# Sensor End



# Device Start


class MotorBlock(ISerializable):

    def __init__(self):
        self.rotation   = Rotation.None_
        self.value      = 0


    @classmethod
    def getSize(cls):
        return 3


    def toArray(self):
        return pack('<Bh', self.rotation.value, self.value)


    @classmethod
    def parse(cls, dataArray):
        data = MotorBlock()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.rotation, data.value = unpack('<Bh', dataArray)
        data.rotation = Rotation(data.rotation)
        
        return data



class Motor(ISerializable):

    def __init__(self):
        self.motor      = []
        self.motor.append(MotorBlock())
        self.motor.append(MotorBlock())
        self.motor.append(MotorBlock())
        self.motor.append(MotorBlock())


    @classmethod
    def getSize(cls):
        return MotorBlock.getSize() * 4


    def toArray(self):
        dataArray = bytearray()
        dataArray.extend(self.motor[0].toArray())
        dataArray.extend(self.motor[1].toArray())
        dataArray.extend(self.motor[2].toArray())
        dataArray.extend(self.motor[3].toArray())
        return dataArray


    @classmethod
    def parse(cls, dataArray):
        data = Motor()
        
        if len(dataArray) != cls.getSize():
            return None
        
        indexStart = 0;        indexEnd  = MotorBlock.getSize();    data.motor[0]   = MotorBlock.parse(dataArray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += MotorBlock.getSize();    data.motor[1]   = MotorBlock.parse(dataArray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += MotorBlock.getSize();    data.motor[2]   = MotorBlock.parse(dataArray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += MotorBlock.getSize();    data.motor[3]   = MotorBlock.parse(dataArray[indexStart:indexEnd])
        
        return data



class MotorSingle(ISerializable):

    def __init__(self):
        self.target     = 0
        self.rotation   = Rotation.None_
        self.value      = 0


    @classmethod
    def getSize(cls):
        return 4


    def toArray(self):
        return pack('<BBh', self.target, self.rotation.value, self.value)


    @classmethod
    def parse(cls, dataArray):
        data = MotorSingle()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.target, data.rotation, data.value = unpack('<BBh', dataArray)
        data.rotation = Rotation(data.rotation)
        
        return data



class InformationAssembledForController(ISerializable):

    def __init__(self):
        self.angleRoll              = 0
        self.anglePitch             = 0
        self.angleYaw               = 0
        
        self.rpm                    = 0
        
        self.positionX              = 0
        self.positionY              = 0
        self.positionZ              = 0
        
        self.speedX                 = 0
        self.speedY                 = 0
        
        self.rangeHeight            = 0
        
        self.rssi                   = 0


    @classmethod
    def getSize(cls):
        return 18


    def toArray(self):
        return pack('<hhhHhhhbbBb', self.angleRoll, self.anglePitch, self.angleYaw, 
                                    self.rpm,
                                    self.positionX, self.positionY, self.positionZ, 
                                    self.speedX, self.speedY, 
                                    self.rangeHeight,
                                    self.rssi)


    @classmethod
    def parse(cls, dataArray):
        data = InformationAssembledForController()
        
        if len(dataArray) != cls.getSize():
            return None
        
        (data.angleRoll, data.anglePitch, data.angleYaw, 
        data.rpm,
        data.positionX, data.positionY, data.positionZ, 
        data.speedX, data.speedY, 
        data.rangeHeight,
        data.rssi) = unpack('<hhhHhhhbbBb', dataArray)
        
        return data



class InformationAssembledForEntry(ISerializable):

    def __init__(self):
        self.angleRoll      = 0
        self.anglePitch     = 0
        self.angleYaw       = 0
        
        self.positionX      = 0
        self.positionY      = 0
        self.positionZ      = 0

        self.rangeHeight    = 0
        self.altitude       = 0


    @classmethod
    def getSize(cls):
        return 18


    def toArray(self):
        return pack('<hhhhhhhf',    self.angleRoll, self.anglePitch, self.angleYaw,
                                    self.positionX, self.positionY, self.positionZ,
                                    self.rangeHeight, self.altitude)


    @classmethod
    def parse(cls, dataArray):
        data = InformationAssembledForEntry()
        
        if len(dataArray) != cls.getSize():
            return None
        
        (data.angleRoll, data.anglePitch, data.angleYaw, 
        data.positionX, data.positionY, data.positionZ, 
        data.rangeHeight, data.altitude) = unpack('<hhhhhhhf', dataArray)
        
        return data



# Device End



# Link Start


class LinkState(ISerializable):

    def __init__(self):
        self.modeLink           = ModeLink.None_


    @classmethod
    def getSize(cls):
        return 1


    def toArray(self):
        return pack('<B', self.modeLink)


    @classmethod
    def parse(cls, dataArray):
        data = LinkState()
        
        if len(dataArray) != cls.getSize():
            return None

        data.modeLink, = unpack('<B', dataArray)
        data.modeLink           = ModeLink(data.modeLink)

        return data



class LinkEvent(ISerializable):

    def __init__(self):
        self.eventLink      = EventLink.None_
        self.eventResult    = 0


    @classmethod
    def getSize(cls):
        return 2


    def toArray(self):
        return pack('<BB', self.eventLink.value, self.eventResult)


    @classmethod
    def parse(cls, dataArray):
        data = LinkEvent()
        
        if len(dataArray) != cls.getSize():
            return None

        data.eventLink, data.eventResult = unpack('<BB', dataArray)
        data.eventLink = EventLink(data.eventLink)

        return data



class LinkEventAddress(ISerializable):

    def __init__(self):
        self.eventLink      = EventLink.None_
        self.eventResult    = 0
        self.address        = bytearray()


    @classmethod
    def getSize(cls):
        return 8


    def toArray(self):
        dataArray = bytearray()
        dataArray.extend(pack('<BB', self.eventLink.value, self.eventResult))
        dataArray.extend(self.address)
        return dataArray


    @classmethod
    def parse(cls, dataArray):
        data = LinkEventAddress()
        
        if len(dataArray) != cls.getSize():
            return None

        data.eventLink, data.eventResult = unpack('<BB', dataArray[0:2])
        data.address = dataArray[2:8]

        data.eventLink = EventLink(data.eventLink)

        return data



class LinkRssi(ISerializable):

    def __init__(self):
        self.rssi       = 0


    @classmethod
    def getSize(cls):
        return 1


    def toArray(self):
        return pack('<b', self.rssi)


    @classmethod
    def parse(cls, dataArray):
        data = LinkRssi()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.rssi, = unpack('<b', dataArray)

        return data



class LinkDiscoveredDevice(ISerializable):

    def __init__(self):
        self.index      = 0
        self.address    = bytearray()
        self.name       = ""
        self.rssi       = 0


    @classmethod
    def getSize(cls):
        return 28


    def toArray(self):
        dataArray = bytearray()
        dataArray.extend(pack('<B', self.index))
        dataArray.extend(self.address)
        dataArray.extend(self.name.encode('ascii', 'ignore'))   # 문자열 데이터의 길이가 고정이기 때문에 그에 대한 처리가 필요하나, 파이썬에서 이 데이터를 전송하지는 않기 때문에 일단 이대로 둠
        dataArray.extend(pack('<b', self.rssi))
        return dataArray


    @classmethod
    def parse(cls, dataArray):
        data = LinkEventAddress()
        
        if len(dataArray) != cls.getSize():
            return None

        indexStart = 0;        indexEnd = 1;    data.index,     = unpack('<B', (dataArray[indexStart:indexEnd]))
        indexStart = indexEnd; indexEnd += 6;   data.address    = dataArray[indexStart:indexEnd]
        indexStart = indexEnd; indexEnd += 20;  data.name       = dataArray[indexStart:indexEnd].decode()
        indexStart = indexEnd; indexEnd += 1;   data.rssi,      = unpack('<b', (dataArray[indexStart:indexEnd]))

        return data



class LinkPasscode(ISerializable):

    def __init__(self):
        self.passcode       = 0


    @classmethod
    def getSize(cls):
        return 4


    def toArray(self):
        return pack('<I', self.passcode)


    @classmethod
    def parse(cls, dataArray):
        data = LinkPasscode()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.passcode, = unpack('<I', dataArray)

        return data


# Link End


