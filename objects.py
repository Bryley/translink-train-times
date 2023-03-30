from pydantic import BaseModel, validator
from datetime import datetime, timedelta

Place = str

class Stop(BaseModel):
    id: int
    name: str
    platform: int

    def __hash__(self):
        return hash((self.id, self.name, self.platform))

    def __eq__(self, other):
        if not isinstance(other, Stop):
            return NotImplemented
        return (
            self.id == other.id
            and self.name == other.name
            and self.platform == other.platform
        )

    def __str__(self) -> str:
        return self.name


class Trip(BaseModel):
    dep_time: datetime
    arrive_time: datetime

    @validator("dep_time", pre=True)
    def validate_dep_time(cls, val: int) -> datetime:
        return datetime.fromtimestamp(val)

    @validator("arrive_time", pre=True)
    def validate_arrive_time(cls, val: int) -> datetime:
        return datetime.fromtimestamp(val)

    def output(self, from_stop: Stop, to_stop: Stop) -> str:
        FORMAT = "%I:%M:%S %p"
        dep = self.dep_time.strftime(FORMAT)
        arr = self.arrive_time.strftime(FORMAT)
        in_ = self.dep_time - datetime.now()
        leave = (self.dep_time - timedelta(minutes=12)).strftime(FORMAT)
        return f"{from_stop} -> {to_stop}: Dep: {dep} ({round(in_.total_seconds() / 60)} mins) | Arr: {arr} | Leave at [magenta]{leave}[/]"
