"""Define your parser using simple python classes and familiar types."""
from typing import cast

from easyprotocol.base import ParseFieldDict, ParseFieldList, hex
from easyprotocol.fields import ArrayField, Int8Field, UInt8Field, UInt16Field

# you can define your field classes before using them in a parser.
ident = Int8Field(name="id")
count = UInt16Field(
    name="count",
    # Let's modify the display of the field value
    string_format="{} data items",
)
data_array = ArrayField(
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
        ident,
        count,
        data_array,
    ],
)

# Some example data bytes to parse
data = b"\x01\x00\x01\x80"
print(f"input bytes:\t{data!r}\n")
print(f"input hex:\t{hex(data)}\n")

# Parse the bytes
exampleParser.parse(data=data)
# Print the parsed data to see what we got
print(f"parsed:\t{exampleParser}")
print(f"hex:\t{hex(exampleParser)}\n")

# Make a new frame from known data to send somewhere (like a socket)
exampleParser["id"].value = 3
exampleParser["count"].value = 2
exampleParser["data"].value = [
    127,
    UInt8Field(name="new data", default=15),
]

print(f"parsed:\t{exampleParser}")
print(f"hex:\t{hex(exampleParser)}\n")

# You can access parsed elements of a ParseDict by name.
idField = exampleParser[ident.name]
dataCountField = exampleParser[count.name]
dataField = cast(ParseFieldList, exampleParser[data_array.name])

# The ArrayField is a list type, so children are accessed by numeric index.
for child in exampleParser.values():
    print(f"{child.name}:\t{child.value}\t\t{child.bits_str}")
