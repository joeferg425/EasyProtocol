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
  from easyprotocol.fields import UInt8Field, UInt16Field, Int8Field
  from easyprotocol.base import ParseList

  exampleParser = ParseList(name='ExampleParser1', children=[
    Int8Field(name='id'),
    UInt16Field(name='data count'),
    UInt8Field(name='data'),
  ])

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
  print(f"bytes:\t{bytes(exampleParser)!r}")

  # You can access parsed elements of a ParseList by numeric index.
  idField = exampleParser[0]
  dataCountField = exampleParser[1]
  dataField = exampleParser[2]
  print(f"{idField.name}:\t\t{idField.value}\t{bytes(idField)!r}")
  print(f"{dataCountField.name}:\t{dataCountField.value}\t{bytes(dataCountField)!r}")
  print(f"{dataField.name}:\t\t{dataField.value}\t{bytes(dataField)!r}")
  ```

- Output

  ```bash
  input:  b'\x01\x00\x01\x80'

  parsed: ExampleParser: [id: 1, data count: 0001(hex), data: -128]
  bytes:  b'\x01\x00\x01\x80'

  parsed: ExampleParser: [id: 3, data count: 0101(hex), data: 127]
  bytes:  b'\x03\x01\x01\x7f'
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
  from easyprotocol.fields import UInt8Field, UInt16Field, Int8Field, ArrayField
  from easyprotocol.base import ParseDict, ParseList

  # you can define your field classes before using them in a parser.
  id = Int8Field(name="id")
  count = UInt16Field(name="count")
  data_array = ArrayField(name="data", count_field=count, array_item_class=UInt8Field)

  # Make an instance of the modified list type and add your fields as the list items.

  exampleParser = ParseDict(
      # give the parser a name
      name="ExampleParser",
      # define your fields in order
      children=[
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
  exampleParser.value = {"id": 3, "count": 2, "data": [127, UInt8Field(name="new data", value=15)]}
  print(f"parsed:\t{exampleParser}")
  print(f"bytes:\t{bytes(exampleParser)!r}\n")

  # You can access parsed elements of a ParseDict by name.
  idField = exampleParser[id.name]
  dataCountField = exampleParser[count.name]
  dataField = cast(ParseList, exampleParser[data_array.name])
  # The ArrayField is a list type, so children are accessed by numeric index.
  data0Field = dataField[0]
  data1Field = dataField[1]
  print(f"{idField.name}:\t\t{idField.value}\t\t{bytes(idField)!r}")
  print(f"{dataCountField.name}:\t\t{dataCountField.value}\t\t{bytes(dataCountField)!r}")
  print(f"{dataField.name}:\t\t{dataField.value}\t{bytes(dataField)!r}")
  print(f"{data0Field.name}:\t\t{data0Field.value}\t\t{bytes(data0Field)!r}")
  print(f"{data1Field.name}:\t{data1Field.value}\t\t{bytes(data1Field)!r}")
  ```

- Output

  ```bash
  input:  b'\x01\x00\x01\x80'

  parsed: ExampleParser: [id: 1, count: 0001(hex), data: [f0: 80(hex)]]
  bytes:  b'\x01\x00\x01\x80'

  parsed: ExampleParser: [id: 3, count: 0002(hex), data: [f0: 7F(hex), new data: 0F(hex)]]
  bytes:  b'\x03\x00\x02\x7f\x0f'

  id:             3               b'\x03'
  count:          2               b'\x00\x02'
  data:           [127, 15]       b'\x7f\x0f'
  f0:             127             b'\x7f'
  new data:       15              b'\x0f'
  ```
