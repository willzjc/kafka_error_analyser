# Kafka Schema conflict exception log analyser

## Usage

1. Put error content into input/error.log
For example:
```
Caused by: java.io.IOException: Incompatible schema ... blah blah blah
```
2. Run ErrorParser.py
3. It will generate a diff of the conflicting schemas
