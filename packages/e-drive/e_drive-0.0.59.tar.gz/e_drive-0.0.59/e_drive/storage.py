import time

from e_drive.protocol import *
from e_drive.system import *


# EventHandler
class EventHandler:

    def __init__(self):
        self.d = dict.fromkeys(list(DataType))



# StorageHeader
class StorageHeader:

    def __init__(self):
        self.d = dict.fromkeys(list(DataType))



# Storage
class Storage:

    def __init__(self):
        self.d = dict.fromkeys(list(DataType))



# Storage Count
class StorageCount:

    def __init__(self):
        self.d = dict.fromkeys(list(DataType))
        
        for key in self.d:
            self.d[key] = 0



# Storage
class DataParser:

    def __init__(self):
        self.d = dict.fromkeys(list(DataType))

        self.d[DataType.Ping]               = Ping.parse
        self.d[DataType.Ack]                = Ack.parse
        self.d[DataType.Error]              = Error.parse
        self.d[DataType.Message]            = Message.parse
        self.d[DataType.Address]            = Address.parse
        self.d[DataType.Information]        = Information.parse
        self.d[DataType.UpdateLocation]     = UpdateLocation.parse
        self.d[DataType.SystemInformation]  = SystemInformation.parse
        self.d[DataType.Registration]       = RegistrationInformation.parse

        self.d[DataType.RawMotion]          = RawMotion.parse
        self.d[DataType.RawLineTracer]      = RawLineTracer.parse
        self.d[DataType.RawCard]            = RawCard.parse
        self.d[DataType.RawCardList]        = RawCardList.parse

        self.d[DataType.State]              = State.parse
        self.d[DataType.Attitude]           = Attitude.parse
        self.d[DataType.Position]           = Position.parse
        self.d[DataType.Motion]             = Motion.parse
        self.d[DataType.Range]              = Range.parse

        self.d[DataType.Count]              = Count.parse
        self.d[DataType.Bias]               = Bias.parse
        self.d[DataType.Trim]               = Trim.parse

        self.d[DataType.Button]             = Button.parse

        self.d[DataType.InformationAssembledForController]  = InformationAssembledForController.parse
        self.d[DataType.InformationAssembledForEntry]       = InformationAssembledForEntry.parse

        self.d[DataType.LinkState]              = LinkState.parse
        self.d[DataType.LinkEvent]              = LinkEvent.parse
        self.d[DataType.LinkEventAddress]       = LinkEventAddress.parse
        self.d[DataType.LinkRssi]               = LinkRssi.parse
        self.d[DataType.LinkDiscoveredDevice]   = LinkDiscoveredDevice.parse
        self.d[DataType.LinkPasscode]           = LinkPasscode.parse

