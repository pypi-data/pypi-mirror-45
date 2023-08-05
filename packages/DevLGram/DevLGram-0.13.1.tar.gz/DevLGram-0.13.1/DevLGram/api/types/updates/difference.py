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


class Difference(Object):
    """Attributes:
        ID: ``0x00f49ca0``

    Args:
        new_messages: List of either :obj:`MessageEmpty <DevLGram.api.types.MessageEmpty>`, :obj:`Message <DevLGram.api.types.Message>` or :obj:`MessageService <DevLGram.api.types.MessageService>`
        new_encrypted_messages: List of either :obj:`EncryptedMessage <DevLGram.api.types.EncryptedMessage>` or :obj:`EncryptedMessageService <DevLGram.api.types.EncryptedMessageService>`
        other_updates: List of either :obj:`UpdateNewMessage <DevLGram.api.types.UpdateNewMessage>`, :obj:`UpdateMessageID <DevLGram.api.types.UpdateMessageID>`, :obj:`UpdateDeleteMessages <DevLGram.api.types.UpdateDeleteMessages>`, :obj:`UpdateUserTyping <DevLGram.api.types.UpdateUserTyping>`, :obj:`UpdateChatUserTyping <DevLGram.api.types.UpdateChatUserTyping>`, :obj:`UpdateChatParticipants <DevLGram.api.types.UpdateChatParticipants>`, :obj:`UpdateUserStatus <DevLGram.api.types.UpdateUserStatus>`, :obj:`UpdateUserName <DevLGram.api.types.UpdateUserName>`, :obj:`UpdateUserPhoto <DevLGram.api.types.UpdateUserPhoto>`, :obj:`UpdateContactLink <DevLGram.api.types.UpdateContactLink>`, :obj:`UpdateNewEncryptedMessage <DevLGram.api.types.UpdateNewEncryptedMessage>`, :obj:`UpdateEncryptedChatTyping <DevLGram.api.types.UpdateEncryptedChatTyping>`, :obj:`UpdateEncryption <DevLGram.api.types.UpdateEncryption>`, :obj:`UpdateEncryptedMessagesRead <DevLGram.api.types.UpdateEncryptedMessagesRead>`, :obj:`UpdateChatParticipantAdd <DevLGram.api.types.UpdateChatParticipantAdd>`, :obj:`UpdateChatParticipantDelete <DevLGram.api.types.UpdateChatParticipantDelete>`, :obj:`UpdateDcOptions <DevLGram.api.types.UpdateDcOptions>`, :obj:`UpdateUserBlocked <DevLGram.api.types.UpdateUserBlocked>`, :obj:`UpdateNotifySettings <DevLGram.api.types.UpdateNotifySettings>`, :obj:`UpdateServiceNotification <DevLGram.api.types.UpdateServiceNotification>`, :obj:`UpdatePrivacy <DevLGram.api.types.UpdatePrivacy>`, :obj:`UpdateUserPhone <DevLGram.api.types.UpdateUserPhone>`, :obj:`UpdateReadHistoryInbox <DevLGram.api.types.UpdateReadHistoryInbox>`, :obj:`UpdateReadHistoryOutbox <DevLGram.api.types.UpdateReadHistoryOutbox>`, :obj:`UpdateWebPage <DevLGram.api.types.UpdateWebPage>`, :obj:`UpdateReadMessagesContents <DevLGram.api.types.UpdateReadMessagesContents>`, :obj:`UpdateChannelTooLong <DevLGram.api.types.UpdateChannelTooLong>`, :obj:`UpdateChannel <DevLGram.api.types.UpdateChannel>`, :obj:`UpdateNewChannelMessage <DevLGram.api.types.UpdateNewChannelMessage>`, :obj:`UpdateReadChannelInbox <DevLGram.api.types.UpdateReadChannelInbox>`, :obj:`UpdateDeleteChannelMessages <DevLGram.api.types.UpdateDeleteChannelMessages>`, :obj:`UpdateChannelMessageViews <DevLGram.api.types.UpdateChannelMessageViews>`, :obj:`UpdateChatParticipantAdmin <DevLGram.api.types.UpdateChatParticipantAdmin>`, :obj:`UpdateNewStickerSet <DevLGram.api.types.UpdateNewStickerSet>`, :obj:`UpdateStickerSetsOrder <DevLGram.api.types.UpdateStickerSetsOrder>`, :obj:`UpdateStickerSets <DevLGram.api.types.UpdateStickerSets>`, :obj:`UpdateSavedGifs <DevLGram.api.types.UpdateSavedGifs>`, :obj:`UpdateBotInlineQuery <DevLGram.api.types.UpdateBotInlineQuery>`, :obj:`UpdateBotInlineSend <DevLGram.api.types.UpdateBotInlineSend>`, :obj:`UpdateEditChannelMessage <DevLGram.api.types.UpdateEditChannelMessage>`, :obj:`UpdateChannelPinnedMessage <DevLGram.api.types.UpdateChannelPinnedMessage>`, :obj:`UpdateBotCallbackQuery <DevLGram.api.types.UpdateBotCallbackQuery>`, :obj:`UpdateEditMessage <DevLGram.api.types.UpdateEditMessage>`, :obj:`UpdateInlineBotCallbackQuery <DevLGram.api.types.UpdateInlineBotCallbackQuery>`, :obj:`UpdateReadChannelOutbox <DevLGram.api.types.UpdateReadChannelOutbox>`, :obj:`UpdateDraftMessage <DevLGram.api.types.UpdateDraftMessage>`, :obj:`UpdateReadFeaturedStickers <DevLGram.api.types.UpdateReadFeaturedStickers>`, :obj:`UpdateRecentStickers <DevLGram.api.types.UpdateRecentStickers>`, :obj:`UpdateConfig <DevLGram.api.types.UpdateConfig>`, :obj:`UpdatePtsChanged <DevLGram.api.types.UpdatePtsChanged>`, :obj:`UpdateChannelWebPage <DevLGram.api.types.UpdateChannelWebPage>`, :obj:`UpdateDialogPinned <DevLGram.api.types.UpdateDialogPinned>`, :obj:`UpdatePinnedDialogs <DevLGram.api.types.UpdatePinnedDialogs>`, :obj:`UpdateBotWebhookJSON <DevLGram.api.types.UpdateBotWebhookJSON>`, :obj:`UpdateBotWebhookJSONQuery <DevLGram.api.types.UpdateBotWebhookJSONQuery>`, :obj:`UpdateBotShippingQuery <DevLGram.api.types.UpdateBotShippingQuery>`, :obj:`UpdateBotPrecheckoutQuery <DevLGram.api.types.UpdateBotPrecheckoutQuery>`, :obj:`UpdatePhoneCall <DevLGram.api.types.UpdatePhoneCall>`, :obj:`UpdateLangPackTooLong <DevLGram.api.types.UpdateLangPackTooLong>`, :obj:`UpdateLangPack <DevLGram.api.types.UpdateLangPack>`, :obj:`UpdateFavedStickers <DevLGram.api.types.UpdateFavedStickers>`, :obj:`UpdateChannelReadMessagesContents <DevLGram.api.types.UpdateChannelReadMessagesContents>`, :obj:`UpdateContactsReset <DevLGram.api.types.UpdateContactsReset>`, :obj:`UpdateChannelAvailableMessages <DevLGram.api.types.UpdateChannelAvailableMessages>`, :obj:`UpdateDialogUnreadMark <DevLGram.api.types.UpdateDialogUnreadMark>`, :obj:`UpdateUserPinnedMessage <DevLGram.api.types.UpdateUserPinnedMessage>`, :obj:`UpdateChatPinnedMessage <DevLGram.api.types.UpdateChatPinnedMessage>`, :obj:`UpdateMessagePoll <DevLGram.api.types.UpdateMessagePoll>` or :obj:`UpdateChatDefaultBannedRights <DevLGram.api.types.UpdateChatDefaultBannedRights>`
        chats: List of either :obj:`ChatEmpty <DevLGram.api.types.ChatEmpty>`, :obj:`Chat <DevLGram.api.types.Chat>`, :obj:`ChatForbidden <DevLGram.api.types.ChatForbidden>`, :obj:`Channel <DevLGram.api.types.Channel>` or :obj:`ChannelForbidden <DevLGram.api.types.ChannelForbidden>`
        users: List of either :obj:`UserEmpty <DevLGram.api.types.UserEmpty>` or :obj:`User <DevLGram.api.types.User>`
        state: :obj:`updates.State <DevLGram.api.types.updates.State>`

    See Also:
        This object can be returned by :obj:`updates.GetDifference <DevLGram.api.functions.updates.GetDifference>`.
    """

    __slots__ = ["new_messages", "new_encrypted_messages", "other_updates", "chats", "users", "state"]

    ID = 0x00f49ca0
    QUALNAME = "updates.Difference"

    def __init__(self, *, new_messages: list, new_encrypted_messages: list, other_updates: list, chats: list, users: list, state):
        self.new_messages = new_messages  # Vector<Message>
        self.new_encrypted_messages = new_encrypted_messages  # Vector<EncryptedMessage>
        self.other_updates = other_updates  # Vector<Update>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>
        self.state = state  # updates.State

    @staticmethod
    def read(b: BytesIO, *args) -> "Difference":
        # No flags
        
        new_messages = Object.read(b)
        
        new_encrypted_messages = Object.read(b)
        
        other_updates = Object.read(b)
        
        chats = Object.read(b)
        
        users = Object.read(b)
        
        state = Object.read(b)
        
        return Difference(new_messages=new_messages, new_encrypted_messages=new_encrypted_messages, other_updates=other_updates, chats=chats, users=users, state=state)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.new_messages))
        
        b.write(Vector(self.new_encrypted_messages))
        
        b.write(Vector(self.other_updates))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        b.write(self.state.write())
        
        return b.getvalue()
