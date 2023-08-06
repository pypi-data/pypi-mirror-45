import grp
import os
import pwd
from clav.data import attr
from clav.os.run import run

class Users:

  def __init__(self):
    super().__init__()

  def __iter__(self):
    return pwd.getpwall().__iter__()

  def __len__(self):
    return len(pwd.getpwall())

  def __contains__(self, username):
    if isinstance(username, int):
      return any(_.pw_uid == username for _ in self)
    else:
      return any(_.pw_name == username for _ in self)

  def __getitem__(self, username):
    if isinstance(username, int):
      return {_.pw_uid: _ for _ in self}[username]
    else:
      return {_.pw_name: _ for _ in self}[username]

  def _run(self, cmd, name, **kw):
    'Build command lines for useradd or usermod.'

    kw = attr(kw)
    args = [cmd]
    def addarg(name, value=None):
      args.append(name)
      if value is not None:
        args.append(value)
    addarg('-a') if kw.get('append') == True else None
    addarg('-c', kw.comment) if 'comment' in kw else None
    addarg('-d', kw.home) if 'home' in kw else None
    addarg('-e', kw.expire) if 'expire' in kw else None
    if 'groups' in kw:
      _ = kw.groups
      addarg('-G', _ if isinstance(_, str) else ','.join(_))
    addarg('-g', kw.group) if 'group' in kw else None
    addarg('-m') if kw.get('create') == True else None
    addarg('-p', kw.password) if 'password' in kw else None
    addarg('-r') if kw.get('system') == True else None
    addarg('-s', kw.shell) if 'shell' in kw else None
    addarg('-u', kw.uid) if 'uid' in kw else None
    args.append(name)
    run(args)

  def add(self, name, **kw):
    '''
    Add a user.

    required arguments:

    :param str name: username

    optional keyword arguments:

    :param str comment: user comment
    :param str home: user home directory
    :param str expire: user login expiration
    :param [list, str] groups: groups as list of str or comma-delimited str
    :param str group: primary group
    :param bool create: create home directory from skel
    :param str password: crypt()ed user password
    :param bool system: create as system user
    :param str shell: user shell
    :param int uid: user: user id
    '''
    self._run('useradd', name, **kw)

  create = add

  def update(self, name, **kw):
    '''
    Update a user.

    required arguments:

    :param str name: username

    optional keyword arguments:

    :param str comment: user comment
    :param str home: user home directory
    :param str expire: user login expiration
    :param bool append: append or replace for ``groups`` keyword
    :param [list, str] groups: groups as list of str or comma-delimited str
    :param str group: primary group
    :param bool create: create home directory from skel
    :param str password: crypt()ed user password
    :param bool system: create as system user
    :param str shell: user shell
    :param int uid: user: user id
    '''
    self._run('usermod', name, **kw)

  def remove(self, name, force=False, remove=False):
    '''
    Remove a user.

    required arguments:

    :param str name: username

    optional keyword arguments:

    :param bool force: force removal of user, even if logged in
    :param bool remove: remove user home directory and mail spool
    '''
    args = ['userdel']
    args.append('-f') if force else None
    args.append('-r') if remove else None
    args.append(name)
    run(args)

  delete = remove

  def get_groups_for_user(self, user):
    return [_.gr_name for _ in grp.getgrall() if user in _.gr_mem]

  def add_user_to_group(self, user, group):
    if group in self.get_groups_for_user(user):
      return 0
    self.update(user, append=True, groups=group)
    return 1

  def remove_user_from_group(self, user, group):
    groups = self.get_groups_for_user(user)
    if group not in groups:
      return 0
    groups.remove(group)
    self.update(user, groups=groups)
    return 1

  def get_username(self):
    'Return the name of the executing user.'

    return pwd.getpwuid(os.getuid())[0]

  def get_uid(self):
    'Return the uid of the executing user.'

    return os.getuid()

  username = property(get_username)
  uid = property(get_uid)

users = Users()

class Groups:

  def __init__(self):
    super().__init__()

  def __iter__(self):
    return grp.getgrall().__iter__()

  def __len__(self):
    return len(grp.getgrall())

  def __contains__(self, groupname):
    if isinstance(groupname, int):
      return any(_.gr_gid == groupname for _ in self)
    else:
      return any(_.gr_name == groupname for _ in self)

  def __getitem__(self, groupname):
    if isinstance(groupname, int):
      return {_.gr_gid: _ for _ in self}[groupname]
    else:
      return {_.gr_name: _ for _ in self}[groupname]

  def add(self, name, gid=None, password=None, system=None):
    raise NotImplementedError('group add not implemented D:')

  def update(self, name=None, gid=None, password=None, system=None):
    raise NotImplementedError('group update not implemented D:')

  def remove(self, name=None, gid=None):
    raise NotImplementedError('group remove not implemented D:')

  def get_group_name(self):
    'Return the name of the executing group.'

    return grp.getgrgid(os.getgid())[0]

  def get_gid(self):
    'Return the gid of the executing group.'

    return os.getgid()

  group_name = property(get_group_name)
  gid = property(get_gid)

groups = Groups()
