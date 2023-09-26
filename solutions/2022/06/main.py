def first_marker(input: str, unique_chars: int = 4) -> int:
  index = unique_chars
  while len(set(input[index - unique_chars: index])) < unique_chars:
    index += 1  
  return index

def parse_input(filename: str) -> str:
  with open(filename) as f:
    for l in f:
      return l.rstrip()

if __name__ == '__main__':
  print(first_marker(
    parse_input('input/input.txt'),
    unique_chars = 14,
  ))