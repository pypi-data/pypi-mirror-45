from typing import Optional

from bzflag.networking.game_data_player_state import PlayerStateData
from bzflag.networking.game_packet import GamePacket
from bzflag.networking.packet import Packet


class MsgPlayerUpdatePacket(GamePacket):
    __slots__ = (
        'player_id',
        'state',
    )

    def __init__(self):
        super().__init__()

        self.packet_type: str = 'MsgPlayerUpdate'
        self.player_id: int = -1
        self.state: Optional[PlayerStateData] = None

    def _unpack(self):
        # Discard this value; I'm not sure why this value comes out to a weird
        # float. We have the timestamp of the raw packet, so just that instead
        _ = Packet.unpack_float(self.buffer)

        self.player_id = Packet.unpack_uint8(self.buffer)
        self.state = Packet.unpack_player_state(self.buffer, self.packet.code)
