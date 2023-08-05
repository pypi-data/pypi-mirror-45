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


class UpdateShort(Object):
    """Attributes:
        ID: ``0x78d4dec1``

    Args:
        update: Either :obj:`UpdateNewMessage <DevLGram.api.types.UpdateNewMessage>`, :obj:`UpdateMessageID <DevLGram.api.types.UpdateMessageID>`, :obj:`UpdateDeleteMessages <DevLGram.api.types.UpdateDeleteMessages>`, :obj:`UpdateUserTyping <DevLGram.api.types.UpdateUserTyping>`, :obj:`UpdateChatUserTyping <DevLGram.api.types.UpdateChatUserTyping>`, :obj:`UpdateChatParticipants <DevLGram.api.types.UpdateChatParticipants>`, :obj:`UpdateUserStatus <DevLGram.api.types.UpdateUserStatus>`, :obj:`UpdateUserName <DevLGram.api.types.UpdateUserName>`, :obj:`UpdateUserPhoto <DevLGram.api.types.UpdateUserPhoto>`, :obj:`UpdateContactLink <DevLGram.api.types.UpdateContactLink>`, :obj:`UpdateNewEncryptedMessage <DevLGram.api.types.UpdateNewEncryptedMessage>`, :obj:`UpdateEncryptedChatTyping <DevLGram.api.types.UpdateEncryptedChatTyping>`, :obj:`UpdateEncryption <DevLGram.api.types.UpdateEncryption>`, :obj:`UpdateEncryptedMessagesRead <DevLGram.api.types.UpdateEncryptedMessagesRead>`, :obj:`UpdateChatParticipantAdd <DevLGram.api.types.UpdateChatParticipantAdd>`, :obj:`UpdateChatParticipantDelete <DevLGram.api.types.UpdateChatParticipantDelete>`, :obj:`UpdateDcOptions <DevLGram.api.types.UpdateDcOptions>`, :obj:`UpdateUserBlocked <DevLGram.api.types.UpdateUserBlocked>`, :obj:`UpdateNotifySettings <DevLGram.api.types.UpdateNotifySettings>`, :obj:`UpdateServiceNotification <DevLGram.api.types.UpdateServiceNotification>`, :obj:`UpdatePrivacy <DevLGram.api.types.UpdatePrivacy>`, :obj:`UpdateUserPhone <DevLGram.api.types.UpdateUserPhone>`, :obj:`UpdateReadHistoryInbox <DevLGram.api.types.UpdateReadHistoryInbox>`, :obj:`UpdateReadHistoryOutbox <DevLGram.api.types.UpdateReadHistoryOutbox>`, :obj:`UpdateWebPage <DevLGram.api.types.UpdateWebPage>`, :obj:`UpdateReadMessagesContents <DevLGram.api.types.UpdateReadMessagesContents>`, :obj:`UpdateChannelTooLong <DevLGram.api.types.UpdateChannelTooLong>`, :obj:`UpdateChannel <DevLGram.api.types.UpdateChannel>`, :obj:`UpdateNewChannelMessage <DevLGram.api.types.UpdateNewChannelMessage>`, :obj:`UpdateReadChannelInbox <DevLGram.api.types.UpdateReadChannelInbox>`, :obj:`UpdateDeleteChannelMessages <DevLGram.api.types.UpdateDeleteChannelMessages>`, :obj:`UpdateChannelMessageViews <DevLGram.api.types.UpdateChannelMessageViews>`, :obj:`UpdateChatParticipantAdmin <DevLGram.api.types.UpdateChatParticipantAdmin>`, :obj:`UpdateNewStickerSet <DevLGram.api.types.UpdateNewStickerSet>`, :obj:`UpdateStickerSetsOrder <DevLGram.api.types.UpdateStickerSetsOrder>`, :obj:`UpdateStickerSets <DevLGram.api.types.UpdateStickerSets>`, :obj:`UpdateSavedGifs <DevLGram.api.types.UpdateSavedGifs>`, :obj:`UpdateBotInlineQuery <DevLGram.api.types.UpdateBotInlineQuery>`, :obj:`UpdateBotInlineSend <DevLGram.api.types.UpdateBotInlineSend>`, :obj:`UpdateEditChannelMessage <DevLGram.api.types.UpdateEditChannelMessage>`, :obj:`UpdateChannelPinnedMessage <DevLGram.api.types.UpdateChannelPinnedMessage>`, :obj:`UpdateBotCallbackQuery <DevLGram.api.types.UpdateBotCallbackQuery>`, :obj:`UpdateEditMessage <DevLGram.api.types.UpdateEditMessage>`, :obj:`UpdateInlineBotCallbackQuery <DevLGram.api.types.UpdateInlineBotCallbackQuery>`, :obj:`UpdateReadChannelOutbox <DevLGram.api.types.UpdateReadChannelOutbox>`, :obj:`UpdateDraftMessage <DevLGram.api.types.UpdateDraftMessage>`, :obj:`UpdateReadFeaturedStickers <DevLGram.api.types.UpdateReadFeaturedStickers>`, :obj:`UpdateRecentStickers <DevLGram.api.types.UpdateRecentStickers>`, :obj:`UpdateConfig <DevLGram.api.types.UpdateConfig>`, :obj:`UpdatePtsChanged <DevLGram.api.types.UpdatePtsChanged>`, :obj:`UpdateChannelWebPage <DevLGram.api.types.UpdateChannelWebPage>`, :obj:`UpdateDialogPinned <DevLGram.api.types.UpdateDialogPinned>`, :obj:`UpdatePinnedDialogs <DevLGram.api.types.UpdatePinnedDialogs>`, :obj:`UpdateBotWebhookJSON <DevLGram.api.types.UpdateBotWebhookJSON>`, :obj:`UpdateBotWebhookJSONQuery <DevLGram.api.types.UpdateBotWebhookJSONQuery>`, :obj:`UpdateBotShippingQuery <DevLGram.api.types.UpdateBotShippingQuery>`, :obj:`UpdateBotPrecheckoutQuery <DevLGram.api.types.UpdateBotPrecheckoutQuery>`, :obj:`UpdatePhoneCall <DevLGram.api.types.UpdatePhoneCall>`, :obj:`UpdateLangPackTooLong <DevLGram.api.types.UpdateLangPackTooLong>`, :obj:`UpdateLangPack <DevLGram.api.types.UpdateLangPack>`, :obj:`UpdateFavedStickers <DevLGram.api.types.UpdateFavedStickers>`, :obj:`UpdateChannelReadMessagesContents <DevLGram.api.types.UpdateChannelReadMessagesContents>`, :obj:`UpdateContactsReset <DevLGram.api.types.UpdateContactsReset>`, :obj:`UpdateChannelAvailableMessages <DevLGram.api.types.UpdateChannelAvailableMessages>`, :obj:`UpdateDialogUnreadMark <DevLGram.api.types.UpdateDialogUnreadMark>`, :obj:`UpdateUserPinnedMessage <DevLGram.api.types.UpdateUserPinnedMessage>`, :obj:`UpdateChatPinnedMessage <DevLGram.api.types.UpdateChatPinnedMessage>`, :obj:`UpdateMessagePoll <DevLGram.api.types.UpdateMessagePoll>` or :obj:`UpdateChatDefaultBannedRights <DevLGram.api.types.UpdateChatDefaultBannedRights>`
        date: ``int`` ``32-bit``

    See Also:
        This object can be returned by :obj:`account.GetNotifyExceptions <DevLGram.api.functions.account.GetNotifyExceptions>`, :obj:`messages.SendMessage <DevLGram.api.functions.messages.SendMessage>`, :obj:`messages.SendMedia <DevLGram.api.functions.messages.SendMedia>`, :obj:`messages.ForwardMessages <DevLGram.api.functions.messages.ForwardMessages>`, :obj:`messages.EditChatTitle <DevLGram.api.functions.messages.EditChatTitle>`, :obj:`messages.EditChatPhoto <DevLGram.api.functions.messages.EditChatPhoto>`, :obj:`messages.AddChatUser <DevLGram.api.functions.messages.AddChatUser>`, :obj:`messages.DeleteChatUser <DevLGram.api.functions.messages.DeleteChatUser>`, :obj:`messages.CreateChat <DevLGram.api.functions.messages.CreateChat>`, :obj:`messages.ImportChatInvite <DevLGram.api.functions.messages.ImportChatInvite>`, :obj:`messages.StartBot <DevLGram.api.functions.messages.StartBot>`, :obj:`messages.MigrateChat <DevLGram.api.functions.messages.MigrateChat>`, :obj:`messages.SendInlineBotResult <DevLGram.api.functions.messages.SendInlineBotResult>`, :obj:`messages.EditMessage <DevLGram.api.functions.messages.EditMessage>`, :obj:`messages.GetAllDrafts <DevLGram.api.functions.messages.GetAllDrafts>`, :obj:`messages.SetGameScore <DevLGram.api.functions.messages.SetGameScore>`, :obj:`messages.SendScreenshotNotification <DevLGram.api.functions.messages.SendScreenshotNotification>`, :obj:`messages.SendMultiMedia <DevLGram.api.functions.messages.SendMultiMedia>`, :obj:`messages.UpdatePinnedMessage <DevLGram.api.functions.messages.UpdatePinnedMessage>`, :obj:`messages.SendVote <DevLGram.api.functions.messages.SendVote>`, :obj:`messages.GetPollResults <DevLGram.api.functions.messages.GetPollResults>`, :obj:`messages.EditChatDefaultBannedRights <DevLGram.api.functions.messages.EditChatDefaultBannedRights>`, :obj:`help.GetAppChangelog <DevLGram.api.functions.help.GetAppChangelog>`, :obj:`channels.CreateChannel <DevLGram.api.functions.channels.CreateChannel>`, :obj:`channels.EditAdmin <DevLGram.api.functions.channels.EditAdmin>`, :obj:`channels.EditTitle <DevLGram.api.functions.channels.EditTitle>`, :obj:`channels.EditPhoto <DevLGram.api.functions.channels.EditPhoto>`, :obj:`channels.JoinChannel <DevLGram.api.functions.channels.JoinChannel>`, :obj:`channels.LeaveChannel <DevLGram.api.functions.channels.LeaveChannel>`, :obj:`channels.InviteToChannel <DevLGram.api.functions.channels.InviteToChannel>`, :obj:`channels.DeleteChannel <DevLGram.api.functions.channels.DeleteChannel>`, :obj:`channels.ToggleSignatures <DevLGram.api.functions.channels.ToggleSignatures>`, :obj:`channels.EditBanned <DevLGram.api.functions.channels.EditBanned>`, :obj:`channels.TogglePreHistoryHidden <DevLGram.api.functions.channels.TogglePreHistoryHidden>`, :obj:`phone.DiscardCall <DevLGram.api.functions.phone.DiscardCall>` and :obj:`phone.SetCallRating <DevLGram.api.functions.phone.SetCallRating>`.
    """

    __slots__ = ["update", "date"]

    ID = 0x78d4dec1
    QUALNAME = "UpdateShort"

    def __init__(self, *, update, date: int):
        self.update = update  # Update
        self.date = date  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateShort":
        # No flags
        
        update = Object.read(b)
        
        date = Int.read(b)
        
        return UpdateShort(update=update, date=date)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.update.write())
        
        b.write(Int(self.date))
        
        return b.getvalue()
