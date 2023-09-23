from typing import Dict, List, Union
from functools import cache

_irp_mj_mapping: Dict[int, str] = {
    0x00: "IRP_MJ_CREATE",
    0x01: "IRP_MJ_CREATE_NAMED_PIPE",
    0x02: "IRP_MJ_CLOSE",
    0x03: "IRP_MJ_READ",
    0x04: "IRP_MJ_WRITE",
    0x05: "IRP_MJ_QUERY_INFORMATION",
    0x06: "IRP_MJ_SET_INFORMATION",
    0x07: "IRP_MJ_QUERY_EA",
    0x08: "IRP_MJ_SET_EA",
    0x09: "IRP_MJ_FLUSH_BUFFERS",
    0x0A: "IRP_MJ_QUERY_VOLUME_INFORMATION",
    0x0B: "IRP_MJ_SET_VOLUME_INFORMATION",
    0x0C: "IRP_MJ_DIRECTORY_CONTROL",
    0x0D: "IRP_MJ_FILE_SYSTEM_CONTROL",
    0x0E: "IRP_MJ_DEVICE_CONTROL",
    0x0F: "IRP_MJ_INTERNAL_DEVICE_CONTROL",
    0x10: "IRP_MJ_SHUTDOWN",
    0x11: "IRP_MJ_LOCK_CONTROL",
    0x12: "IRP_MJ_CLEANUP",
    0x13: "IRP_MJ_CREATE_MAILSLOT",
    0x14: "IRP_MJ_QUERY_SECURITY",
    0x15: "IRP_MJ_SET_SECURITY",
    0x16: "IRP_MJ_POWER",
    0x17: "IRP_MJ_SYSTEM_CONTROL",
    0x18: "IRP_MJ_DEVICE_CHANGE",
    0x19: "IRP_MJ_QUERY_QUOTA",
    0x1A: "IRP_MJ_SET_QUOTA",
    0x1B: "IRP_MJ_PNP",
}


@cache
def irp2str(mj: int) -> str:
    try:
        return _irp_mj_mapping[mj]
    except IndexError:
        return ""


@cache
def str2irp(name: str) -> Union[int, None]:
    values: List[str] = list(_irp_mj_mapping.values())
    try:
        return list(_irp_mj_mapping.keys())[values.index(name)]
    except (IndexError, ValueError):
        return None
