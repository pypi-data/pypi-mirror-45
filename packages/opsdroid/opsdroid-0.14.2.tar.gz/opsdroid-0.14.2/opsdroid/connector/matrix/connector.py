"""Connector for Matrix (https://matrix.org)."""

import re
import logging

import aiohttp

from matrix_api_async.api_asyncio import AsyncHTTPAPI
from matrix_client.errors import MatrixRequestError

from opsdroid.connector import Connector
from opsdroid.events import Message

from .html_cleaner import clean


_LOGGER = logging.getLogger(__name__)

__all__ = ['ConnectorMatrix']


class ConnectorMatrix(Connector):
    """Connector for Matrix (https://matrix.org)."""

    def __init__(self, config, opsdroid=None):  # noqa: D107
        """Init the config for the connector."""
        super().__init__(config, opsdroid=opsdroid)

        self.name = "ConnectorMatrix"  # The name of your connector
        self.config = config  # The config dictionary to be accessed later
        self.rooms = config.get('rooms', None)
        if not self.rooms:
            self.rooms = {'main': config['room']}
        self.room_ids = {}
        self.default_room = self.rooms['main']
        self.mxid = config['mxid']
        self.nick = config.get('nick', None)
        self.homeserver = config.get('homeserver', "https://matrix.org")
        self.password = config['password']
        self.room_specific_nicks = config.get("room_specific_nicks", False)
        self.session = None
        self.filter_id = None
        self.connection = None

    @property
    def filter_json(self):
        """Define JSON filter to apply to incoming events."""
        return {
            "event_format": "client",
            "account_data": {
                "limit": 0,
                "types": []
            },
            "presence": {
                "limit": 0,
                "types": []
            },
            "room": {
                "rooms": [],
                "account_data": {
                    "types": []
                },
                "timeline": {
                    "types": ["m.room.message"]
                },
                "ephemeral": {
                    "types": []
                },
                "state": {
                    "types": []
                }
            }
        }

    async def make_filter(self, api, room_ids):
        """Make a filter on the server for future syncs."""
        fjson = self.filter_json
        for room_id in room_ids:
            fjson['room']['rooms'].append(room_id)

        resp = await api.create_filter(
            user_id=self.mxid, filter_params=fjson)

        return resp['filter_id']

    async def connect(self):
        """Create connection object with chat library."""
        session = aiohttp.ClientSession()
        mapi = AsyncHTTPAPI(self.homeserver, session)

        self.session = session
        login_response = await mapi.login(
            "m.login.password", user=self.mxid, password=self.password)
        mapi.token = login_response['access_token']
        mapi.sync_token = None

        for roomname, room in self.rooms.items():
            response = await mapi.join_room(room)
            self.room_ids[roomname] = response['room_id']
        self.connection = mapi

        # Create a filter now, saves time on each later sync
        self.filter_id = await self.make_filter(mapi, self.room_ids.values())

        # Do initial sync so we don't get old messages later.
        response = await self.connection.sync(
            timeout_ms=3000,
            filter='{ "room": { "timeline" : { "limit" : 1 } } }',
            set_presence="online")
        self.connection.sync_token = response["next_batch"]

        if self.nick:
            display_name = await self.connection.get_display_name(self.mxid)
            if display_name != self.nick:
                await self.connection.set_display_name(self.mxid, self.nick)

    async def _parse_sync_response(self, response):
        self.connection.sync_token = response["next_batch"]
        for roomid in self.room_ids.values():
            room = response['rooms']['join'].get(roomid, None)
            if room and 'timeline' in room:
                for event in room['timeline']['events']:
                    if event['content']['msgtype'] == 'm.text':
                        if event['sender'] != self.mxid:
                            return Message(
                                await self._get_nick(roomid, event['sender']),
                                roomid, self,
                                event['content']['body'],
                                raw_event=event)

    async def listen(self):  # pragma: no cover
        """Listen for new messages from the chat service."""
        while True:  # pylint: disable=R1702
            try:
                response = await self.connection.sync(
                    self.connection.sync_token,
                    timeout_ms=int(6 * 60 * 60 * 1e3),  # 6h in ms
                    filter=self.filter_id)
                _LOGGER.debug("matrix sync request returned")
                message = await self._parse_sync_response(response)
                await self.opsdroid.parse(message)

            except Exception:  # pylint: disable=W0703
                _LOGGER.exception('Matrix Sync Error')

    async def _get_nick(self, roomid, mxid):
        """
        Get nickname from user ID.

        Get the nickname of a sender depending on the room specific config
        setting.
        """
        if self.room_specific_nicks:
            try:
                return await self.connection.get_room_displayname(roomid, mxid)
            except Exception:  # pylint: disable=W0703
                # Fallback to the non-room specific one
                logging.exception(
                    "Failed to lookup room specific nick for %s", mxid)

        try:
            return await self.connection.get_display_name(mxid)
        except MatrixRequestError as mre:
            # Log the error if it's not the 404 from the user not having a nick
            if mre.code != 404:
                logging.exception("Failed to lookup nick for %s", mxid)
            return mxid

    @staticmethod
    def _get_formatted_message_body(message, body=None, msgtype="m.text"):
        """
        Get HTML from a message.

        Return the json representation of the message in
        "org.matrix.custom.html" format.
        """
        # Markdown leaves a <p></p> around standard messages that we want to
        # strip:
        if message.startswith('<p>'):
            message = message[3:]
            if message.endswith('</p>'):
                message = message[:-4]

        clean_html = clean(message)

        return {
            # Strip out any tags from the markdown to make the body
            "body": body if body else re.sub('<[^<]+?>', '', clean_html),
            "msgtype": msgtype,
            "format": "org.matrix.custom.html",
            "formatted_body": clean_html
            }

    async def respond(self, message, room=None):
        """Send `message.text` back to the chat service."""
        if not room:
            # Connector responds in the same room it received the original
            # message
            room_id = message.room
        else:
            room_id = self.rooms[room]

        # Ensure we have a room id not alias
        if not room_id.startswith('!'):
            room_id = await self.connection.get_room_id(room_id)
        else:
            room_id = room_id

        try:
            await self.connection.send_message_event(
                room_id,
                "m.room.message",
                self._get_formatted_message_body(message.text))
        except aiohttp.client_exceptions.ServerDisconnectedError:
            _LOGGER.debug("Server had disconnected, retrying send.")
            await self.connection.send_message_event(
                room_id,
                "m.room.message",
                self._get_formatted_message_body(message.text))

    async def disconnect(self):
        """Close the matrix session."""
        await self.session.close()

    def get_roomname(self, room):
        """Get the name of a room from alias or room ID."""
        if room.startswith(('#', '!')):
            for connroom in self.rooms:
                if room in (connroom, self.room_ids[connroom]):
                    return connroom

        return room
