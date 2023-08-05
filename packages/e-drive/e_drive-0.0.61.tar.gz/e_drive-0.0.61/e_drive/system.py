from enum import Enum


class ModelNumber(Enum):
    
    None_                   = 0x00000000

    Drone_3_Drone_P1        = 0x00031001    # Drone_3_Drone_P1 (Lightrone / GD65 / HW2181 / Keil / 3.7v / barometer / RGB LED / Shaking binding)
    Drone_3_Drone_P2        = 0x00031002    # Drone_3_Drone_P2 (Soccer Drone / HW2181 / Keil / 7.4v / barometer / RGB LED / Shaking binding)
    Drone_3_Drone_P3        = 0x00031003    # Drone_3_Drone_P3 (GD240 / HW2181 / Keil / power button / u30 flow / 3.7v / geared motor / barometer)
    Drone_3_Drone_P4        = 0x00031004    # Drone_3_Drone_P4 (GD50N / HW2181 / Keil / power button / 3.7v / barometer)
    Drone_3_Drone_P5        = 0x00031005    # Drone_3_Drone_P5 (GD30 / HW2181 / Keil / 3.7v / nomal binding)
    Drone_3_Drone_P6        = 0x00031006    # Drone_3_Drone_P6 (Soccer Drone 2 / HW2181 / Keil / 7.4v / barometer / RGB LED / Shaking binding)

    Drone_3_Controller_P1   = 0x00032001    # Drone_3_Controller_P1
    Drone_3_Controller_P2   = 0x00032002    # Drone_3_Controller_P2

    Drone_4_Drone_P4        = 0x00041004    # Drone_4_Drone_P4
    Drone_4_Drone_P5        = 0x00041005    # Drone_4_Drone_P5 - E-Drone

    Drone_4_Controller_P1   = 0x00042001    # Drone_4_Controller_P1
    Drone_4_Controller_P2   = 0x00042002    # Drone_4_Controller_P2

    Drone_4_Link_P0         = 0x00043000    # Drone_4_Link_P0

    Drone_4_Tester_P2       = 0x0004A002    # Drone_4_Tester_P2
    Drone_4_Monitor_P2      = 0x0004A102    # Drone_4_Monitor_P2
    
    Drone_7_Drone_P1        = 0x00041001    # Drone_7_Drone_P1 - E-Drive
    Drone_7_BleClient_P0    = 0x00073200    # Drone_7_BleClient_P0
    Drone_7_BleServer_P0    = 0x00073300    # Drone_7_BleServer_P0



class DeviceType(Enum):

    None_           = 0x00

    Drone           = 0x10      # 드론(Server)

    Controller      = 0x20      # 조종기(Client)

    LinkClient      = 0x30      # 링크 모듈(Client)
    LinkServer      = 0x31      # 링크 모듈(Server, 링크 모듈이 서버로 동작하는 경우에만 통신 타입을 잠시 바꿈)
    BleClient       = 0x32      # BLE 클라이언트
    BleServer       = 0x33      # BLE 서버

    Range           = 0x40      # 거리 센서 모듈

    Base            = 0x70      # 베이스

    ByScratch       = 0x80      # 바이스크래치
    Scratch         = 0x81      # 스크래치
    Entry           = 0x82      # 네이버 엔트리

    Tester          = 0xA0      # 테스터
    Monitor         = 0xA1      # 모니터
    Updater         = 0xA2      # 펌웨어 업데이트 도구
    Encrypter       = 0xA3      # 암호화 도구

    Broadcasting    = 0xFF



class ModeSystem(Enum):
    
    None_               = 0x00

    Boot                = 0x01
    Start               = 0x02
    Running             = 0x03
    ReadyToReset        = 0x04
    Error               = 0x05

    EndOfType           = 0x06



class ModeDrive(Enum):
    
    None_               = 0x00

    Ready               = 0x10

    Start               = 0x11
    Drive               = 0x12

    Stop                = 0x20

    Accident            = 0x30
    Error               = 0x31

    Test                = 0x40

    EndOfType           = 0x41



class ModeUpdate(Enum):
    
    None_               = 0x00

    Ready               = 0x01      # 업데이트 가능 상태
    Update              = 0x02      # 업데이트 중
    Complete            = 0x03      # 업데이트 완료

    Failed              = 0x04      # 업데이트 실패(업데이트 완료까지 갔으나 body의 CRC16이 일치하지 않는 경우 등)

    NotAvailable        = 0x05      # 업데이트 불가능 상태(Debug 모드 등)
    RunApplication      = 0x06      # 어플리케이션 동작 중
    NotRegistered       = 0x07      # 등록되지 않음

    EndOfType           = 0x08



class ErrorFlagsForSensor(Enum):

    None_                                   = 0x00000000

    Motion_NoAnswer                         = 0x00000001    # Motion 센서 응답 없음
    Motion_WrongValue                       = 0x00000002    # Motion 센서 잘못된 값
    Motion_NotCalibrated                    = 0x00000004    # Gyro Bias 보정이 완료되지 않음
    Motion_Calibrating                      = 0x00000008    # Gyro Bias 보정 중



class ErrorFlagsForState(Enum):

    None_                                   = 0x00000000

    NotRegistered                           = 0x00000001    # 장치 등록이 안됨
    FlashReadLock_UnLocked                  = 0x00000002    # 플래시 메모리 읽기 Lock이 안 걸림
    BootloaderWriteLock_UnLocked            = 0x00000004    # 부트로더 영역 쓰기 Lock이 안 걸림



class DriveEvent(Enum):
    
    None_               = 0x00

    Stop                = 0x10

    EndOfType           = 0x11



class Direction(Enum):
    
    None_               = 0x00

    Left                = 0x01
    Front               = 0x02
    Right               = 0x03
    Rear                = 0x04

    Top                 = 0x05
    Bottom              = 0x06

    Center              = 0x07

    EndOfType           = 0x08



class Rotation(Enum):
    
    None_               = 0x00

    Clockwise           = 0x01
    Counterclockwise    = 0x02

    EndOfType           = 0x03



class ModeMovement(Enum):
    
    None_               = 0x00

    Ready               = 0x01      # Ready
    Moving              = 0x02      # Moving
    Stop                = 0x03      # Stop

    EndOfType           = 0x04



class CardColor(Enum):
    
    Unknown         = 0x00
    
    White           = 0x01
    Red             = 0x02
    Yellow          = 0x03
    Green           = 0x04
    Cyan            = 0x05
    Blue            = 0x06
    Magenta         = 0x07
    Black           = 0x08

    EndOfType       = 0x09



class Card(Enum):
    
    None_           = 0x00

    WhiteWhite      = 0x11
    WhiteRed        = 0x12
    WhiteYellow     = 0x13
    WhiteGreen      = 0x14
    WhiteCyan       = 0x15
    WhiteBlue       = 0x16
    WhiteMagenta    = 0x17
    WhiteBlack      = 0x18

    RedWhite        = 0x21
    RedRed          = 0x22
    RedYellow       = 0x23
    RedGreen        = 0x24
    RedCyan         = 0x25
    RedBlue         = 0x26
    RedMagenta      = 0x27
    RedBlack        = 0x28

    YellowWhite     = 0x31
    YellowRed       = 0x32
    YellowYellow    = 0x33
    YellowGreen     = 0x34
    YellowCyan      = 0x35
    YellowBlue      = 0x36
    YellowMagenta   = 0x37
    YellowBlack     = 0x38

    GreenWhite      = 0x41
    GreenRed        = 0x42
    GreenYellow     = 0x43
    GreenGreen      = 0x44
    GreenCyan       = 0x45
    GreenBlue       = 0x46
    GreenMagenta    = 0x47
    GreenBlack      = 0x48

    CyanWhite       = 0x51
    CyanRed         = 0x52
    CyanYellow      = 0x53
    CyanGreen       = 0x54
    CyanCyan        = 0x55
    CyanBlue        = 0x56
    CyanMagenta     = 0x57
    CyanBlack       = 0x58

    BlueWhite       = 0x61
    BlueRed         = 0x62
    BlueYellow      = 0x63
    BlueGreen       = 0x64
    BlueCyan        = 0x65
    BlueBlue        = 0x66
    BlueMagenta     = 0x67
    BlueBlack       = 0x68

    MagentaWhite    = 0x71
    MagentaRed      = 0x72
    MagentaYellow   = 0x73
    MagentaGreen    = 0x74
    MagentaCyan     = 0x75
    MagentaBlue     = 0x76
    MagentaMagenta  = 0x77
    MagentaBlack    = 0x78

    BlackWhite      = 0x81
    BlackRed        = 0x82
    BlackYellow     = 0x83
    BlackGreen      = 0x84
    BlackCyan       = 0x85
    BlackBlue       = 0x86
    BlackMagenta    = 0x87
    BlackBlack      = 0x88



class ModeLink(Enum):
    
    None_               = 0x00

    Boot                = 0x01      # 부팅
    Ready               = 0x02      # 대기(연결 전)
    Connecting          = 0x03      # 장치 연결 중
    Connected           = 0x04      # 장치 연결 완료(정상 연결 됨)
    Disconnecting       = 0x05      # 장치 연결 해제 중

    ReadyToReset        = 0x06      # 리셋 대기(1초 뒤 리셋)

    EndOfType           = 0x07



class EventLink(Enum):

    None_                               = 0x00  # 없음

    SystemReset                         = 0x01  # 시스템 리셋

    Initialized                         = 0x02  # 장치 초기화 완료

    Scanning                            = 0x03  # 장치 검색 시작
    ScanStop                            = 0x04  # 장치 검색 중단

    FoundDroneService                   = 0x05  # 드론 서비스 검색 완료

    Connecting                          = 0x06  # 장치 연결 시작		
    Connected                           = 0x07  # 장치 연결

    ConnectionFailed                    = 0x08  # 연결 실패
    ConnectionFailedNoDevices           = 0x09  # 연결 실패 - 장치가 없음
    ConnectionFailedNotReady            = 0x0A  # 연결 실패 - 대기 상태가 아님

    PairingStart                        = 0x0B  # 페어링 시작
    PairingSuccess                      = 0x0C  # 페어링 성공
    PairingFailed                       = 0x0D  # 페어링 실패

    BondingSuccess                      = 0x0E  # Bonding 성공

    LookupAttribute                     = 0x0F  # 장치 서비스 및 속성 검색(GATT Event 실행)

    RssiPollingStart                    = 0x10  # RSSI 풀링 시작
    RssiPollingStop                     = 0x11  # RSSI 풀링 중지

    DiscoverService                     = 0x12  # 서비스 검색
    DiscoverCharacteristic              = 0x13  # 속성 검색
    DiscoverCharacteristicDroneData     = 0x14  # 속성 검색
    DiscoverCharacteristicDroneConfig   = 0x15  # 속성 검색
    DiscoverCharacteristicUnknown       = 0x16  # 속성 검색
    DiscoverCCCD                        = 0x17  # CCCD 검색

    ReadyToControl                      = 0x18  # 제어 준비 완료

    Disconnecting                       = 0x19  # 장치 연결 해제 시작
    Disconnected                        = 0x1A  # 장치 연결 해제 완료

    GapLinkParamUpdate                  = 0x1B  # GAP_LINK_PARAM_UPDATE_EVENT

    RspReadError                        = 0x1C  # RSP 읽기 오류
    RspReadSuccess                      = 0x1D  # RSP 읽기 성공

    RspWriteError                       = 0x1E  # RSP 쓰기 오류
    RspWriteSuccess                     = 0x1F  # RSP 쓰기 성공

    SetNotify                           = 0x20  # Notify 활성화

    Write                               = 0x21 # 데이터 쓰기 이벤트

    EndOfType                           = 0x22 



class ModeLinkDiscover(Enum):

    None_               = 0x00

    Name                = 0x01      # 이름을 기준으로 검색
    Service             = 0x02      # 서비스를 기준으로 검색
    All                 = 0x03      # 모든 장치 검색

    EndOfType           = 0x04



class ImageType(Enum):

    None_                   = 0x00

    # 현재 장치의 이미지
    ImageSingle             = 0x10      # 실행 이미지
    ImageA                  = 0x11
    ImageB                  = 0x12
    
    # 펌웨어 이미지
    RawImageSingle          = 0x20      # 업데이트 이미지
    RawImageA               = 0x21
    RawImageB               = 0x22
    
    # 암호화 된 이미지
    EncryptedImageSingle    = 0x30      # 업데이트 이미지
    EncryptedImageA         = 0x31
    EncryptedImageB         = 0x32

    EndOfType               = 0x40


