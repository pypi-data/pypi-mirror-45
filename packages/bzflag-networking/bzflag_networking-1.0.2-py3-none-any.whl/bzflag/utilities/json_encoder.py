import json

from typing import List

from bzflag.networking.game_packet import GamePacket
from bzflag.utilities.json_serializable import JsonSerializable


class RRLogEncoder(json.JSONEncoder):
    black_list: List[str] = []
    white_list: List[str] = []

    def default(self, obj):
        if not isinstance(obj, JsonSerializable):
            return str(obj)

        if len(RRLogEncoder.white_list) > 0:
            if isinstance(obj, GamePacket) and obj.packet_type not in RRLogEncoder.white_list:
                return {}

        if isinstance(obj, GamePacket) and obj.packet_type in RRLogEncoder.black_list:
            return {}

        return obj.to_dict()
