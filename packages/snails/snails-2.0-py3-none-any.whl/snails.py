from __future__ import annotations
import atexit
import functools
import inspect
import ssl
from email.message import Message
from email.parser import Parser
from typing import Any, Callable, Coroutine, Optional, Tuple, Union

import aiosmtpd.controller
from aiosmtpd.smtp import SMTP, Envelope, Session


__all__ = ["Envelope", "Mailbox", "Message", "serve"]
__version__ = "2.0"

SMTP_250 = "250 ok"
SMTP_451 = "451 server error"
SMTP_500 = "500 syntax error"
SMTP_502 = "502 unsupported command"
SMTP_550 = "550 mailbox unavailable"


def _wrap_handler(original_handler) -> AsyncHandlerType:
    if inspect.iscoroutinefunction(original_handler):
        return original_handler

    @functools.wraps(original_handler)
    async def wrapped_handler(x):
        return original_handler(x)

    return wrapped_handler


def _wrap_parser(original_parser) -> AsyncParserType:
    if inspect.iscoroutinefunction(original_parser):
        return original_parser

    @functools.wraps(original_parser)
    async def wrapped_parser(e):
        return original_parser(e)

    return wrapped_parser


def _infer_parser(handler: AsyncHandlerType) -> AsyncParserType:
    sig = inspect.signature(handler)
    arg_count = len(sig.parameters)
    if arg_count != 1:
        raise ValueError(f"handler must take exactly one positional arg but takes {arg_count} instead")
    arg, = sig.parameters.values()  # type: inspect.Parameter
    arg_type = arg.annotation
    if arg_type is inspect.Parameter.empty:
        raise ValueError(f"provide a parse function or annotate your handler argument")
    try:
        parser = _builtin_parsers[arg_type]
    except KeyError:
        raise ValueError(f"no built-in parser provides the {arg_type} your handler expects")
    else:
        return parser


async def parse_to_envelope(envelope: Envelope) -> Envelope:
    return envelope


async def parse_to_bytes(envelope: Envelope) -> bytes:
    return envelope.content


async def parse_to_message(envelope: Envelope) -> Message:
    return Parser().parsestr(envelope.content.decode())


_builtin_parsers = {
    bytes: parse_to_bytes,
    Envelope: parse_to_envelope,
    Message: parse_to_message
}

AsyncHandlerType = Callable[[Any], Coroutine[None, None, Optional[str]]]  # async def handle(m: Message) -> str
AsyncParserType = Callable[[Envelope], Coroutine[None, None, Any]]  # async def parse(e: Envelope) -> Any


class _Controller(aiosmtpd.controller.Controller):
    @property
    def is_running(self) -> bool:
        return self._thread is not None


class _Wrapper:
    def __init__(self, parser: AsyncParserType, handler: AsyncHandlerType) -> None:
        self.parser = parser
        self.handler = handler

    # noinspection PyPep8Naming
    async def handle_DATA(self, server: SMTP, session: Session, envelope: Envelope) -> str:
        msg = await self.parser(envelope)

        # noinspection PyBroadException
        try:
            res = await self.handler(msg)
        except Exception:
            return SMTP_451
        else:
            if res is None:
                return SMTP_250
            return res


class Mailbox:
    def __init__(
            self, handler: AsyncHandlerType, host: str, port: int,
            parser: Optional[AsyncParserType] = None,
            ssl_context: Union[ssl.SSLContext, Tuple[str, str]] = None) -> None:
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
        """
        handler = _wrap_handler(handler)
        if parser:
            parser = _wrap_parser(parser)
        else:
            parser = _infer_parser(handler)

        self.controller = _Controller(_Wrapper(parser, handler), hostname=host, port=port, ssl_context=ssl_context)

    def start(self) -> None:
        self.stop()
        self.controller.start()

    def stop(self) -> None:
        if self.controller.is_running:
            self.controller.stop()


def serve(handler, host: str, port: int, **kwargs) -> Mailbox:
    """

    Usage:

    .. code-block:: python

        import snails
        def handle(msg: snails.Message) -> None:
            m_to, m_from, m_sub = msg["to"], msg["from"], msg["subject"]

            print(f"To: {m_to}\nFrom: {m_from}\nSubject: {m_sub}")
            for p in msg.get_payload():
                print(p.get_payload(decode=True))

        snails.serve(handle, "127.0.0.1", 10025)
    """
    block = kwargs.pop("block", True)
    cleanup_at_exit = kwargs.pop("cleanup_at_exit", True)

    mailbox = Mailbox(handler, host, port, **kwargs)
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
