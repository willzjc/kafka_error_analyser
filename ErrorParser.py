import subprocess
import pprint
import json
import logging

null = None
true = True
false = False
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)

TOPIC_FILE = 'out/TOPIC_SCHEMA.json'
MESSAGE_FILE = 'out/MESSAGE_SCHEMA.json'


class ErrorParser:

    def __init__(self, file: str) -> None:
        logger.info(f'Reading {file}')
        error = open(file).read()
        self.error_log = error
        self.lhs_current_topic = None
        self.rhs_message_input = None

    @staticmethod
    def parse_string_brute_force(s: str):
        value = None
        while len(s) and value is None:
            try:
                value = eval(s)
            except:
                s = s[:-1]
        return value

    def parse_brace_matching(self):
        start_brace, end_brace, start_token = None, None, None
        stack_count = 1
        lhs = []
        rhs = []
        ptr = lhs
        for i, c in enumerate(self.error_log):
            if start_token is None:
                for brace in ['{}']:
                    if c in brace:
                        start_token = [i, brace]
                        start_brace, end_brace = brace[0], brace[1]
                        ptr.append(c)
                        stack_count = 1
                        break
            else:
                if c == start_brace:
                    stack_count += 1
                elif c == end_brace:
                    stack_count -= 1

                ptr.append(c)

                if stack_count == 0:
                    if ptr == lhs:
                        ptr = rhs
                    else:
                        break
                    start_token = None

        lhsstr = ''.join(lhs)
        rhsstr = ''.join(rhs)

        return eval(lhsstr), eval(rhsstr)

    def parse(self) -> None:
        lhs, rhs = self.parse_brace_matching()

        self.lhs_current_topic = lhs_current_topic = lhs
        self.rhs_message_input = rhs_message_input = rhs
        pprint.pprint(lhs_current_topic, indent=1)
        pprint.pprint(rhs_message_input, indent=1)

        with open(TOPIC_FILE, "w") as flhs_current_topic:
            flhs_current_topic.write(json.dumps(self.lhs_current_topic, indent=1))
        with open(MESSAGE_FILE, "w") as frhs_message_input:
            frhs_message_input.write(json.dumps(self.rhs_message_input, indent=1))

    def pattern_match_parse(self):

        for start_match, mid_match in [["Incompatible schema", "of type AVRO for schema"],
                                       ["Writers schema:", "Readers schema:"]]:
            if start_match in self.error_log and mid_match in self.error_log:
                start = self.error_log.split(start_match)[-1]
                elements = start.split(mid_match)
                for i, e in enumerate(elements):
                    elements[i] = elements[i].strip()
                if len(elements) > 1:
                    while len(elements[0]) > 0 and not (elements[0].endswith("}") or elements[0].endswith("]")):
                        elements[0] = elements[0][:-1]

                return self.parse_string_brute_force(elements[0]), self.parse_string_brute_force(elements[1])

        raise Exception("No pattern found")

    def show_diff(self) -> None:
        subprocess.run([
            "python", "pydiff/pydiff.py", "-p", TOPIC_FILE, MESSAGE_FILE
        ])


def main():
    ep = ErrorParser(file="input/error.log")
    ep.parse()
    ep.showDiff()


if __name__ == '__main__':
    main()
