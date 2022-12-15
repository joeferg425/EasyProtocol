"""Define your parser using simple python classes and familiar types."""
from typing import cast

from easyprotocol.base import ParseFieldDict, ParseFieldList
from easyprotocol.fields import Int8Field, ParseArrayField, UInt8Field, UInt16Field

# you can define your field classes before using them in a parser.
id = Int8Field(name="id")
count = UInt16Field(name="count")
data_array = ParseArrayField(
    name="data",
    count=count,
    array_item_class=UInt8Field,
    array_item_default=0,
)

# Make an instance of the modified list type and add your fields as the list items.

exampleParser = ParseFieldDict(
    # give the parser a name
    name="ExampleParser",
    # define your fields in order
    default=[
        # give each field a name, some standard types are defined for you.
        id,
        count,
        data_array,
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
exampleParser["id"].value = 3
exampleParser["count"].value = 2
exampleParser["data"].value = [
    127,
    UInt8Field(name="new data", default=15),
]

print(f"parsed:\t{exampleParser}")
print(f"bytes:\t{bytes(exampleParser)!r}\n")

# You can access parsed elements of a ParseDict by name.
idField = exampleParser[id.name]
dataCountField = exampleParser[count.name]
dataField = cast(ParseFieldList, exampleParser[data_array.name])
# The ArrayField is a list type, so children are accessed by numeric index.
data0Field = dataField[0]
data1Field = dataField[1]
print(f"{idField.name}:\t\t{idField.value}\t\t{bytes(idField)!r}")
print(f"{dataCountField.name}:\t\t{dataCountField.value}\t\t{bytes(dataCountField)!r}")
print(f"{dataField.name}:\t\t{dataField.value}\t{bytes(dataField)!r}")
print(f"{data0Field.name}:\t\t{data0Field.value}\t\t{bytes(data0Field)!r}")
print(f"{data1Field.name}:\t\t{data1Field.value}\t\t{bytes(data1Field)!r}")
