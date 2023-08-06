import warnings

from bzflag.networking.msg_flag_drop import MsgFlagDropPacket


class MsgDropFlagPacket(MsgFlagDropPacket):
    warnings.warn("use the `MsgFlagDropPacket` class now", DeprecationWarning)

    pass
