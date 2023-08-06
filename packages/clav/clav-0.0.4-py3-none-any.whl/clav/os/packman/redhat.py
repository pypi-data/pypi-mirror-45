import logging
import re
from collections import namedtuple
from subprocess import Popen, PIPE
from clav.os.run import run

Package = namedtuple(
  'Package',
  ['name', 'upstream_version', 'package_version', 'arch', 'full_name'],
)

def make_package(spec):
  _ = Package.rexp1.match(spec)
  if _ is not None:
    return Package(_[1], _[2], _[3], _[4], spec)
  _ = Package.rexp2.match(spec)
  if _ is not None:
    return Package(_[1], _[2], _[3], None, spec)
  return Package(spec, None, None, None, spec)

Package.rexp1 = re.compile('([-_.+a-zA-Z0-9]+)-([.a-zA-Z0-9]+)-([.a-zA-Z0-9]+)\.([-_a-zA-Z0-9]+)')
Package.rexp2 = re.compile('([-_.+a-zA-Z0-9]+)-([.a-zA-Z0-9]+)-([.a-zA-Z0-9]+)')
Package.make = make_package

class Yum:

  def __init__(self):
    super().__init__()
    self.log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

  def __iter__(self):
    return self.installed.__iter__()

  def __contains__(self, package):
    return any(_ for _ in self if _.name == package or _.full_name == package)

  def __getitem__(self, package):
    return [_ for _ in self if package in (_.name, _.full_name)]

  def yum(self, args):
    'Run yum.'

    cmd = ['yum']
    cmd.append(args)
    cmd = ' '.join(cmd)
    self.log.debug(cmd)
    return run(cmd)

  def rpm(self, args):
    'Run rpm.'

    cmd = ['rpm']
    cmd.append(args)
    cmd = ' '.join(cmd)
    self.log.debug(cmd)
    return run(cmd)

  def get_installed(self):
    'Return the list of all installed packages.'

    self.log.debug('Building installed package list')
    argv = 'rpm -qa'.split()
    with Popen(argv, stdout=PIPE, stderr=PIPE, universal_newlines=True) as p:
      return [Package.make(_.rstrip()) for _ in p.stdout]

  def update(self):
    pass

  def install(self, packages, upgrade=False):
    if not packages:
      raise ValueError('Called with empty package list')
    log = self.log
    if isinstance(packages, str):
      packages = [packages]
    if upgrade:
      log.info(f'Installing{len(packages)} packages')
      log.debug(f'Installing: {packages}')
    else:
      installed = {_.name: True for _ in self}
      installed.update({_.full_name: True for _ in self})
      missing = [_ for _ in packages if _ not in installed]
      args = (len(missing), len(packages))
      log.info('Installing {} missing of {} requested packages'.format(*args))
      if len(missing) == 0:
        return False
      log.debug(f'Installing: {missing}')
      log.debug(f'Requested: {packages}')
      packages = missing
    args = ['-y install']
    args.extend(packages)
    args = ' '.join(args)
    self.yum(args)

  def remove(self, packages):
    if not packages:
      raise ValueError('Called with empty package list')
    log = self.log
    if isinstance(packages, str):
      packages = [packages]
    installed = {_.name: True for _ in self}
    installed.update({_.full_name: True for _ in self})
    removing = [_ for _ in packages if _ in installed]
    args = (len(removing), len(packages))
    log.info('Removing {} installed of {} requested packages'.format(*args))
    if len(removing) == 0:
      return False
    log.debug(f'Removing: {removing}')
    log.debug(f'Requested: {packages}')
    args = ['-y erase']
    args.extend(removing)
    args = ' '.join(args)
    self.yum(args)
    return True

  def upgrade(self):
    'Perform an update.'

    self.yum('-y update')

  def package(self, paths):
    if isinstance(paths, str):
      paths = [paths]
    args = [f'-y install']
    args.extend(paths)
    args = ' '.join(args)
    self.log.info('Installing rpm with yum')
    self.yum(args)
    return True

  installed = property(get_installed)

yum = Yum()
