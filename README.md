# EasyProtocol

## Introduction

A library for quick prototyping protocol parsing in python. Not the fastest, not the most efficient, not the coolest, but hopefully the easiest to modify and prototype with.

## Quick Start

### Installing

For now you have to install from source, this will be on pypi soon.

- Current Method

```bash
git clone https://github.com/joeferg425/EasyProtocol.git .
cd EasyProtocol
python -m pip install .
```

- Future, better method

```bash
python -m pip install easyprotocol
```

### Example 1 - Making a Parser From a List of Fields

- Demo Code

    Lets parse something like the following.

    | Name       | Bit Count | Data Type           |
    |:--         |:--        |:--                  |
    | id         | 8         | 8-bit int           |
    | data count | 16        | 16-bit unsigned int |
    | data       | 8         | 8-bit unsigned int  |

    Fixed frame definition. Nothing fancy.

    ```python
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
    ```

- Output

    ```bash
    input bytes:    b'\x01\x00\x01\x80'
    input hex:      01 00 01 80

    parsed: ExampleParser1: [id: 1, count: 0001(hex), data: 80(hex)]
    bytes:  b'\x01\x00\x01\x80'
    hex:    01 00 01 80

    parsed: ExampleParser1: [id: 3, count: 0101(hex), data: 7F(hex)]
    bytes:  b'\x03\x01\x01\x7f'
    hex:    03 01 01 7F

    id:     3       "3"
    count:  257     "0101(hex)"
    data:   127     "7F(hex)"

    parsed: ExampleParser1: [id: 3, count: 257, data: 127]
    bytes:  b'\x03\x01\x01\x7f'
    hex:    03 01 01 7F

    id:     3       "3"
    count:  257     "257"
    data:   127     "127"
        ```

### Example 2 - Making a Parser from a Dictionary of Fields

- Demo Code

    Lets parse something like the following.

    | Name       | Bit Count | Data Type              |
    |:--         |:--        |:--                     |
    | id         | 8         | 8-bit unsigned int     |
    | count      | 16        | 16-bit unsigned int    |
    | data array | 8         | 8-bit unsigned int(s)  |

    Variable Frame size, handles a variable length array of uint8 chunks.

    ```python
    """Define your parser using simple python classes and familiar types."""
    from typing import cast

    from easyprotocol.base import ParseFieldDict, ParseFieldList, hex
    from easyprotocol.fields import Int8Field, ParseArrayField, UInt8Field, UInt16Field

    # you can define your field classes before using them in a parser.
    ident = Int8Field(name="id")
    count = UInt16Field(
        name="count",
        # Let's modify the display of the field value
        string_format="{} data items",
    )
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
    ```

- Output

    ```bash
    input bytes:    b'\x01\x00\x01\x80'

    input hex:      01 00 01 80

    parsed: ExampleParser: {id: 1, count: 1 data items, data: [#0: 80(hex)]}
    hex:    01 00 01 80

    parsed: ExampleParser: {id: 3, count: 2 data items, data: [#0: 7F(hex), #1: 0F(hex)]}
    hex:    03 00 02 7F 0F

    id:     3               00000011:<b
    count:  2               0000000000000010:<b
    data:   [<UInt8Field> #0: 7F(hex), <UInt8Field> #1: 0F(hex)]            0111111100001111:<b
        ```
