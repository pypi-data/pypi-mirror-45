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

from typing import Union, List

import DevLGram
from DevLGram.api import functions, types
from DevLGram.client.ext import BaseClient


class SendPoll(BaseClient):
    def send_poll(
        self,
        chat_id: Union[int, str],
        question: str,
        options: List[str],
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_markup: Union[
            "DevLGram.InlineKeyboardMarkup",
            "DevLGram.ReplyKeyboardMarkup",
            "DevLGram.ReplyKeyboardRemove",
            "DevLGram.ForceReply"
        ] = None
    ) -> "DevLGram.Message":
        """Use this method to send a new poll.

        Args:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            question (``str``):
                The poll question, as string.

            options (List of ``str``):
                The poll options, as list of strings (2 to 10 options are allowed).

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_markup (:obj:`InlineKeyboardMarkup` | :obj:`ReplyKeyboardMarkup` | :obj:`ReplyKeyboardRemove` | :obj:`ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent :obj:`Message <DevLGram.Message>` is returned.

        Raises:
            :class:`RPCError <DevLGram.RPCError>` in case of a Telegram RPC error.
        """
        r = self.send(
            functions.messages.SendMedia(
                peer=self.resolve_peer(chat_id),
                media=types.InputMediaPoll(
                    poll=types.Poll(
                        id=0,
                        question=question,
                        answers=[
                            types.PollAnswer(text=o, option=bytes([i]))
                            for i, o in enumerate(options)
                        ]
                    )
                ),
                message="",
                silent=disable_notification or None,
                reply_to_msg_id=reply_to_message_id,
                random_id=self.rnd_id(),
                reply_markup=reply_markup.write() if reply_markup else None
            )
        )

        for i in r.updates:
            if isinstance(i, (types.UpdateNewMessage, types.UpdateNewChannelMessage)):
                return DevLGram.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats}
                )
