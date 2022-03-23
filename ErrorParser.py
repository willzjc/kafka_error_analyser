import subprocess
import pprint
import json
import logging

null = None
true = True
false = False
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)


class ErrorParser:

    def __init__(self, file: str) -> None:
        logger.info(f'Reading {file}')
        error = open(file).read()
        self.error = error
        self.lhs_current_topic = None
        self.rhs_message_input = None

    def parse(self) -> None:
        start = self.error.split("Incompatible schema")[-1]
        elements = start.split("of type AVRO for schema")
        for i, e in enumerate(elements):
            elements[i] = elements[i].strip()
        if len(elements) > 1:
            while len(elements[0]) > 0 and not elements[0].endswith("}"):
                elements[0] = elements[0][:-1]
        self.lhs_current_topic = lhs_current_topic = eval(elements[0])
        self.rhs_message_input = rhs_message_input = eval(elements[1])
        pprint.pprint(lhs_current_topic, indent=1)
        pprint.pprint(rhs_message_input, indent=1)

    def showDiff(self) -> None:
        if self.lhs_current_topic is None or self.rhs_message_input is None:
            self.parse()
        with open("out/lhs_current_topic.json", "w") as flhs_current_topic:
            flhs_current_topic.write(json.dumps(self.lhs_current_topic, indent=1))
        with open("out/rhs_message_input.json", "w") as frhs_message_input:
            frhs_message_input.write(json.dumps(self.rhs_message_input, indent=1))

        subprocess.run([
            "python", "pydiff/pydiff.py", "-p", "out/lhs_current_topic.json", "out/rhs_message_input.json"
        ])


def main():
    ep = ErrorParser(file="input/error.log")
    ep.showDiff()


if __name__ == '__main__':
    main()
