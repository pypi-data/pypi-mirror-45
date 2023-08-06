import logging
import os
import re
from collections import namedtuple
from subprocess import Popen, PIPE
from clav.os.run import run
from clav.os.fs import which

Package = namedtuple(
  'Package',
  ['state', 'name', 'upstream_version', 'package_version', 'arch', 'desc'],
)

def make_package(spec):
  _ = Package.rexp.match(spec)
  if _ is None:
    raise ValueError(f'Failed parsing spec: {spec}')
  return Package(
    _[1],
    _[2].split(':')[0] if ':' in _[2] else _[2],
    _[3].rsplit('-', 1)[0] if '-' in _[3] else _[3],
    _[3].rsplit('-', 1)[1] if '-' in _[3] else _[3],
    _[4],
    _[5],
  )

Package.rexp = re.compile('(\w+)\s+([-.:+a-zA-Z0-9]+)\s+([^ ]+)\s+([a-z0-9]+)\s*(.*)')
Package.make = make_package

class Apt:
  'Apt front-end.'

  def __init__(self):
    super().__init__()
    self.log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

  def __iter__(self):
    return self.installed.__iter__()

  def __contains__(self, package):
    package = package.split(':')[0]
    return any(_ for _ in self if _.name == package)

  def __getitem__(self, package):
    package = package.split(':')[0]
    return [_ for _ in self if _.name == package]

  def get_env(self):
    env = os.environ.copy()
    env['DEBIAN_FRONTEND'] = 'noninteractive'
    return env

  def aptget(self, args):
    'Run apt-get.'

    cmd = ['apt-get']
    cmd.append(args)
    cmd = ' '.join(cmd)
    self.log.debug(cmd)
    with run.quash():
      with run.unhook():
        return run(cmd, env=self.env)

  def apt(self, args):
    'Run apt.'

    cmd = ['apt']
    cmd.append(args)
    cmd = ' '.join(cmd)
    self.log.debug(cmd)
    with run.unhook():
      return run(cmd, env=self.env)

  def dpkg(self, args):
    'Run dpkg.'

    cmd = ['dpkg']
    cmd.append(args)
    cmd = ' '.join(cmd)
    self.log.debug(cmd)
    with run.unhook():
      return run(cmd, env=self.env)

  def get_installed(self):
    'Return the list of all installed packages.'

    self.log.debug('Build installed package list')
    argv = 'dpkg -l'.split()
    p = Popen(argv, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    for _ in range(5):
      p.stdout.readline()
    packages = [Package.make(_.rstrip()) for _ in p.stdout]
    return packages

  def update(self):
    'Update package cache.'

    self.log.debug('Updating apt package cache')
    with run.quash():
      res = self.aptget('-y update')
    if res.code != 0:
      self.log.warn(f'Update exited with status {res.code}')
    return True

  def install(self, packages, upgrade=False):
    '''
    Install packages.

    :param [str, list] packages: packages to install as str or list of str
    :param bool upgrade: if False, ignore packages that are already installed.
      if true, attempt to upgrade packages that are already installed.
    :returns: True if packages were installed or upgraded, else False
    :rtype bool:
    '''
    if not packages:
      raise ValueError('Called with empty package list')
    log = self.log
    if isinstance(packages, str):
      packages = [packages]
    if upgrade:
      log.debug(f'Installing {len(packages)} packages')
      log.debug(f'Installing: {packages}')
    else:
      installed = {_.name: True for _ in self}
      missing = [_ for _ in packages if _.split(':')[0] not in installed]
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
    self.aptget(args)
    return True

  def remove(self, packages, purge=True):
    '''
    Remove packages.

    :param [str, list] packages: packages to remove as str or list of str
    :param bool purge: if True, include the --purge flag
    :returns: True if packages were removed, else False
    :rtype bool:
    '''
    if not packages:
      raise ValueError('Called with empty package list')
    log = self.log
    if isinstance(packages, str):
      packages = [packages]
    installed = {_.name: True for _ in self}
    removing = [_ for _ in packages if _.split(':')[0] in installed]
    args = (len(removing), len(packages))
    log.info('Removing {} installed of {} requested packages'.format(*args))
    if len(removing) == 0:
      return False
    log.debug('Purging' if purge else 'Not purging')
    log.debug(f'Removing: {removing}')
    log.debug(f'Requested: {packages}')
    args = ['-y remove']
    args.append('--purge') if purge else None
    args.extend(removing)
    args = ' '.join(args)
    self.aptget(args)
    return True

  def upgrade(self):
    'Perform a dist-upgrade.'

    self.aptget('-yu dist-upgrade')

  def package(self, paths):
    '''
    Install .deb files.

    :param str path: path to .deb file as str
    '''
    if isinstance(paths, str):
      paths = [paths]
    args = [f'-y install']
    args.extend(paths)
    args = ' '.join(args)
    if which('apt'):
      # use apt when available as it will auto-install a .deb's dependencies
      self.log.info('Installing debs with apt')
      self.apt(args)
    else:
      self.log.info('Installing debs with apt-get')
      with run.quash():
        res = self.aptget(args)
      # try -f install in case .deb failed to install due to missing
      # dependencies
      if res.code != 0:
        self.log.debug('Fixing install with apt-get -f install')
        self.aptget('-yf install')
    return True

  env = property(get_env)
  installed = property(get_installed)

apt = Apt()
