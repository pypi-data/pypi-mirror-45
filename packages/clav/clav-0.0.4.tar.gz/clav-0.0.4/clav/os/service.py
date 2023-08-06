import logging
from abc import abstractmethod
from .run import run

class ServiceManager:
  'Service manager base class.'

  # list of actions to treat as commands, e.g. start, stop, reload, enable
  # commands will raise with non-zero exit code
  commands = ()

  # list of actions to treat as queries, e.g. status, is-enabled, list-units
  # queries will not raise with non-zero exit code
  queries = ()

  def __init__(self):
    super().__init__()
    cls = self.__class__
    self.log = logging.getLogger(f'{cls.__module__}.{cls.__name__}')

  def __getattr__(self, action):
    'Return a function that will run the requested action.'

    if action in self.commands:
      return self.make_command(action)
    elif action in self.queries:
      return self.make_query(action)
    else:
      raise ValueError(f'Invalid action: {action}')

  @abstractmethod
  def run(self, action, args):
    'Invoke the service manager.'

    pass

  def make_command(self, action):
    'Return a function that will invoke action as a command.'

    def run_command(args):
      return self.run(action, args)
    return run_command

  def make_query(self, action):
    'Return a function that will invoke action as a query.'

    def run_query(args):
      with run.quash():
        return self.run(action, args)
    return run_query

  def start_or_restart(self, name):
    'Start a service if not started, else restart.'

    if self.status(name).code == 0:
      self.restart(name)
    else:
      self.start(name)

  def start_or_reload(self, name):
    'Start a service if not started, else reload.'

    if self.status(name).code == 0:
      self.reload(name)
    else:
      self.start(name)

  def start_if_stopped(self, name):
    '''
    Start a service if stopped.'

    :returns: True if the service was started.
    :rtype bool:
    '''

    if self.status(name).code != 0:
      self.start(name)
      return True
    return False

  def stop_if_started(self, name):
    '''
    Stop a service if started.

    :returns: True if the service was stopped
    :rtype bool:
    '''

    if self.status(name).code == 0:
      self.stop(name)
      return True
    return False

class Systemctl(ServiceManager):
  'Front-end for systemctl.'

  commands = (
    # Unit
    'start',
    'stop',
    'reload',
    'restart',
    'try-restart',
    'reload-or-restart',
    'try-reload-or-restart',
    'isolate',
    'kill',
    'set-property',
    'reset-failed',
    # Unit files
    'enable',
    'disable',
    'reenable',
    'preset',
    'preset-all',
    'mask',
    'unmask',
    'link',
    'revert',
    'add-wants',
    'add-requires',
    'set-default',
    # Job
    'cancel',
    # Environment
    'set-environment',
    'unset-environment',
    'import-environment',
    # Manager
    'daemon-reload',
    'daemon-reexec',
    # System
    'default',
    'rescue',
    'emergency',
    'halt',
    'poweroff',
    'reboot',
    'kexec',
    'exit',
    'switch-root',
    'suspend',
    'hibernate',
    'hybrid-sleep',
    'suspend-then-hibernate',
  )

  queries = (
    # Unit
    'list-units',
    'list-sockets',
    'list-timers',
    'is-active',
    'is-failed',
    'status',
    'show',
    'cat',
    'list-dependencies',
    # Unit files
    'list-unit-files',
    'is-enabled',
    'get-default',
    # Machine
    'list-machines',
    # Job
    'list-jobs',
    # Environment
    'show-environment',
    # System
    'is-system-running',
  )

  def __init__(self):
    super().__init__()

  def __getattr__(self, action):
    action = action.replace('_', '-')
    return super().__getattr__(action)

  def run(self, action, args):
    cmd = f'systemctl {action} {args}'
    self.log.debug(cmd)
    return run(cmd)

  def enable_if_not_enabled(self, service):
    if not self.is_enabled(service):
      self.enable(service)
      return True
    return False

systemctl = Systemctl()

class Initd(ServiceManager):
  'Wrapper for sysvinit.'

  commands = (
    'stop',
    'start',
    'restart',
    'reload',
  )

  queries = (
    'status',
  )

  def __init__(self):
    super().__init__()

  def __getattr__(self, action):
    # since there is no standard list of actions supported by init scripts,
    # support unknown actions (e.g. configtest), but don't raise exceptions
    # if they exit with non-zero status
    try:
      return super().__getattr__(action)
    except ValueError as ex:
      if 'Invalid action:' not in ex.args[0]:
        raise
    return self.make_unknown(action)

  def make_unknown(self, action):
    def run_unknown(args):
      with run.quash():
        return self.run(action, args)
    return run_unknown

  def run(self, action, args):
    cmd = f'/etc/init.d/{args} {action}'
    self.log.debug(cmd)
    return run(cmd)

initd = Initd()
