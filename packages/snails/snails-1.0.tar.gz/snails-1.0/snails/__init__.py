from __future__ import annotations
import atexit

from aiosmtpd.controller import Controller
from aiosmtpd.smtp import Session, SMTP, Envelope
from email.parser import Parser
from email.message import Message
from typing import Callable, Optional

__all__ = ["Mailbox", "Message", "serve"]
__version__ = "1.0"

SNAILS_ERROR = "500 Could not process your message"
SNAILS_OK = "250 OK"

_MailHandler = Callable[[Message], Optional[str]]


class _Wrapper:
    def __init__(self, handler: _MailHandler) -> None:
        self.handler = handler

    async def handle_DATA(self, server: SMTP, session: Session, envelope: Envelope) -> str:
        # https://aiosmtpd.readthedocs.io/en/latest/aiosmtpd/docs/migrating.html
        data = envelope.content
        msg = Parser().parsestr(data.decode())

        # noinspection PyBroadException
        try:
            res = self.handler(msg)
        except Exception:
            return SNAILS_ERROR
        else:
            return res or SNAILS_OK


class Mailbox:
    _controller: Optional[Controller] = None

    def __init__(self, *, handler: _MailHandler, host: str, port: int) -> None:
        """
            Usage:

        .. code-block:: python

            import snails
            def handle(msg: snails.Message) -> None:
                print(f"To: {msg['to']}\nFrom: {msg['from']}\nSubject: {msg['subject']}")
                for p in msg.get_payload():
                    print(p.get_payload(decode=True))

            mailbox = snails.Mailbox(handle, "127.0.0.1", 10025)
            mailbox.start()

        :param handler:
        :param host:
        :param port:
        """
        self.handler = handler
        self.host = host
        self.port = port

    def start(self) -> None:
        self.stop()
        self._controller = Controller(
            # closure lets us change mailbox.handler at runtime
            _Wrapper(lambda msg: self.handler(msg)),
            hostname=self.host, port=self.port)
        self._controller.start()

    def stop(self) -> None:
        if self._controller:
            self._controller.stop()
            self._controller = None


def serve(handler: _MailHandler, host: str, port: int, block: bool = True, cleanup_at_exit: bool = True) -> Mailbox:
    """

    Usage:

    .. code-block:: python

        import snails
        def handle(msg: snails.Message) -> None:
            print(f"To: {msg['to']}\nFrom: {msg['from']}\nSubject: {msg['subject']}")
            for p in msg.get_payload():
                print(p.get_payload(decode=True))

        snails.serve(handle, "127.0.0.1", 10025)

    :param handler:
    :param host:
    :param port:
    :param block:
    :param cleanup_at_exit:
    :return:
    """
    mailbox = Mailbox(handler=handler, host=host, port=port)
    mailbox.start()

    if cleanup_at_exit:
        atexit.register(mailbox.stop)

    if block:
        try:
            while True:
                pass
        except KeyboardInterrupt:
            pass
    return mailbox
