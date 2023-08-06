class Apk:

  def __init__(self):
    super().__init__()

  def __iter__(self):
    raise NotImplementedError()

  def __contains__(self, package):
    raise NotImplementedError()

  def apk(self, args):
    raise NotImplementedError()

  def get_installed(self):
    raise NotImplementedError()

  def update(self):
    raise NotImplementedError()

  def install(self, packages, upgrade=False):
    raise NotImplementedError()

  def remove(self, packages):
    raise NotImplementedError()

  def upgrade(self):
    raise NotImplementedError()

  def package(self, paths):
    raise NotImplementedError()

  installed = property(get_installed)

apk = Apk()
