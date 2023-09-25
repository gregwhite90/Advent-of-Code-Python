if __name__ == '__main__':    
  for ls, pk in [(18738047, 12721030), (3794585, 10943862)]:
    value = 1
    for i in range(ls):
      value = (value * pk) % 20201227
    print(value)