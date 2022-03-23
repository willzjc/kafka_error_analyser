# Kafka Schema conflict exception log analyser

## Installation

### Dependencies

1. Python3
2. pydiff - https://github.com/yebrahim/difflibparser.git

Run git clone with recursive as this relies on pydiff at https://github.com/yebrahim/difflibparser.git
(pydiff also requires recursive git clone)

```
git clone --recursive https://github.com/willzjc/kafka_error_analyser.git
```

## Usage

1. Put error content into input/error.log For example:

```
Caused by: java.io.IOException: Incompatible schema ... blah blah blah
```

2. Run ErrorParser.py
3. It will generate a diff of the conflicting schemas

![readme/example.png](readme/example.png)