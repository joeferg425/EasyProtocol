"""Define your parser using simple python classes and familiar types."""
from easyprotocol.fields import UInt8Field, UInt16Field, Int8Field
from easyprotocol.base import ParseList

# Make an instance of the modified list type and add your fields as the list items.
exampleParser = ParseList(
    # give the parser a name
    name="ExampleParser",
    # define your fields in order
    children=[
        # give each field a name, some standard types are defined for you.
        Int8Field(name="id"),
        UInt16Field(name="data count"),
        UInt8Field(name="data"),
    ],
)

# Some example data bytes to parse
data = b"\x01\x00\x01\x80"
print(f"input:\t{data!r}\n")

# Parse the bytes
exampleParser.parse(data=data)
# Print the parsed data to see what we got
print(f"parsed:\t{exampleParser}")
print(f"bytes:\t{bytes(exampleParser)!r}\n")

# Make a new frame from known data to send somewhere (like a socket)
exampleParser.value = [3, 257, 127]
print(f"parsed:\t{exampleParser}")
print(f"bytes:\t{bytes(exampleParser)!r}\n")

# You can access parsed elements of a ParseList by numeric index.
idField = exampleParser[0]
dataCountField = exampleParser[1]
dataField = exampleParser[2]
print(f"{idField.name}:\t\t{idField.value}\t{bytes(idField)!r}")
print(f"{dataCountField.name}:\t{dataCountField.value}\t{bytes(dataCountField)!r}")
print(f"{dataField.name}:\t\t{dataField.value}\t{bytes(dataField)!r}")
