from __future__ import annotations
from typing import Dict, List
import re

CD_RE = re.compile(r"\$ cd (?P<arg>\S+)")
LS_RE = re.compile(r"\$ ls")
DIR_RE = re.compile(r"dir (?P<name>\w+)")
FILE_RE = re.compile(r"(?P<size>\d+) (?P<name>\S+)")

class Directory:
  def __init__(
    self,
    name: str,
    parent: Directory,
    fs: Filesystem,
  ):
    self.name = name
    self.parent = parent
    self.fs = fs
    self.files: List[File] = []
    self.children: Dict[str, Directory] = {}
    self.size: int = None

  def parse_ls_row(self, row: str):
    if DIR_RE.match(row):
      m = DIR_RE.match(row)
      dir = Directory(m['name'], self, self.fs)
      self.children[m['name']] = dir
      self.fs.all_dirs.append(dir)
    else:
      m = FILE_RE.match(row)
      assert m
      self.files.append(File(int(m['size']), m['name'], self))

  def get_size(self):
    if not self.size:
      self.size = sum(file.size for file in self.files) + sum(dir.get_size() for dir in self.children.values())
    return self.size

class File:
  def __init__(
    self,
    size: int,
    name: str,
    dir: Directory,
  ):
    self.size = size
    self.name = name
    self.dir = dir

class Filesystem:
  def __init__(self):
    self.outermost_dir = Directory('/', None, self)
    self.all_dirs: List[Directory] = [self.outermost_dir]
    self.pwd: Directory = None

  def parse_row(self, row: str):
    if CD_RE.match(row):
      arg = CD_RE.match(row)['arg']
      if arg == '/':
        self.pwd = self.outermost_dir
      else:
        assert self.pwd
        if arg == '..':
          self.pwd = self.pwd.parent
        else:
          self.pwd = self.pwd.children[arg]
    elif LS_RE.match(row):
      assert self.pwd
    else:
      self.pwd.parse_ls_row(row)

  def sum_of_dirs_of_max_size(self, max_size: int = 100000) -> int:
    dir_sizes = [dir.get_size() for dir in self.all_dirs]
    return sum(size for size in dir_sizes if not max_size or size <= max_size)

  def size_of_smallest_sufficient(
    self,
    total_disk_space: int = 70000000,
    unused_required: int =  30000000,
  ) -> int:
    total_used = self.outermost_dir.get_size()
    space_required = total_used - (total_disk_space - unused_required)
    dir_sizes = [dir.get_size() for dir in self.all_dirs]
    dir_sizes.sort()
    for dir_size in dir_sizes:
      if dir_size >= space_required:
        return dir_size

def parse_input(filename: str) -> fs:
  fs = Filesystem()
  with open(filename) as f:
    for l in f:
      fs.parse_row(l.rstrip())
  return fs

if __name__ == '__main__':
  fs = parse_input('input/input.txt')
  print(fs.sum_of_dirs_of_max_size())
  print(fs.size_of_smallest_sufficient())