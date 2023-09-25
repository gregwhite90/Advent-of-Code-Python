from collections import defaultdict

orbitees = defaultdict(set)
orbits = {}
planets = set()

with open('input/input.txt') as input:
  for line in input:
    orbitee, orbiter = line.strip().split(')')
    orbitees[orbiter].add(orbitee)
    planets.add(orbiter)
    planets.add(orbitee)

def num_orbits(orbits, orbiter):
  if orbiter not in orbits:
    orbits[orbiter] = sum([1 + num_orbits(orbits, orbitee) for orbitee in orbitees[orbiter]])
  return orbits[orbiter]
  
for planet in planets:
  num_orbits(orbits, planet)

print(sum(orbits.values()))