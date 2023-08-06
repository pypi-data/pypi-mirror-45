# config_argparse

Config library based on standard ArgumentParser.

## Usage

**Simple:**

```python3
from config_argparse import Config

class MyConfig(Config):
    weight = 10.0         # -> .add_argument('--weight', type=float, default=10.0)
    layers = [10, 20, 30] # -> .add_argument('--layers', type=int, nargs='+', default=[10, 20, 30])

MyConfig().parse_args([])
# MyConfig:
#         weight = 10.0
#         layers = [10, 20, 30]

MyConfig().parse_args(['--weight', '30.5', '--layers', '1', '2'])
# MyConfig:
#        weight = 30.5
#        layers = [1, 2]

MyConfig().parse_args(['--help'])
# usage: MyConfig [-h] [--weight WEIGHT] [--layers LAYERS [LAYERS ...]]
#
# optional arguments:
#   -h, --help            show this help message and exit
#   --weight WEIGHT
#   --layers LAYERS [LAYERS ...]
```

You can use `int`, `float`, `str`, `bool`, and `list` of them.

`config_argparse.Config` automatically generates `argparse.ArgumentParser` internally and parse arguments.

All the values defined as class variables are copied to the instance by `copy.deepcopy`.

**Nested:**

This library supports nested config (it generates multiple `ArgumentParser` internally).

```python3
from config_argparse import Config

class Nest(Config):
    a = 10

class MyConfig(Config):
    a = 'str'
    nest = Nest()  # -> .add_argument('--nest.a', type=int, default=10, dest=`a in nest`)

MyConfig().parse_args([])
# MyConfig:
#         a = str
#         nest = Nest:
#                 a = 10

MyConfig().parse_args(['--nest.a', '33'])
# MyConfig:
#        a = str
#        nest = Nest:
#                a = 33

MyConfig().parse_args(['--help'])
# usage: MyConfig [-h] [--a A] [--nest]
#
# optional arguments:
#   -h, --help  show this help message and exit
#   --a A
#   --nest

MyConfig().parse_args(['--nest.help'])
# usage: Nest [-h] [--nest.a A]
#
# optional arguments:
#   -h, --help  show this help message and exit
#   --nest.a A
```

**Inherited:**

You can merge multiple configs by inheriting them.

```python3
from config_argparse import Config

class ParentA(Config):
    a = 10

class ParentB(Config):
    b = 10

class MyConfig(ParentA, ParentB):
    c = 'str'

MyConfig().parse_args([])
# MyConfig:
#         a = 10
#         b = 10
#         c = str

MyConfig().parse_args(['--a', '33'])
# MyConfig:
#         a = 33
#         b = 10
#         c = str
```

**Dynamic:**

You can dynamically build nested configs according to the values in the parent.

```python3
from config_argparse import Config, Value, DynamicConfig

class ConfigA(Config):
    a = 1

class ConfigB(Config):
    b = 1

config_map = {
    'a': ConfigA,
    'b': ConfigB,
}

class MyConfig(Config):
    lr = 0.1
    epoch = 100
    model = Value('a', choices=list(config_map.keys()))
    model_cfg = DynamicConfig(lambda c: config_map[c.model]()) # pass function which returns Type[Config]

args = MyConfig().parse_args([])
print(args)
# MyConfig:
#         lr = 0.1
#         epoch = 100
#         model = a
#         model_cfg = ConfigA:
#                 a = 1

args = MyConfig().parse_args(['--lr', '1', '--model', 'b', '--model_cfg.b', '100'])
print(args)
# MyConfig:
#         lr = 1.0
#         epoch = 100
#         model = b
#         model_cfg = ConfigB:
#                 b = 100
```

**Value:**

You can use some `ArgumentParser`'s features such as `required`, `choices` by `config_argparse.Value`.

```python3
from config_argparse import Config, Value

class MyConfig(Config):
    weight = Value(type=float, required=True)
    dim = Value('a', choices=['a', 'b', 'c'])

MyConfig().parse_args([])
# MyConfig: error: the following arguments are required: --weight

MyConfig().parse_args(['--weight', '1.0', '--dim', 'foo'])
# MyConfig: error: argument --dim: invalid choice: 'foo' (choose from 'a', 'b', 'c')
```

**Convert to/from dict**

Default values can be set by passing dict like object to `Config::__init__`.

`Config::todict` creates serializable dict (if the config is already parsed).

```python3
import json
from config_argparse import Config

class MyConfig(Config):
    weight = 10.0         # -> .add_argument('--weight', type=float, default=10.0)
    layers = [10, 20, 30] # -> .add_argument('--layers', type=int, nargs='+', default=[10, 20, 30])

c = MyConfig({'weight': 1.0}).parse_args([])
c.weight
# -> 1.0
c.todict()
# -> {'weight': 1.0, 'layers': [10, 20, 30]}
```
