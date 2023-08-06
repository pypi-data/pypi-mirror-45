'Regex helpers.'

import re
from io import StringIO
from clav.hash import hashf, hashs
from clav.os.fs import dump

def subf(pat, rep, file, count=0, flags=0):
  'Replace a pattern in a file.'

  with open(file) as _:
    data, cnt = re.subn(pat, rep, _.read(), count=count, flags=flags)
  if hashs(data) == hashf(file):
    cnt = 0
  else:
    with open(file, 'w') as _:
      _.write(data)
  return cnt

def sublinef(pat, rep, file, count=0, flags=0):
  'Replace a pattern in each line of a file.'

  cnt = 0
  lines = []
  with open(file) as _:
    for line in _:
      line, c = re.subn(pat, rep, line.rstrip(), count=count, flags=flags)
      lines.append(line)
      cnt += c
  lines = '\n'.join(lines)
  if hashs(lines) == hashf(file):
    cnt = 0
  else:
    with open(file, 'w') as _:
      _.write(lines)
  return cnt

def sublines(pat, rep, data, count=0, flags=0):
  'Replace a pattern in each line of a string.'

  cnt = 0
  lines = []
  with StringIO(data) as _:
    for line in _:
      line, c = re.subn(pat, rep, line.rstrip(), count=count, flags=flags)
      lines.append(line)
      cnt += c
  return '\n'.join(lines), cnt

re_flags = (
  'A', 'ASCII', 'DEBUG', 'I', 'IGNORECASE', 'L', 'LOCALE', 'M', 'MULTILINE',
  'S', 'DOTALL', 'X', 'VERBOSE'
)

for flag in re_flags:
  for fn in subf, sublinef:
    setattr(fn, flag, getattr(re, flag))
