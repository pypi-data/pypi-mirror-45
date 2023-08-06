# pylint: disable=no-member

import struct
import sys
import os
import logging
import resource
import asyncio

from . import protocol_pb2 as spb2
from .protocol_pb2 import WrapperMessage as wm
from .config import Config


class Backend(asyncio.Protocol):
    """
    Creates new NetworkPlugin and connects the Spectrum2 NetworkPluginServer.
    @param host: Host where Spectrum2 NetworkPluginServer runs.
    @param port: Port.
    """

    def __init__(self, jid, config=None):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.jid = jid

        self.config = Config(config) if config else None

        self._ping_received = False
        self._data = bytes()
        self._init_res = 0

    def connection_made(self, transport):
        self.transport = transport
        self.logger.debug("Connection established")

    def connection_lost(self, exc):
        self.transport = None
        self.logger.debug("Connection lost")

    @property
    def connected(self):
        return self.transport is not None

    def data_received(self, data):
        self.handle_data_read(data)

    def data_send(self, data):
        header = struct.pack('!I', len(data))

        self.transport.write(header + data)

    def handle_message(self, user, legacy_name, message, nickname='', xhtml='',
                       timestamp=''):
        m = spb2.ConversationMessage()
        m.userName = user
        m.buddyName = legacy_name
        m.message = message
        m.nickname = nickname
        m.xhtml = xhtml
        m.timestamp = str(timestamp)

        self.send_wrapped(m.SerializeToString(),
                          wm.TYPE_CONV_MESSAGE)

    def handle_message_ack(self, user, legacy_name, mid):
        m = spb2.ConversationMessage()
        m.userName = user
        m.buddyName = legacy_name
        m.message = ''
        m.id = mid

        self.send_wrapped(m.SerializeToString(),
                          wm.TYPE_CONV_MESSAGE_ACK)

    def handle_attention(self, user, buddy_name, message):
        m = spb2.ConversationMessage()
        m.userName = user
        m.buddyName = buddy_name
        m.message = message

        self.send_wrapped(m.SerializeToString(),
                          wm.TYPE_ATTENTION)

    def handle_vcard(self, user, mid, legacy_name, full_name,
                     nickname, photo):
        vcard = spb2.VCard()
        vcard.userName = user
        vcard.buddyName = legacy_name
        vcard.id = mid
        vcard.fullname = full_name
        vcard.nickname = nickname
        vcard.photo = bytes(photo)

        self.send_wrapped(vcard.SerializeToString(),
                          wm.TYPE_VCARD)

    def handle_subject(self, user, legacy_name, message, nickname=''):
        m = spb2.ConversationMessage()
        m.userName = user
        m.buddyName = legacy_name
        m.message = message
        m.nickname = nickname

        self.send_wrapped(m.SerializeToString(),
                          wm.TYPE_ROOM_SUBJECT_CHANGED)

    def handle_buddy_changed(self, user, buddy_name, alias, groups, status,
                             status_message='', icon_hash='', blocked=False):
        buddy = spb2.Buddy()
        buddy.userName = user
        buddy.buddyName = buddy_name
        buddy.alias = alias
        buddy.group.extend(groups)
        buddy.status = status
        buddy.statusMessage = status_message
        buddy.iconHash = icon_hash
        buddy.blocked = blocked

        self.send_wrapped(buddy.SerializeToString(),
                          wm.TYPE_BUDDY_CHANGED)

    def handle_buddy_removed(self, user, buddy_name):
        buddy = spb2.Buddy()
        buddy.userName = user
        buddy.buddyName = buddy_name

        self.send_wrapped(buddy.SerializeToString(),
                          wm.TYPE_BUDDY_REMOVED)

    def handle_buddy_typing(self, user, buddy_name):
        buddy = spb2.Buddy()
        buddy.userName = user
        buddy.buddyName = buddy_name

        self.send_wrapped(buddy.SerializeToString(),
                          wm.TYPE_BUDDY_TYPING)

    def handle_buddy_typed(self, user, buddy_name):
        buddy = spb2.Buddy()
        buddy.userName = user
        buddy.buddyName = buddy_name

        self.send_wrapped(buddy.SerializeToString(),
                          wm.TYPE_BUDDY_TYPED)

    def handle_buddy_stopped_typing(self, user, buddy_name):
        buddy = spb2.Buddy()
        buddy.userName = user
        buddy.buddyName = buddy_name

        self.send_wrapped(buddy.SerializeToString(),
                          wm.TYPE_BUDDY_STOPPED_TYPING)

    def handle_authorization(self, user, buddy_name):
        buddy = spb2.Buddy()
        buddy.userName = user
        buddy.buddyName = buddy_name

        self.send_wrapped(buddy.SerializeToString(),
                          wm.TYPE_AUTH_REQUEST)

    def handle_connected(self, user):
        d = spb2.Connected()
        d.user = user

        self.send_wrapped(d.SerializeToString(),
                          wm.TYPE_CONNECTED)

    def handle_disconnected(self, user, error=0, message=''):
        d = spb2.Disconnected()
        d.user = user
        d.error = error
        d.message = message

        self.send_wrapped(d.SerializeToString(),
                          wm.TYPE_DISCONNECTED)

    def handle_participant_changed(self, user, nickname, room, flags, status,
                                   status_message='', newname='',
                                   icon_hash=''):
        d = spb2.Participant()
        d.userName = user
        d.nickname = nickname
        d.room = room
        d.flag = flags
        d.newname = newname
        d.iconHash = icon_hash
        d.status = status
        d.statusMessage = status_message

        self.send_wrapped(d.SerializeToString(),
                          wm.TYPE_PARTICIPANT_CHANGED)

    def handle_room_nickname_changed(self, user, r, nickname):
        room = spb2.Room()
        room.userName = user
        room.nickname = nickname
        room.room = r
        room.password = ''

        self.send_wrapped(room.SerializeToString(),
                          wm.TYPE_ROOM_NICKNAME_CHANGED)

    def handle_room_list(self, rooms):
        room_list = spb2.RoomList()

        for room in rooms:
            room_list.room.append(room[0])
            room_list.name.append(room[1])

        self.send_wrapped(room_list.SerializeToString(),
                          wm.TYPE_ROOM_LIST)

    def handle_ft_start(self, user, buddy_name, filename, size):
        room = spb2.File()
        room.userName = user
        room.buddyName = buddy_name
        room.fileName = filename
        room.size = size

        self.send_wrapped(room.SerializeToString(),
                          wm.TYPE_FT_START)

    def handle_ft_finish(self, user, buddy_name, filename, size, ft_id):
        room = spb2.File()
        room.userName = user
        room.buddyName = buddy_name
        room.fileName = filename
        room.size = size

        # Check later
        if ft_id != 0:
            room.ft_id = ft_id

        self.send_wrapped(room.SerializeToString(),
                          wm.TYPE_FT_FINISH)

    def handle_ft_data(self, ft_id, data):
        d = spb2.FileTransferData()
        d.ftID = ft_id
        d.data = bytes(data)

        self.send_wrapped(d.SerializeToString(),
                          wm.TYPE_FT_DATA)

    def handle_backend_config(self, data):
        """
        @param data: a dictionary, whose keys are sections and values are
                     a list of tuples of configuration key
                     and configuration value.
        """

        c = spb2.BackendConfig()
        config = []
        for section, rest in data.items():
            config.append('[%s]' % section)
            for key, value in rest:
                config.append('%s = %s' % (key, value))

        c.config = '\n'.join(config)

        self.send_wrapped(c.SerializeToString(),
                          wm.TYPE_BACKEND_CONFIG)

    def handle_query(self, command):
        c = spb2.BackendConfig()
        c.config = command

        self.send_wrapped(c.SerializeToString(),
                          wm.TYPE_QUERY)

    def handle_login_payload(self, data):
        payload = spb2.Login()
        payload.ParseFromString(data)

        self.handle_login_request(payload.user,
                                  payload.legacyName,
                                  payload.password,
                                  payload.extraFields)

    def handle_logout_payload(self, data):
        payload = spb2.Logout()
        payload.ParseFromString(data)

        self.handle_logout_request(payload.user,
                                   payload.legacyName)

    def handle_status_changed_payload(self, data):
        payload = spb2.Status()
        payload.ParseFromString(data)

        self.handle_status_change_request(payload.userName,
                                          payload.status,
                                          payload.statusMessage)

    def handle_conv_message_payload(self, data):
        payload = spb2.ConversationMessage()
        payload.ParseFromString(data)

        self.handle_message_send_request(payload.userName,
                                         payload.buddyName,
                                         payload.message,
                                         payload.xhtml,
                                         payload.id)

    def handle_conv_message_ack_payload(self, data):
        payload = spb2.ConversationMessage()
        payload.ParseFromString(data)

        self.handle_message_ack_request(payload.userName,
                                        payload.buddyName,
                                        payload.id)

    def handle_attention_payload(self, data):
        payload = spb2.ConversationMessage()
        payload.ParseFromString(data)

        self.handle_attention_request(payload.userName,
                                      payload.buddyName,
                                      payload.message)

    def handle_ft_start_payload(self, data):
        payload = spb2.File()
        payload.ParseFromString(data)

        self.handle_ft_start_request(payload.userName,
                                     payload.buddyName,
                                     payload.fileName,
                                     payload.size,
                                     payload.ftId)

    def handle_ft_finish_payload(self, data):
        payload = spb2.File()
        payload.ParseFromString(data)

        self.handle_ft_finish_request(payload.userName,
                                      payload.buddyName,
                                      payload.fileName,
                                      payload.size,
                                      payload.ftId)

    def handle_ft_pause_payload(self, data):
        payload = spb2.FileTransferData()
        payload.ParseFromString(data)

        self.handle_ft_pause_request(payload.ftId)

    def handle_ft_continue_payload(self, data):
        payload = spb2.FileTransferData()
        payload.ParseFromString(data)

        self.handle_ft_continue_request(payload.ftId)

    def handle_join_room_payload(self, data):
        payload = spb2.Room()
        payload.ParseFromString(data)

        self.handle_join_room_request(payload.userName,
                                      payload.room,
                                      payload.nickname,
                                      payload.password)

    def handle_leave_room_payload(self, data):
        payload = spb2.Room()
        payload.ParseFromString(data)

        self.handle_leave_room_request(payload.userName,
                                       payload.room)

    def handle_vcard_payload(self, data):
        payload = spb2.VCard()
        payload.ParseFromString(data)

        if payload.HasField('photo'):
            self.handle_vcard_updated_request(payload.userName,
                                              payload.photo,
                                              payload.nickname)
        elif payload.buddyName:
            self.handle_vcard_request(payload.userName, payload.buddyName,
                                      payload.id)

    def handle_buddy_changed_payload(self, data):
        payload = spb2.Buddy()
        payload.ParseFromString(data)

        if payload.HasField('blocked'):
            self.handle_buddy_block_toggled(payload.userName,
                                            payload.buddyName,
                                            payload.blocked)
        else:
            groups = [g for g in payload.group]
            self.handle_buddy_updated_request(payload.userName,
                                              payload.buddyName,
                                              payload.alias, groups)

    def handle_buddy_removed_payload(self, data):
        payload = spb2.Buddy()
        payload.ParseFromString(data)

        groups = [g for g in payload.group]
        self.handle_buddy_removed_request(payload.userName,
                                          payload.buddyName,
                                          groups)

    def handle_buddies_payload(self, data):
        payload = spb2.Buddies()
        payload.ParseFromString(data)

        self.handle_buddies(payload)

    def handle_chat_state_payload(self, data, message_type):
        payload = spb2.Buddy()
        payload.ParseFromString(data)

        if message_type == wm.TYPE_BUDDY_TYPING:
            self.handle_typing_request(payload.userName,
                                       payload.buddyName)
        elif message_type == wm.TYPE_BUDDY_TYPED:
            self.handle_typed_request(payload.userName,
                                      payload.buddyName)
        elif message_type == wm.TYPE_BUDDY_STOPPED_TYPING:
            self.handle_stopped_typing_request(payload.userName,
                                               payload.buddyName)

    def handle_data_read(self, data):
        self._data += data
        while self._data:
            expected_size = 0
            if len(self._data) >= 4:
                expected_size = struct.unpack('!I', self._data[0:4])[0]
                if len(self._data) - 4 < expected_size:
                    self.logger.debug('Data packet incomplete')
                    return
            else:
                self.logger.debug('Data packet incomplete')
                return

            packet = self._data[4:4+expected_size]
            wrapper = wm()
            try:
                wrapper.ParseFromString(packet)
            except Exception:
                self._data = self._data[expected_size+4:]
                self.logger.error('Parse from String exception. '
                                  'Skipping packet.')
                return

            self._data = self._data[4+expected_size:]

            if wrapper.type == wm.TYPE_PING:
                self.send_pong()
            elif wrapper.type == wm.TYPE_EXIT:
                self.handle_exit_request()
            elif wrapper.type == wm.TYPE_LOGIN:
                self.handle_login_payload(wrapper.payload)
            elif wrapper.type == wm.TYPE_LOGOUT:
                self.handle_logout_payload(wrapper.payload)
            elif wrapper.type == wm.TYPE_CONV_MESSAGE:
                self.handle_conv_message_payload(wrapper.payload)
            elif wrapper.type == wm.TYPE_JOIN_ROOM:
                self.handle_join_room_payload(wrapper.payload)
            elif wrapper.type == wm.TYPE_LEAVE_ROOM:
                self.handle_leave_room_payload(wrapper.payload)
            elif wrapper.type == wm.TYPE_VCARD:
                self.handle_vcard_payload(wrapper.payload)
            elif wrapper.type == wm.TYPE_BUDDY_CHANGED:
                self.handle_buddy_changed_payload(wrapper.payload)
            elif wrapper.type == wm.TYPE_BUDDY_REMOVED:
                self.handle_buddy_removed_payload(wrapper.payload)
            elif wrapper.type == wm.TYPE_STATUS_CHANGED:
                self.handle_status_changed_payload(wrapper.payload)
            elif wrapper.type == wm.TYPE_ATTENTION:
                self.handle_attention_payload(wrapper.payload)
            elif wrapper.type == wm.TYPE_FT_START:
                self.handle_ft_start_payload(wrapper.payload)
            elif wrapper.type == wm.TYPE_FT_FINISH:
                self.handle_ft_finish_payload(wrapper.payload)
            elif wrapper.type == wm.TYPE_FT_PAUSE:
                self.handle_ft_pause_payload(wrapper.payload)
            elif wrapper.type == wm.TYPE_FT_CONTINUE:
                self.handle_ft_continue_payload(wrapper.payload)
            elif wrapper.type == wm.TYPE_CONV_MESSAGE_ACK:
                self.handle_conv_message_ack_payload(wrapper.payload)
            elif wrapper.type == wm.TYPE_RAW_XML:
                self.handle_raw_xml_request(wrapper.payload)
            elif wrapper.type == wm.TYPE_BUDDIES:
                self.handle_buddies_payload(wrapper.payload)
            elif wrapper.type == wm.TYPE_BUDDY_TYPING:
                self.handle_chat_state_payload(wrapper.payload,
                                               wm.TYPE_BUDDY_TYPING)
            elif wrapper.type == wm.TYPE_BUDDY_TYPED:
                self.handle_chat_state_payload(wrapper.payload,
                                               wm.TYPE_BUDDY_TYPED)
            elif wrapper.type == wm.TYPE_BUDDY_STOPPED_TYPING:
                self.handle_chat_state_payload(wrapper.payload,
                                               wm.TYPE_BUDDY_STOPPED_TYPING)

    def send_wrapped(self, message, typ):
        wrap = wm()
        wrap.type = typ
        wrap.payload = bytes(message)

        self.data_send(wrap.SerializeToString())

    def send_pong(self):
        self._ping_received = True
        wrap = wm()
        wrap.type = wm.TYPE_PONG
        message = wrap.SerializeToString()
        self.data_send(message)
        self.send_memory_usage()

    def send_memory_usage(self):
        stats = spb2.Stats()

        stats.init_res = self._init_res
        res = 0
        shared = 0

        e_res, e_shared = self.handle_memory_usage()

        stats.res = res + e_res
        stats.shared = shared + e_shared
        stats.id = str(os.getpid())

        self.send_wrapped(stats.SerializeToString(),
                          wm.TYPE_STATS)

    def handle_login_request(self, user, legacy_name, password, extra):
        """
        Called when XMPP user wants to connect legacy network.
        You should connect him to legacy network and call handle_connected
        or handle_disconnected function later.

        @param user: XMPP JID of user for which this event occurs.
        @param legacy_name: Legacy network name of this user used for login.
        @param password: Legacy network password of this user.
        """

        raise NotImplementedError()

    def handle_buddies(self, buddies):
        pass

    def handle_logout_request(self, user, legacy_name):
        """
        Called when XMPP user wants to disconnect legacy network.
        You should disconnect him from legacy network.
        @param user: XMPP JID of user for which this event occurs.
        @param legacy_name: Legacy network name of this user used for login.
        """

        raise NotImplementedError()

    def handle_message_send_request(self, user, legacy_name, message,
                                    xhtml='', mid=0):
        """
        Called when XMPP user sends message to legacy network.
        @param user: XMPP JID of user for which this event occurs.
        @param legacy_name: Legacy network name of buddy or room.
        @param message: Plain text message.
        @param xhtml: XHTML message.
        @param mid: message ID
        """

        raise NotImplementedError()

    def handle_message_ack_request(self, user, legacy_name, mid=0):
        """
        Called when XMPP user sends message to legacy network.
        @param user: XMPP JID of user for which this event occurs.
        @param legacy_name: Legacy network name of buddy or room.
        @param mid: message ID
        """

        # raise NotImplementedError()
        pass

    def handle_vcard_request(self, user, legacy_name, mid):
        """ Called when XMPP user requests VCard of buddy.
        @param user: XMPP JID of user for which this event occurs.
        @param legacy_name: Legacy network name of buddy
                            whose VCard is requested.
        @param mid: ID which is associated with this request.
                           You have to pass it to handle_vcard function
                           when you receive VCard.
        """

        pass

    def handle_vcard_updated_request(self, user, photo, nickname):
        """
        Called when XMPP user updates his own VCard.
        You should update the VCard in legacy network too.
        @param user: XMPP JID of user for which this event occurs.
        @param photo: Raw photo data.
        """

        pass

    def handle_join_room_request(self, user, room, nickname, password):
        pass

    def handle_leave_room_request(self, user, room):
        pass

    def handle_status_change_request(self, user, status, status_message):
        pass

    def handle_buddy_updated_request(self, user, buddy_name, alias, groups):
        pass

    def handle_buddy_removed_request(self, user, buddy_name, groups):
        pass

    def handle_buddy_block_toggled(self, user, buddy_name, blocked):
        pass

    def handle_typing_request(self, user, buddy_name):
        pass

    def handle_typed_request(self, user, buddy_name):
        pass

    def handle_stopped_typing_request(self, user, buddy_name):
        pass

    def handle_attention_request(self, user, buddy_name, message):
        pass

    def handle_ft_start_request(self, user, buddy_name,
                                file_name, size, ft_id):
        pass

    def handle_ft_finish_request(self, user, buddy_name,
                                 file_name, size, ft_id):
        pass

    def handle_ft_pause_request(self, ft_id):
        pass

    def handle_ft_continue_request(self, ft_id):
        pass

    def handle_memory_usage(self):
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, 0

    def handle_exit_request(self):
        if self.config['service.ignore_exit_request']:
            return

        sys.exit(1)

    def handle_raw_xml_request(self, xml):
        pass

    def send_data(self, data):
        pass
