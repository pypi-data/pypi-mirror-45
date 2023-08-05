# DevLGram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/devladityanugraha>
#
# This file is part of DevLGram.
#
# DevLGram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DevLGram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with DevLGram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from DevLGram.api.core import *


class UpdatesTooLong(Object):
    """Attributes:
        ID: ``0xe317af7e``

    No parameters required.

    See Also:
        This object can be returned by :obj:`account.GetNotifyExceptions <DevLGram.api.functions.account.GetNotifyExceptions>`, :obj:`messages.SendMessage <DevLGram.api.functions.messages.SendMessage>`, :obj:`messages.SendMedia <DevLGram.api.functions.messages.SendMedia>`, :obj:`messages.ForwardMessages <DevLGram.api.functions.messages.ForwardMessages>`, :obj:`messages.EditChatTitle <DevLGram.api.functions.messages.EditChatTitle>`, :obj:`messages.EditChatPhoto <DevLGram.api.functions.messages.EditChatPhoto>`, :obj:`messages.AddChatUser <DevLGram.api.functions.messages.AddChatUser>`, :obj:`messages.DeleteChatUser <DevLGram.api.functions.messages.DeleteChatUser>`, :obj:`messages.CreateChat <DevLGram.api.functions.messages.CreateChat>`, :obj:`messages.ImportChatInvite <DevLGram.api.functions.messages.ImportChatInvite>`, :obj:`messages.StartBot <DevLGram.api.functions.messages.StartBot>`, :obj:`messages.MigrateChat <DevLGram.api.functions.messages.MigrateChat>`, :obj:`messages.SendInlineBotResult <DevLGram.api.functions.messages.SendInlineBotResult>`, :obj:`messages.EditMessage <DevLGram.api.functions.messages.EditMessage>`, :obj:`messages.GetAllDrafts <DevLGram.api.functions.messages.GetAllDrafts>`, :obj:`messages.SetGameScore <DevLGram.api.functions.messages.SetGameScore>`, :obj:`messages.SendScreenshotNotification <DevLGram.api.functions.messages.SendScreenshotNotification>`, :obj:`messages.SendMultiMedia <DevLGram.api.functions.messages.SendMultiMedia>`, :obj:`messages.UpdatePinnedMessage <DevLGram.api.functions.messages.UpdatePinnedMessage>`, :obj:`messages.SendVote <DevLGram.api.functions.messages.SendVote>`, :obj:`messages.GetPollResults <DevLGram.api.functions.messages.GetPollResults>`, :obj:`messages.EditChatDefaultBannedRights <DevLGram.api.functions.messages.EditChatDefaultBannedRights>`, :obj:`help.GetAppChangelog <DevLGram.api.functions.help.GetAppChangelog>`, :obj:`channels.CreateChannel <DevLGram.api.functions.channels.CreateChannel>`, :obj:`channels.EditAdmin <DevLGram.api.functions.channels.EditAdmin>`, :obj:`channels.EditTitle <DevLGram.api.functions.channels.EditTitle>`, :obj:`channels.EditPhoto <DevLGram.api.functions.channels.EditPhoto>`, :obj:`channels.JoinChannel <DevLGram.api.functions.channels.JoinChannel>`, :obj:`channels.LeaveChannel <DevLGram.api.functions.channels.LeaveChannel>`, :obj:`channels.InviteToChannel <DevLGram.api.functions.channels.InviteToChannel>`, :obj:`channels.DeleteChannel <DevLGram.api.functions.channels.DeleteChannel>`, :obj:`channels.ToggleSignatures <DevLGram.api.functions.channels.ToggleSignatures>`, :obj:`channels.EditBanned <DevLGram.api.functions.channels.EditBanned>`, :obj:`channels.TogglePreHistoryHidden <DevLGram.api.functions.channels.TogglePreHistoryHidden>`, :obj:`phone.DiscardCall <DevLGram.api.functions.phone.DiscardCall>` and :obj:`phone.SetCallRating <DevLGram.api.functions.phone.SetCallRating>`.
    """

    __slots__ = []

    ID = 0xe317af7e
    QUALNAME = "UpdatesTooLong"

    def __init__(self, ):
        pass

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdatesTooLong":
        # No flags
        
        return UpdatesTooLong()

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
