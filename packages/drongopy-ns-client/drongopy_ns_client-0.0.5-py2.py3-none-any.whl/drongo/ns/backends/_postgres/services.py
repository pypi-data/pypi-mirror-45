import random

from .models import ModuleInstance, Namespace, db

_KEY_SET = 'qwertyuiopasdfghjklzxcvbnm1234567890'


def _generate_key(length=8):
    s = random.choice(_KEY_SET[:26])
    for i in range(length - 1):
        s += random.choice(_KEY_SET)
    return s


class NSServiceBase(object):
    @classmethod
    def init(cls, module):
        cls.module = module
        db.initialize(module.database.instance.get())

        module.database.instance.auto_migrate(Namespace)
        module.database.instance.auto_migrate(ModuleInstance)

        if Namespace.get_or_none(uid='core') is None:
            Namespace.create(
                uid='core',
                name='Drongo',
                description='Core namespace for the drongo ecosystem.',
                modules=[],
                _ns='core',
                is_active=True
            )

        if ModuleInstance.get_or_none(module='auth', uid='core') is None:
            ModuleInstance.create(
                module='auth',
                uid='core',
                name='Auth for Core',
                description='Authentication and Authorization for Core.',
                is_active=True,
                settings={},
                _ns='core'
            )

        cls._db = module.database.instance.get()

    def __enter__(self):
        self._db.connect(reuse_if_open=True)

    def __exit__(self, *args):
        self._db.close()


class NamespaceCreate(NSServiceBase):
    def __init__(self, name, description, is_active=False):
        self.name = name
        self.description = description
        self.is_active = is_active

    def call(self, ns='core'):
        with self:
            return Namespace.create(
                name=self.name,
                description=self.description,
                is_active=self.is_active,
                uid=_generate_key(8),
                _ns=ns
            )


class NamespaceGet(NSServiceBase):
    def __init__(self, uid):
        self.uid = uid

    def call(self, ns='core'):
        with self:
            return Namespace.get_or_none(
                uid=self.uid,
                _ns=ns)


class NamespaceActivate(NSServiceBase):
    def __init__(self, uid):
        self.uid = uid

    def call(self, ns='core'):
        with self:
            ns = Namespace.get_or_none(uid=self.uid, _ns=ns)
            if ns is not None:
                ns.is_active = True
                ns.save()
                return True
            return False


class NamespaceDeactivate(NSServiceBase):
    def __init__(self, uid):
        self.uid = uid

    def call(self, ns='core'):
        with self:
            ns = Namespace.get_or_none(uid=self.uid, _ns=ns)
            if ns is not None:
                ns.is_active = False
                ns.save()
                return True
            return False


class NamespaceUpdate(NSServiceBase):
    def __init__(self, uid, name=None, description=None):
        self.uid = uid
        self.name = name
        self.description = description

    def call(self, ns='core'):
        with self:
            ns = Namespace.get_or_none(uid=self.uid, _ns=ns)
            if ns is not None:
                ns.name = self.name or ns.name
                ns.description = self.description or ns.description
                ns.save()
                return True
            return False


class NamespaceDelete(NSServiceBase):
    def __init__(self, uid):
        self.uid = uid

    def call(self, ns='core'):
        with self:
            ns = Namespace.get_or_none(uid=self.uid, _ns=ns)
            if ns is not None:
                ns.del_inst()


class NamespaceList(NSServiceBase):
    def __init__(self, active_only=False, page_number=1, page_size=50):
        self.active_only = active_only
        self.page_number = page_number
        self.page_size = page_size

    def call(self, ns='core'):
        with self:
            q = Namespace.sel().where(Namespace._ns == ns)
            if self.active_only:
                q = q.where(Namespace.is_active == True)  # noqa: E712
            return q.count(), q.paginate(self.page_number, self.page_size)


class ModuleInstanceCreate(NSServiceBase):
    def __init__(self, module, name, description='',
                 is_active=False, settings={}):
        self.module = module
        self.name = name
        self.description = description
        self.is_active = is_active
        self.settings = settings

    def call(self, ns='core'):
        with self:
            return ModuleInstance.create(
                uid=_generate_key(8),
                module=self.module,
                name=self.name,
                description=self.description,
                is_active=self.is_active,
                settings=self.settings,
                _ns=ns
            )


class ModuleInstanceUpdate(NSServiceBase):
    def __init__(self, module, uid, name=None, description=None):
        self.module = module
        self.uid = uid
        self.name = name
        self.description = description

    def call(self, ns='core'):
        with self:
            mi = ModuleInstance.get_or_none(
                module=self.module, uid=self.uid,
                _ns=ns)
            if mi is not None:
                mi.name = self.name or mi.name
                mi.description = self.description or mi.description
                mi.save()
            return True


class ModuleInstanceActivate(NSServiceBase):
    def __init__(self, module, uid):
        self.module = module
        self.uid = uid

    def call(self, ns='core'):
        with self:
            mi = ModuleInstance.get_or_none(
                module=self.module, uid=self.uid, _ns=ns)
            if mi is not None:
                mi.is_active = True
                mi.save()
                return True
            return False


class ModuleInstanceDeactivate(NSServiceBase):
    def __init__(self, module, uid):
        self.module = module
        self.uid = uid

    def call(self, ns='core'):
        with self:
            mi = ModuleInstance.get_or_none(
                module=self.module, uid=self.uid, _ns=ns)
            if mi is not None:
                mi.is_active = False
                mi.save()
                return True
            return False


class ModuleInstanceDelete(NSServiceBase):
    def __init__(self, module, uid):
        self.module = module
        self.uid = uid

    def call(self, ns='core'):
        with self:
            mi = ModuleInstance.get_or_none(
                module=self.module, uid=self.uid, _ns=ns)
            if mi is not None:
                mi.del_inst()


class ModuleInstanceList(NSServiceBase):
    def __init__(self):
        pass

    def call(self, ns='core'):
        with self:
            return ModuleInstance.sel().filter(
                ModuleInstance._ns == ns).order_by(ModuleInstance.module)


class ModuleInstanceListInstances(NSServiceBase):
    def __init__(self, module):
        self.module = module

    def call(self, ns='core'):
        with self:
            return ModuleInstance.sel().filter(
                (ModuleInstance.module == self.module) &
                (ModuleInstance._ns == ns)
            )


class ModuleInstanceGet(NSServiceBase):
    def __init__(self, module, uid):
        self.module = module
        self.uid = uid

    def call(self, ns='core'):
        with self:
            return ModuleInstance.get_or_none(
                module=self.module, uid=self.uid,
                _ns=ns)


class ModuleInstanceGetSingletonSettings(NSServiceBase):
    def __init__(self, module):
        self.module = module

    def call(self, ns='core'):
        with self:
            return ModuleInstance.get_or_none(
                module=self.module, is_active=True, _ns=ns)


class ModuleInstanceGetSettings(NSServiceBase):
    def __init__(self, module, instance):
        self.module = module
        self.instance = instance

    def call(self, ns='core'):
        with self:
            return ModuleInstance.get_or_none(
                module=self.module, uid=self.instance, is_active=True, _ns=ns)


class ModuleInstanceUpdateSettings(NSServiceBase):
    def __init__(self, module, instance, settings):
        self.module = module
        self.instance = instance
        self.settings = settings

    def call(self, ns='core'):
        with self:
            mi = ModuleInstance.get_or_none(
                module=self.module, uid=self.instance, is_active=True, _ns=ns)
            if mi is not None:
                mi.settings = self.settings
                mi.save()
                return True

            return False
