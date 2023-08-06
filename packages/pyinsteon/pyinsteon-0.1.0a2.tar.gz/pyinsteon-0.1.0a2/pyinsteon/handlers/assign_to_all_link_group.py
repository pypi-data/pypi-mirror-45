"""Assign a device to an all link group."""
from ..topics import ASSIGN_TO_ALL_LINK_GROUP
from ..constants import AllLinkMode, ResponseStatus
from .direct_command import DirectCommandHandlerBase
from .. import pub
from ..address import Address


class AssignToAllLinkGroupCommand(DirectCommandHandlerBase):
    """Assign to All-Link Group command handler."""

    def __init__(self, address: Address):
        """Init the AssignToAllLinkGroupCommand class."""
        super().__init__(address, ASSIGN_TO_ALL_LINK_GROUP)
        self._id_response_topic = '{}.{}.broadcast'.format(
            self._address.id, ASSIGN_TO_ALL_LINK_GROUP)

    #pylint: disable=arguments-differ
    async def async_send(self, group: int, mode: AllLinkMode = AllLinkMode.RESPONDER):
        """Send the device ID request asyncronously."""
        pub.subscribe(self.receive_id, self._id_response_topic)
        return await super().async_send(group=group, mode=mode)

    def receive_id(self, cmd2, target, user_data):
        """Receive the device ID information."""
        if not self.response_lock.locked():
            # Assign to All-Link Group not called therefore
            # this is not meant for us
            return

        cat = target.high
        subcat = target.middle
        firmware = target.low
        for subscriber in self._subscribers:
            subscriber(self._address, cat, subcat, firmware)
        pub.unsubscribe(self.receive_id, self._id_response_topic)
        if self.response_lock.locked():
            self.message_response.put_nowait(ResponseStatus.SUCCESS)
