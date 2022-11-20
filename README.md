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

### Making a Parser From a List of Fields

- Quick Demo

  Lets parse something like the following.

  | Name       | Bit Count | Data Type           |
  |:--         |:--        |:--                  |
  | id         | 8         | 8-bit int           |
  | data count | 16        | 16-bit unsigned int |
  | data       | 8         | 8-bit unsigned int  |

  ```python
  from easyprotocol.fields import UInt8Field, UInt16Field, Int8Field
  from easyprotocol.base import ParseList

  exampleParser = ParseList(name='ExampleParser', children=[
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
