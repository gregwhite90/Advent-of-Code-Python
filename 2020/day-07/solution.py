import re
from collections import defaultdict

def add_parents_recursive(found_parents, all_parents, key):
    for parent in all_parents[key]:
        if parent in found_parents: continue
        found_parents.add(parent)
        add_parents_recursive(found_parents, all_parents, parent)

def total_children_bags_recursive(all_children, key):
    return sum([num * (1 + total_children_bags_recursive(all_children, child)) for child, num in all_children[key].items()])

def both_parts():
    parents = defaultdict(set)
    children = defaultdict(dict)
    line_re = re.compile(r"^(?P<cur_bag>.*) bags contain (?P<contained_bags>.*)\.$")
    contained_bag_re = re.compile(r"(?P<num>\d+) (?P<contained_bag>[\w\s]*) bags?")
    
    with open('input/input.txt') as input_file:
        for row in input_file:
            line_match = line_re.match(row.strip())
            if line_match['contained_bags'] == 'no other bags': continue
            for contained_bag in line_match['contained_bags'].split(', '):
                contained_bag_match = contained_bag_re.match(contained_bag)
                parents[contained_bag_match['contained_bag']].add(line_match['cur_bag'])
                children[line_match['cur_bag']][contained_bag_match['contained_bag']] = int(contained_bag_match['num'])

    shiny_gold_parents = set()
    print(children)
    add_parents_recursive(shiny_gold_parents, parents, 'shiny gold')
    
    return len(shiny_gold_parents), total_children_bags_recursive(children, 'shiny gold')

if __name__ == '__main__':
    print(both_parts())
