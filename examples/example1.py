"""Define your parser using simple python classes and familiar types."""
from easyprotocol.base import ParseFieldList, hex
from easyprotocol.fields import Int8Field, UInt8Field, UInt16Field

# Make an instance of the modified list type and add your fields as the list items.
exampleParser = ParseFieldList(
    # give the parser a name
    name="ExampleParser1",
    # define your fields in order
    default=[
        # give each field a name, some standard field types are already defined.
        Int8Field(name="id"),
        UInt16Field(name="count"),
        UInt8Field(name="data"),
    ],
)

# Some example data bytes to parse
data = b"\x01\x00\x01\x80"
print(f"input bytes:\t{data!r}")
print(f"input hex:\t{hex(data)}\n")

# Parse the bytes
exampleParser.parse(data=data)

# Print the parsed data to see what we got
print(f"parsed:\t{exampleParser}")
print(f"bytes:\t{bytes(exampleParser)!r}")
print(f"hex:\t{exampleParser.hex_value}\n")

# Make a new frame from known data to send somewhere (like a socket)
exampleParser[0].value = 3
exampleParser.value = [3, 257, 127]
exampleParser.value = [3, 257, 127]
print(f"parsed:\t{exampleParser}")
print(f"bytes:\t{bytes(exampleParser)!r}")
print(f"hex:\t{exampleParser.hex_value}\n")

# You can access parsed elements of a ParseList by numeric index.
for child in exampleParser.children.values():
    print(f'{child.name}:\t{child.value}\t"{child.string_value}"')
print()

# Wait, I don't really like hexadecimal
exampleParser.string_format = "{}"
for child in exampleParser.children.values():
    child.string_format = "{}"

# Print the values again
exampleParser[0].value = 3
exampleParser.value = [3, 257, 127]
exampleParser.value = [3, 257, 127]
print(f"parsed:\t{exampleParser}")
print(f"bytes:\t{bytes(exampleParser)!r}")
print(f"hex:\t{exampleParser.hex_value}\n")
for child in exampleParser.children.values():
    print(f'{child.name}:\t{child.value}\t"{child.string_value}"')
