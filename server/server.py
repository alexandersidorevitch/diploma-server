import json
import logging
import socketserver
from typing import Optional

from config import CONFIG
from defs import Action, Result, Type
from logger import get_logger
import errors


class MyTCPHandler(socketserver.BaseRequestHandler):
    HANDLERS = {}
    log = get_logger(__name__, use_file=True, use_stream=True)

    def __init__(self, *args, **kwargs):
        self.closed = False
        self.data = None
        self.action_handler = None
        super().__init__(*args, **kwargs)

    def setup(self):
        self.log.info(f'New connection from {self.client_address}')
        self.HANDLERS[self] = self

    def handle(self):
        while not self.closed:
            data = self.receive_package()
            if data:
                self.received_data(data)
            else:
                self.closed = True

    def received_data(self, data):
        action, message_type, message = self.get_message(data)
        try:
            result, message = self.action_handler.action(action, message_type, message)
        except errors.all_exceptions as err:
            self.error_response(err)
        else:
            self.send_message(result, message)

    def get_message(self, data):
        while len(data) < CONFIG.HEADERS_LEN:
            data += self.receive_package()

        action, data = self._get_header(data, Action, CONFIG.ACTION_LENGTH_HEADER)
        message_type, data = self._get_header(data, Type, CONFIG.MESSAGE_TYPE_HEADER)
        message_len, data = self._get_header(data, int, CONFIG.MESSAGE_LENGTH_HEADER)

        while len(data) < message_len:
            data += self.receive_package()

        message = data[:message_len]

        return action, message_type, json.loads(message.decode('utf-8') or '{}')

    @staticmethod
    def _get_header(data, cls, shift):
        header = cls(
            int.from_bytes(
                data[:shift],
                byteorder='little'
            )
        )
        data = data[shift:]
        return header, data

    def receive_package(self):
        return self.request.recv(CONFIG.RECEIVE_CHUNK_SIZE)

    def send_message(self, result: Result, message: Optional[str] = None) -> None:
        message = '' if message is None else message
        self.request.sendall(
            result.to_bytes(
                CONFIG.RESULT_LENGTH_HEADER,
                byteorder='little'
            )
        )
        self.request.sendall(
            len(message).to_bytes(
                CONFIG.MESSAGE_LENGTH_HEADER,
                byteorder='little'
            )
        )
        self.request.sendall(message)

    def error_response(self, err):
        self.send_message(err.RESULT, str(err))


def run_server(_, address: str = CONFIG.SERVER_ADDR, port: int = CONFIG.SERVER_PORT,
               level: str = logging.getLevelName(logging.INFO)) -> None:
    MyTCPHandler.log.setLevel(level)
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer((address, port), MyTCPHandler) as server:
        server.serve_forever()
