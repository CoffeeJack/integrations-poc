import typing
import dataclasses


ORM = typing.TypeVar("ORM")


@dataclasses.dataclass(frozen=True)
class SyncEntity:
    """
    This is an interface for "syncable" entities. It should be implemented for
    each model that needs to be synced with an external system.
    """

    local_id: int
    remote_id: typing.Optional[str]

    def __eq__(self, other):
        return (
            type(self).__name__ == type(other).__name__
            and self.local_id == other.local_id
        )

    def serialize(self):
        """Produces data that is ready to be sent to the remote system."""

        return dataclasses.asdict(self)

    @classmethod
    def deserialize(cls, data):
        """Accepts data from the remote system and instantiates a SyncEntity."""

        return cls(**data)

    def to_local(cls) -> ORM:
        """Create a local entity from instance of SyncEntity."""
        raise NotImplementedError()

    @classmethod
    def from_local(cls, model: ORM) -> "SyncEntity":
        """Accepts serialized data from the local entity. This needs to be
        implemented on a per remote entity basis."""
        raise NotImplementedError()
