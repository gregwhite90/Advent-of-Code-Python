def print_num(num):
  print(num)
  print(f"mod {19} = {num % 19} (vs. {0})")
  print(f"mod {37} = {num % 37} (vs. {24})")
  print(f"mod {883} = {num % 883} (vs. {864})")
  print(f"mod {23} = {num % 23} (vs. {19})")
  print(f"mod {13} = {num % 13} (vs. {7})")
  print(f"mod {17} = {num % 17} (vs. {15})")
  print(f"mod {797} = {num % 797} (vs. {747})")
  print(f"mod {41} = {num % 41} (vs. {22})")
  print(f"mod {29} = {num % 29} (vs. {8})")
  print("\n")

num = 87638212952466

for _ in range(29):
  print_num(num)
  if (
    num % 37 == 24 and
    num % 883 == 864 and
    num % 23 == 19 and
    num % 13 == 7 and
    num % 17 == 15 and
    num % 797 == 747 and
    num % 41 == 22 and
    num % 29 == 8
  ):
    break
  
  num += 19 * 883 * 797 * 37 * 23 * 13 * 17 * 41