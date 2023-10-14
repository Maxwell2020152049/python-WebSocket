
import struct

greeting: str = "Hello World!"
len_greeting = len(greeting)
print(f"len({greeting}):", len_greeting)

pack_format = f">I{len_greeting}sI"

pack = struct.pack(pack_format, 0x3ff, bytes(greeting, encoding="utf8"), 2020152049)

print(bytes(greeting, encoding="utf8"))

print(pack)

unpack = struct.unpack(pack_format, pack)

print(unpack)