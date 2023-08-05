from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.completion import WordCompleter

from radio.models import radios

# Cria list_buffer
# para resetar um buffer -> buffer.reset(Document(text, 0))
list_buffer = Buffer(
    document=Document(radios.content, 0),
    multiline=True,
    read_only=True,
    name="list_buffer",
)

# cria command_buffer
command_buffer = Buffer(
    completer=WordCompleter(
        ["play", "stop", "info", "help", "stations", "bytag", "byid", "exit"],
        ignore_case=True,
    ),
    complete_while_typing=True,
    name="command_buffer",
)


class DisplayBuffer:
    def __init__(self):
        self._buffer = Buffer(document=Document("", 0), read_only=True)

    @property
    def buffer(self):
        return self._buffer

    @buffer.setter
    def buffer(self, value):
        self._buffer.set_document(Document(value, 0), bypass_readonly=True)


display_buffer = DisplayBuffer()
