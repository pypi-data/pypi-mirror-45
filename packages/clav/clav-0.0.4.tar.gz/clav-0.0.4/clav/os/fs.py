import os
import shutil
import stat
from clav.hash import hashf, hashs
from clav.os.run import run

which = shutil.which

def filemode(path, mode=None):
  def get():
    s = os.stat(path)
    return oct(s[stat.ST_MODE])[-4:]
  def set():
    assert(isinstance(mode, str))
    if get().endswith(mode):
      return False
    run(f'chmod {mode} {path}')
    return True
  return get() if mode is None else set()

def fext(file):
  'Return the extension for ``file`` or ``None``.'

  ext = os.path.splitext(file)[1][1:]
  return ext.lower() if ext else None

def fname(file):
  'Return the filename without extension of ``file``.'

  return file.split('.')[-1]

def backuponce(src, ext='dist'):
  '''
  Create a backup file if one doesn't already exist.

  :param str src: source file path
  :param str ext: backup file extension
  :returns: True if the file was backed up
  :rtype bool:
  '''

  dst = f'{src}.{ext}'
  if os.path.isfile(dst):
    return False
  shutil.copyfile(src, dst)
  return True

def slurp(path, encoding='utf-8'):
  with open(path, encoding=encoding) as fd:
    return fd.read()

def dump(path, buf, mode='w', encoding='utf-8'):
  '''
  Dump a buffer to a file. If the file exits and its contents are identical to
  the contents of the buffer, no action is taken.

  :param str path: path to receive dump
  :param str buf: data to dump
  :param str mode: file open mode
  :param str encoding: character encoding
  :returns: True if the file was update
  :rtype bool:
  '''
  if os.path.isfile(path) and hashf(path) == hashs(buf):
    return False
  with open(path, mode, encoding=encoding) as fd:
    fd.write(buf)
    fd.flush()
  return True

def ln(src, dst, hard=False):
  if hard:
    raise NotImplementedError('Hard links not implemented')
  if os.path.islink(dst):
    if os.path.abspath(os.readlink(dst)) == os.path.abspath(src):
      return False
    os.unlink(dst)
  run(f'ln -s {src} {dst}')
  return True

def mkdir(path, p=False):
  if os.path.isdir(path):
    return False
  args = '-p' if p else ''
  run(f'mkdir {args} {path}')
  return True

def rm(path, r=False, f=False):
  assert(path != '/')
  assert(not (os.getcwd() == '/' and path == '*'))
  args = ''
  args += 'r' if r else ''
  args += 'f' if f else ''
  args = f'-{args}' if args else ''
  run(f'rm {args} {path}')
  return True

def cp(src, dst, r=False, f=False, p=False):
  args = ''
  args += 'r' if r else ''
  args += 'f' if f else ''
  args += 'p' if p else ''
  args = f'-{args}' if args else ''
  run(f'cp {args} {src} {dst}')
  return True
