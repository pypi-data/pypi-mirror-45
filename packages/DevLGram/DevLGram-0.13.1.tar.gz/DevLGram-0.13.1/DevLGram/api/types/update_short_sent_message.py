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


class UpdateShortSentMessage(Object):
    """Attributes:
        ID: ``0x11f1331c``

    Args:
        id: ``int`` ``32-bit``
        pts: ``int`` ``32-bit``
        pts_count: ``int`` ``32-bit``
        date: ``int`` ``32-bit``
        out (optional): ``bool``
        media (optional): Either :obj:`MessageMediaEmpty <DevLGram.api.types.MessageMediaEmpty>`, :obj:`MessageMediaPhoto <DevLGram.api.types.MessageMediaPhoto>`, :obj:`MessageMediaGeo <DevLGram.api.types.MessageMediaGeo>`, :obj:`MessageMediaContact <DevLGram.api.types.MessageMediaContact>`, :obj:`MessageMediaUnsupported <DevLGram.api.types.MessageMediaUnsupported>`, :obj:`MessageMediaDocument <DevLGram.api.types.MessageMediaDocument>`, :obj:`MessageMediaWebPage <DevLGram.api.types.MessageMediaWebPage>`, :obj:`MessageMediaVenue <DevLGram.api.types.MessageMediaVenue>`, :obj:`MessageMediaGame <DevLGram.api.types.MessageMediaGame>`, :obj:`MessageMediaInvoice <DevLGram.api.types.MessageMediaInvoice>`, :obj:`MessageMediaGeoLive <DevLGram.api.types.MessageMediaGeoLive>` or :obj:`MessageMediaPoll <DevLGram.api.types.MessageMediaPoll>`
        entities (optional): List of either :obj:`MessageEntityUnknown <DevLGram.api.types.MessageEntityUnknown>`, :obj:`MessageEntityMention <DevLGram.api.types.MessageEntityMention>`, :obj:`MessageEntityHashtag <DevLGram.api.types.MessageEntityHashtag>`, :obj:`MessageEntityBotCommand <DevLGram.api.types.MessageEntityBotCommand>`, :obj:`MessageEntityUrl <DevLGram.api.types.MessageEntityUrl>`, :obj:`MessageEntityEmail <DevLGram.api.types.MessageEntityEmail>`, :obj:`MessageEntityBold <DevLGram.api.types.MessageEntityBold>`, :obj:`MessageEntityItalic <DevLGram.api.types.MessageEntityItalic>`, :obj:`MessageEntityCode <DevLGram.api.types.MessageEntityCode>`, :obj:`MessageEntityPre <DevLGram.api.types.MessageEntityPre>`, :obj:`MessageEntityTextUrl <DevLGram.api.types.MessageEntityTextUrl>`, :obj:`MessageEntityMentionName <DevLGram.api.types.MessageEntityMentionName>`, :obj:`InputMessageEntityMentionName <DevLGram.api.types.InputMessageEntityMentionName>`, :obj:`MessageEntityPhone <DevLGram.api.types.MessageEntityPhone>` or :obj:`MessageEntityCashtag <DevLGram.api.types.MessageEntityCashtag>`

    See Also:
        This object can be returned by :obj:`account.GetNotifyExceptions <DevLGram.api.functions.account.GetNotifyExceptions>`, :obj:`messages.SendMessage <DevLGram.api.functions.messages.SendMessage>`, :obj:`messages.SendMedia <DevLGram.api.functions.messages.SendMedia>`, :obj:`messages.ForwardMessages <DevLGram.api.functions.messages.ForwardMessages>`, :obj:`messages.EditChatTitle <DevLGram.api.functions.messages.EditChatTitle>`, :obj:`messages.EditChatPhoto <DevLGram.api.functions.messages.EditChatPhoto>`, :obj:`messages.AddChatUser <DevLGram.api.functions.messages.AddChatUser>`, :obj:`messages.DeleteChatUser <DevLGram.api.functions.messages.DeleteChatUser>`, :obj:`messages.CreateChat <DevLGram.api.functions.messages.CreateChat>`, :obj:`messages.ImportChatInvite <DevLGram.api.functions.messages.ImportChatInvite>`, :obj:`messages.StartBot <DevLGram.api.functions.messages.StartBot>`, :obj:`messages.MigrateChat <DevLGram.api.functions.messages.MigrateChat>`, :obj:`messages.SendInlineBotResult <DevLGram.api.functions.messages.SendInlineBotResult>`, :obj:`messages.EditMessage <DevLGram.api.functions.messages.EditMessage>`, :obj:`messages.GetAllDrafts <DevLGram.api.functions.messages.GetAllDrafts>`, :obj:`messages.SetGameScore <DevLGram.api.functions.messages.SetGameScore>`, :obj:`messages.SendScreenshotNotification <DevLGram.api.functions.messages.SendScreenshotNotification>`, :obj:`messages.SendMultiMedia <DevLGram.api.functions.messages.SendMultiMedia>`, :obj:`messages.UpdatePinnedMessage <DevLGram.api.functions.messages.UpdatePinnedMessage>`, :obj:`messages.SendVote <DevLGram.api.functions.messages.SendVote>`, :obj:`messages.GetPollResults <DevLGram.api.functions.messages.GetPollResults>`, :obj:`messages.EditChatDefaultBannedRights <DevLGram.api.functions.messages.EditChatDefaultBannedRights>`, :obj:`help.GetAppChangelog <DevLGram.api.functions.help.GetAppChangelog>`, :obj:`channels.CreateChannel <DevLGram.api.functions.channels.CreateChannel>`, :obj:`channels.EditAdmin <DevLGram.api.functions.channels.EditAdmin>`, :obj:`channels.EditTitle <DevLGram.api.functions.channels.EditTitle>`, :obj:`channels.EditPhoto <DevLGram.api.functions.channels.EditPhoto>`, :obj:`channels.JoinChannel <DevLGram.api.functions.channels.JoinChannel>`, :obj:`channels.LeaveChannel <DevLGram.api.functions.channels.LeaveChannel>`, :obj:`channels.InviteToChannel <DevLGram.api.functions.channels.InviteToChannel>`, :obj:`channels.DeleteChannel <DevLGram.api.functions.channels.DeleteChannel>`, :obj:`channels.ToggleSignatures <DevLGram.api.functions.channels.ToggleSignatures>`, :obj:`channels.EditBanned <DevLGram.api.functions.channels.EditBanned>`, :obj:`channels.TogglePreHistoryHidden <DevLGram.api.functions.channels.TogglePreHistoryHidden>`, :obj:`phone.DiscardCall <DevLGram.api.functions.phone.DiscardCall>` and :obj:`phone.SetCallRating <DevLGram.api.functions.phone.SetCallRating>`.
    """

    __slots__ = ["id", "pts", "pts_count", "date", "out", "media", "entities"]

    ID = 0x11f1331c
    QUALNAME = "UpdateShortSentMessage"

    def __init__(self, *, id: int, pts: int, pts_count: int, date: int, out: bool = None, media=None, entities: list = None):
        self.out = out  # flags.1?true
        self.id = id  # int
        self.pts = pts  # int
        self.pts_count = pts_count  # int
        self.date = date  # int
        self.media = media  # flags.9?MessageMedia
        self.entities = entities  # flags.7?Vector<MessageEntity>

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateShortSentMessage":
        flags = Int.read(b)
        
        out = True if flags & (1 << 1) else False
        id = Int.read(b)
        
        pts = Int.read(b)
        
        pts_count = Int.read(b)
        
        date = Int.read(b)
        
        media = Object.read(b) if flags & (1 << 9) else None
        
        entities = Object.read(b) if flags & (1 << 7) else []
        
        return UpdateShortSentMessage(id=id, pts=pts, pts_count=pts_count, date=date, out=out, media=media, entities=entities)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.out is not None else 0
        flags |= (1 << 9) if self.media is not None else 0
        flags |= (1 << 7) if self.entities is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.id))
        
        b.write(Int(self.pts))
        
        b.write(Int(self.pts_count))
        
        b.write(Int(self.date))
        
        if self.media is not None:
            b.write(self.media.write())
        
        if self.entities is not None:
            b.write(Vector(self.entities))
        
        return b.getvalue()
