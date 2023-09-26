import numpy as np

# from scanner 0
"""
-618,-824,-621
-537,-823,-458
-447,-329,318
404,-588,-901
"""

# from scanner 1
"""
686,422,578
605,423,415
515,917,-361
-336,658,858
"""

scanner_1_matrix = np.array([
  [686,422,578, 0, 0, 0, 0, 0, 0, 1, 0, 0],
  [0, 0, 0, 686,422,578, 0, 0, 0, 0, 1, 0],
  [0, 0, 0, 0, 0, 0, 686,422,578, 0, 0, 1],
  [605,423,415, 0, 0, 0, 0, 0, 0, 1, 0, 0],
  [0, 0, 0, 605,423,415, 0, 0, 0, 0, 1, 0],
  [0, 0, 0, 0, 0, 0, 605,423,415, 0, 0, 1],
  [515,917,-361, 0, 0, 0, 0, 0, 0, 1, 0, 0],
  [0, 0, 0, 515,917,-361, 0, 0, 0, 0, 1, 0],
  [0, 0, 0, 0, 0, 0, 515,917,-361, 0, 0, 1],
  [-336,658,858, 0, 0, 0, 0, 0, 0, 1, 0, 0],
  [0, 0, 0, -336,658,858, 0, 0, 0, 0, 1, 0],
  [0, 0, 0, 0, 0, 0, -336,658,858, 0, 0, 1],
], dtype=np.int32)

scanner_0_vector = np.array([
  -618,
  -824,
  -621,
  -537,
  -823,
  -458,
  -447,
  -329,
  318,
  404,
  -588,
  -901,
], dtype=np.int32)

def get_transformation_matrix():
  inv = np.linalg.inv(scanner_1_matrix)
  vec = np.rint(np.dot(inv, scanner_0_vector)).astype(int)
  transformation_matrix = vec[:9].reshape((3, 3))
  translation_vector = vec[9:]
  return transformation_matrix, translation_vector

transformation_matrix = np.array([
  [-1, 0, 0],
  [0, 1, 0],
  [0, 0, -1],
], dtype=np.int32)

translation_vector = np.array([
  68,
  -1246,
  -43,
])

def test_transform(vec):
  return np.dot(transformation_matrix, vec) + translation_vector