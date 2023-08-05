import random

from .models import Namespace, db

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
        if Namespace.get_or_none(uid='core') is None:
            Namespace.create(
                uid='core',
                name='Drongo',
                description='Core namespace for the drongo ecosystem.',
                modules=[],
                _ns='core',
                is_active=True
            )


class NamespaceCreate(NSServiceBase):
    def __init__(self, name, description, is_active=False):
        self.name = name
        self.description = description
        self.is_active = is_active

    def call(self, ns='core'):
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
        return Namespace.get_or_none(
            uid=self.uid,
            _ns=ns)


class NamespaceActivate(NSServiceBase):
    def __init__(self, uid):
        self.uid = uid

    def call(self, ns='core'):
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
        ns = Namespace.get_or_none(uid=self.uid, _ns=ns)
        if ns is not None:
            ns.del_inst()


class NamespaceList(NSServiceBase):
    def __init__(self, active_only=False, page_number=1, page_size=50):
        self.active_only = active_only
        self.page_number = page_number
        self.page_size = page_size

    def call(self, ns='core'):
        q = Namespace.sel().where(Namespace._ns == ns)
        if self.active_only:
            q = q.where(Namespace.is_active == True)  # noqa: E712
        return q.count(), q.paginate(self.page_number, self.page_size)


class NamespaceListModules(NSServiceBase):
    def __init__(self, uid):
        self.uid = uid

    def call(self, ns='core'):
        ns = Namespace.get_or_none(uid=self.uid, _ns=ns)
        if ns is not None:
            return ns.modules

        return []


class NamespaceAddModule(NSServiceBase):
    def __init__(self, uid, module):
        self.uid = uid
        self.module = module

    def call(self, ns='core'):
        ns = Namespace.get_or_none(uid=self.uid, _ns=ns)
        if ns is not None:
            if ns.modules is None:
                ns.modules = []
                ns.save()
            if self.module not in ns.modules:
                ns.modules.append(self.module)
                ns.save()
            return True
        return False


class NamespaceDeleteModule(NSServiceBase):
    def __init__(self, uid, module):
        self.uid = uid
        self.module = module

    def call(self, ns='core'):
        ns = Namespace.get_or_none(uid=self.uid, _ns=ns)
        if ns is not None:
            if self.module in ns.modules:
                ns.modules.remove(self.module)
                ns.save()
            return True
        return False
