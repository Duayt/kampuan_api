from dataclasses import asdict, dataclass


@dataclass
class SourceInfo:
    source_type: str
    auto_mode: bool
    current_bot: str

    @classmethod
    def new(cls, env):
        return cls('new', True, env)

    @classmethod
    def rejoin(cls, env):
        return cls('rejoin', True, env)

    @classmethod
    def old(cls, env):
        return cls('old_room', True, env)

    def to_dict(self):
        return asdict(self)
