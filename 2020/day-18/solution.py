import math
import re
from collections import defaultdict

class Expression():
    def __init__(
            self,
            expression,
    ):
        self.index = 0
        self.expression = expression
        self.number_re = re.compile(r"^(?P<num>\d+)")
        self.operator_re = re.compile(r"^(?P<operator>[\+\*])")
        self.total = self.next_value()
        self.cur_operator = None
        self.product_operands = []

    def value_and_index(
            self,
    ):
        # TODO: also test for the parentheses
        finished = False
        while self.index < len(self.expression) and not finished:
            finished = self.process_next()


        self.product_operands.append(self.total)
        return math.prod(self.product_operands), self.index

    def process_next(
            self,
    ):
        if self.expression[self.index] == ')':
            self.index += 1
            return True
        elif self.expression[self.index] == ' ':
            self.index += 1
        elif self.cur_operator:
            assert(self.cur_operator in set(['+', '*']))
            if self.cur_operator == '+':
                self.total += self.next_value()
            elif self.cur_operator == '*':
                self.product_operands.append(self.total)
                self.total = self.next_value()
            self.cur_operator = None
        else:
            self.cur_operator = self.next_operator()

        return False
        
    def next_value(
            self,
    ):
        if self.expression[self.index] == '(':
            value, incr_index = Expression(self.expression[self.index + 1:]).value_and_index()
            self.index += incr_index + 1
            return value
        else:
            num_match = self.number_re.match(self.expression[self.index:])
            assert(num_match)
            num = num_match['num']
            self.index += len(num)
            return int(num)

    def next_operator(
            self,
    ):
        operator_match = self.operator_re.match(self.expression[self.index:])
        assert(operator_match)
        operator = operator_match['operator']
        self.index += len(operator)
        return operator

def both_parts():
    with open('input/input.txt') as infile:
        total = 0
        for line in infile:
            total += Expression(line.strip()).value_and_index()[0]
    return total

if __name__ == '__main__':
    print(both_parts())
