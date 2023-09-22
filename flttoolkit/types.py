from pykd import typedVar, typedVarList, module, addr64
from enum import Enum
from typing import *
from dataclasses import dataclass

# Cache types for to prevent redundant lookups. These fields should not be accessed directly.
_INTERNAL_FLT_MGR: Any = module("fltmgr")
_INTERNAL_FLT_OBJECT: Any = _INTERNAL_FLT_MGR.type("_FLT_OBJECT")
_INTERNAL_FLT_VOLUME: Any = _INTERNAL_FLT_MGR.type("_FLT_VOLUME")

_INTERNAL_NT: Any = module("nt")
_INTERNAL_NT_DEVICE_OBJ: Any = _INTERNAL_NT.type("_DEVICE_OBJECT")
_INTERNAL_NT_UNICODE_STRING: Any = _INTERNAL_NT.type("_UNICODE_STRING")
_INTERNAL_NT_ERESOURCE: Any = _INTERNAL_NT.type("_ERESOURCE")


class FLT_OBJECT:
    class _FLT_OBJECT_FLAGS(Enum):
        FLT_OBFL_DRAINING = 1
        FLT_OBFL_ZOMBIED = 2
        FLT_OBFL_TYPE_INSTANCE = 0x1000000
        FLT_OBFL_TYPE_FILTER = 0x2000000
        FLT_OBFL_TYPE_VOLUME = 0x4000000

    def __init__(self, address: int) -> None:
        self._flt: typedVar = typedVar(_INTERNAL_FLT_OBJECT, address)
        self._addr: int = address

    def __repr__(self) -> str:
        return f"FLT_OBJECT({hex(int(self._addr))})"

    @property
    def Flags(self) -> int:
        """Return the current a bitfield represented as an integer containing the flags set for this object.

        :return: An integer encoding the current `_FLT_OBJECT_FLAGS` set for this object.
        :rtype: int
        """
        return int(self._flt.Flags)

    @property
    def PointerCount(self) -> int:
        """Return the current number of references to this object.

        :return: An integer containing the current number of references to this object.
        :rtype: int
        """
        return int(self._flt.PointerCount)

    @property
    def RundownRef(self) -> int:
        """Return a pointer to the `EX_RUNDOWN_REF` for this object. This object can be reference by the kernel API `ExAcquireRundownProtection`
        to lock an object during user manipulation to prevent deletion/deallocation.

        :return: An integer representing a pointer to a `_EX_RUNDOWN_REF` kernel object.
        :rtype: int
        """
        return int(self._flt.RundownRef)

    @property
    def PrimaryLink(self) -> int:
        """Return the linked list entry for this `FLT_OBJECT`.

        :return: An integer representing a pointer to a `_LIST_ENTRY` kernel object.
        :rtype: int
        """
        return int(self._flt.PrimaryLink)

    @property
    def UniqueIdentifier(self):
        """Unique identifier for this object. Note: Not all objects implement this, and this value can be 0.

        :return: The GUID for the object if set, `None` otherwise.
        :rtype: str
        """
        return self._flt.UniqueIdentifier

    @property
    def object_zombied(self) -> bool:
        """Check if the underlying object is zombied.

        :return: `True` if the flag `FLT_OBFL_DRAINING` is zombied, `False` otherwise.
        :rtype: bool
        """
        return (self.Flags & self._FLT_OBJECT_FLAGS.FLT_OBFL_ZOMBIED.value) != 0

    @property
    def object_draining(self) -> bool:
        """Check if the underlying object is currently draining.

        :return: `True` if the flag `FLT_OBFL_DRAINING` is set, `False` otherwise.
        :rtype: bool
        """
        return (self.Flags & self._FLT_OBJECT_FLAGS.FLT_OBFL_DRAINING.value) != 0

    @property
    def is_instance_type(self) -> bool:
        """Check if the underlying object is of type `FLT_INSTANCE`

        :return: `True` if object is of type `FLT_INSTANCE`, `False` otherwise.
        :rtype: bool
        """
        return (self.Flags & self._FLT_OBJECT_FLAGS.FLT_OBFL_TYPE_INSTANCE.value) != 0

    @property
    def is_filter_type(self) -> bool:
        """Check if the underlying object is of type `FLT_FILTER`

        :return: `True` if object is of type `FLT_FILTER`, `False` otherwise.
        :rtype: bool
        """
        return (self.Flags & self._FLT_OBJECT_FLAGS.FLT_OBFL_TYPE_FILTER.value) != 0

    @property
    def is_volume_type(self) -> bool:
        """Check if the underlying object is of type `FLT_VOLUME`.

        :return: `True` if this object is of type `FLT_VOLUME`, `False` otherwise.
        :rtype: bool
        """
        return (self.Flags & self._FLT_OBJECT_FLAGS.FLT_OBFL_TYPE_VOLUME.value) != 0

    def for_each(self, cb: Callable[["FLT_OBJECT"], None]) -> None:
        """Invoke `cb` for all `FLT_OBJECT`s found in the system

        :param cb: `Callable` object taking one argument of type `FLT_OBJECT` and returning `None`
        :type cb: Callable[["FLT_OBJECT"], None]
        """
        obj_list: List[FLT_OBJECT] = [
            FLT_OBJECT(obj)
            for obj in typedVarList(
                self._flt.PrimaryLink, "fltmgr!_FLT_OBJECT", "PrimaryLink"
            )
        ]

        for obj in obj_list:
            cb(obj)

    def __eq__(self, other: "FLT_OBJECT") -> bool:
        if not isinstance(other, FLT_OBJECT):
            return False
        return self._addr == other._addr


@dataclass
class FLT_VOLUME:
    class _FLT_VOLUME_FLAGS(Enum):
        VOLFL_NETWORK_FILESYSTEM = 1
        VOLFL_PENDING_MOUNT_SETUP_NOTIFIES = 2
        VOLFL_MOUNT_SETUP_NOTIFIES_CALLED = 4
        VOLFL_MOUNTING = 8
        VOLFL_SENT_SHUTDOWN_IRP = 16
        VOLFL_ENABLE_NAME_CACHING = 32
        VOLFL_FILTER_EVER_ATTACHED = 64
        VOLFL_STANDARD_LINK_NOT_SUPPORTED = 128
        VOLFL_ENABLE_DATASCAN = 256
        VOLFL_READ_ONLY_DATASCAN = 512
        VOLFL_SUPPORTED_FEATURES_KNOWN = 1024
        VOLFL_DAX_VOLUME = 2048

    class _FLT_FILESYSTEM_TYPE(Enum):
        FLT_FSTYPE_UNKNOWN = 0
        FLT_FSTYPE_RAW = 1
        FLT_FSTYPE_NTFS = 2
        FLT_FSTYPE_FAT = 3
        FLT_FSTYPE_CDFS = 4
        FLT_FSTYPE_UDFS = 5
        FLT_FSTYPE_LANMAN = 6
        FLT_FSTYPE_WEBDAV = 7
        FLT_FSTYPE_RDPDR = 8
        FLT_FSTYPE_NFS = 9
        FLT_FSTYPE_MS_NETWARE = 10
        FLT_FSTYPE_NETWARE = 11
        FLT_FSTYPE_BSUDF = 12
        FLT_FSTYPE_MUP = 13
        FLT_FSTYPE_RSFX = 14
        FLT_FSTYPE_ROXIO_UDF1 = 15
        FLT_FSTYPE_ROXIO_UDF2 = 16
        FLT_FSTYPE_ROXIO_UDF3 = 17
        FLT_FSTYPE_TACIT = 18
        FLT_FSTYPE_FS_REC = 19
        FLT_FSTYPE_INCD = 20
        FLT_FSTYPE_INCD_FAT = 21
        FLT_FSTYPE_EXFAT = 22
        FLT_FSTYPE_PSFS = 23
        FLT_FSTYPE_GPFS = 24
        FLT_FSTYPE_NPFS = 25
        FLT_FSTYPE_MSFS = 26
        FLT_FSTYPE_CSVFS = 27
        FLT_FSTYPE_REFS = 28
        FLT_FSTYPE_OPENAFS = 29
        FLT_FSTYPE_CIMFS = 30

    def __init__(self, address: int) -> None:
        self._flt: typedVar(_INTERNAL_FLT_VOLUME, address)
        self._Base: FLT_OBJECT = FLT_OBJECT(int(self._flt.Base))

    @property
    def Base(self) -> int:
        return int(self._flt.Base)

    @property
    def Flags(self) -> int:
        return int(self._flt.Flags)

    @property
    def FileSystemType(self) -> int:
        return int(self._flt.FileSystemType)

    @property
    def DeviceObject(self) -> int:
        return int(self._flt.DeviceObject)

    @property
    def DiskDeviceObject(self) -> int:
        return int(self._flt.DiskDeviceObject)

    @property
    def FrameZeroVolume(self) -> int:
        return int(self._flt.FrameZeroVolume)

    @property
    def VolumeInNextFrame(self) -> int:
        return int(self._flt.VolumeInNextFrame)

    @property
    def Frame(self) -> int:
        return int(self._flt.Frame)

    def get_base(self) -> FLT_OBJECT:
        return self._Base

    def get_frame_zero_volume(self) -> ["FLT_VOLUME", None]:
        if self.FrameZeroVolume:
            return FLT_VOLUME(self.FrameZeroVolume)
        return None

    def get_volume_in_next_frame(self) -> ["FLT_VOLUME", None]:
        if self.VolumeInNextFrame:
            return FLT_VOLUME(self.VolumeInNextFrame)
        return None

    def get_fs_type(self) -> _FLT_FILESYSTEM_TYPE:
        match (self.FileSystemType):
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_UNKNOWN.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_UNKNOWN
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_RAW.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_RAW
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_NTFS.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_NTFS
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_FAT.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_FAT
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_CDFS.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_CDFS
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_UDFS.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_UDFS
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_LANMAN.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_LANMAN
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_WEBDAV.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_WEBDAV
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_RDPDR.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_RDPDR
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_NFS.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_NFS
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_MS_NETWARE.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_MS_NETWARE
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_NETWARE.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_NETWARE
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_BSUDF.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_BSUDF
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_MUP.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_MUP
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_RSFX.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_RSFX
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_ROXIO_UDF1.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_ROXIO_UDF1
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_ROXIO_UDF2.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_ROXIO_UDF2
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_ROXIO_UDF3.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_ROXIO_UDF3
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_TACIT.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_TACIT
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_FS_REC.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_FS_REC
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_INCD.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_INCD
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_INCD_FAT.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_INCD_FAT
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_EXFAT.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_EXFAT
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_PSFS.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_PSFS
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_GPFS.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_GPFS
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_NPFS.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_NPFS
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_MSFS.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_MSFS
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_CSVFS.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_CSVFS
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_REFS.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_REFS
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_OPENAFS.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_OPENAFS
            case self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_CIMFS.value:
                return self._FLT_FILESYSTEM_TYPE.FLT_FSTYPE_CIMFS


@dataclass
class FLT_FILTER:
    Base: ...
    Frame: ...
    Name: ...
    DefaultAltitude: ...
    Flags: ...
    DriverObject: ...
    InstanceList: ...
    VerifierExtension: ...
    VerifiedFiltersLink: ...
    FilterUnload: ...
    InstanceSetup: ...
    InstanceQueryTeardown: ...
    InstanceTeardownStart: ...
    InstanceTeardownComplete: ...
    SupportedContextsListHead: ...
    SupportedContexts: ...
    PreVolumeMount: ...
    PostVolumeMount: ...
    GenerateFileName: ...
    NormalizeNameComponent: ...
    NormalizeNameComponentEx: ...
    NormalizeContextCleanup: ...
    KtmNotification: ...
    SectionNotification: ...
    Operations: ...
    OldDriverUnload: ...
    ActiveOpens: ...
    ConnectionList: ...
    PortList: ...
    PortLock: ...


@dataclass
class FLT_PARAMETERS:
    # todo: find how to represent C unions in this class
    ...


@dataclass
class FLT_REGISTRATION:
    Size: ...
    Version: ...
    Flags: ...
    ContextRegistration: ...
    OperationRegistration: ...
    FilterUnloadCallback: ...
    InstanceSetupCallback: ...
    InstanceQueryTeardownCallback: ...
    InstanceTeardownStartCallback: ...
    InstanceTeardownCompleteCallback: ...
    GenerateFileNameCallback: ...
    NormalizeNameComponentCallback: ...
    NormalizeContextCleanupCallback: ...
    TransactionNotificationCallback: ...
    NormalizeNameComponentExCallback: ...
    SectionNotificationCallback: ...


@dataclass
class FLT_INSTANCE:
    Base: ...
    OperationRunDownRef: ...
    Volume: ...
    Filter: ...
    Flags: ...
    Altitude: ...
    Name: ...
    FilterLink: ...
    ContextLock: ...
    Context: ...
    TransactionContexts: ...
    TrackCompletionNodes: ...
    CallbackNodes: ...


@dataclass
class FLT_IO_PARAMETER_BLOCK:
    IrpFlags: ...
    MajorFunction: ...
    MinorFunction: ...
    OperationFlags: ...
    Reserved: ...
    TargetFileObject: ...
    TargetInstance: ...
    Parameters: ...


@dataclass
class FLT_VOLUME_PROPERTIES:
    DeviceType: ...
    DeviceCharacteristics: ...
    DeviceObjectFlags: ...
    AlignmentRequirement: ...
    SectorSize: ...
    Flags: ...
    FileSystemDriverName: ...
    FileSystemDeviceName: ...
    RealDeviceName: ...


@dataclass
class FLT_FILE_NAME_INFORMATION:
    Size: ...
    NamesParsed: ...
    Format: ...
    Name: ...
    Volume: ...
    Share: ...
    Extension: ...
    Stream: ...
    FinalComponent: ...
    ParentDir: ...


@dataclass
class FLT_RELATED_OBJECTS:
    Size: ...
    TransactionContext: ...
    Filter: ...
    Volume: ...
    Instance: ...
    FileObject: ...
    Transaction: ...


@dataclass
class FLT_TAG_DATA_BUFFER:
    FileTag: ...
    TagDataLength: ...
    UnparsedNameLength: ...


@dataclass
class PFLT_CONTEXT:
    ...


@dataclass
class FLT_RELATED_CONTEXTS:
    VolumeContext: PFLT_CONTEXT
    InstanceContext: PFLT_CONTEXT
    FileContext: PFLT_CONTEXT
    StreamContext: PFLT_CONTEXT
    StreamHandleContext: PFLT_CONTEXT
    TransactionContext: PFLT_CONTEXT


@dataclass
class FLT_RELATED_CONTEXTS_EX:
    VolumeContext: PFLT_CONTEXT
    InstanceContext: PFLT_CONTEXT
    FileContext: PFLT_CONTEXT
    StreamContext: PFLT_CONTEXT
    StreamHandleContext: PFLT_CONTEXT
    TransactionContext: PFLT_CONTEXT
    SectionContext: PFLT_CONTEXT


@dataclass
class FLT_CALLBACK_DATA:
    Flags: ...
    Thread: ...
    Iopb: FLT_IO_PARAMETER_BLOCK
    IoStatus: ...
    TagData: ...
    FilterContext: ...
    RequestorMode: ...


@dataclass
class FLT_OPERATION_REGISTRATION:
    MajorFunction: ...
    Flags: ...
    PreOperation: ...
    PostOperation: ...
    Reserved1: ...


@dataclass
class FLT_NAME_CONTROL:
    Name: ...


@dataclass
class FLT_CALLBACK_DATA_QUEUE:
    Csq: ...
    Flags: ...
    InsertIo: ...
    RemoveIo: ...
    PeekNextIo: ...
    Acquire: ...
    Release: ...
    CompleteCanceledIo: ...


@dataclass
class FLT_CONTEXT_REGISTRATION:
    ContextType: ...
    Flags: ...
    ContextCleanupCallback: ...
    Size: ...
    PoolTag: ...
    ContextAllocatedCallback: ...
    ContextFreeCallback: ...
    Reserve1: ...


@dataclass
class FLT_CREATEFILE_TARGET_ECP_CONTEXT:
    Instance: FLT_INSTANCE
    Volume: FLT_VOLUME
    FileNameInformation: ...
    Flags: ...
