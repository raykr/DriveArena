class Registry:
    def __init__(self, name):
        self.name = name
        self._module_dict = {}

    def get(self, key):
        return self._module_dict[key]

    def _register(self, module, name=None):
        module_name = name or module.__name__
        self._module_dict[module_name] = module
        return module

    def register(self, module=None, name=None):
        if module is not None:
            return self._register(module, name=name)

        def _decorator(fn_or_cls):
            return self._register(fn_or_cls, name=name)

        return _decorator

    register_module = register


ARCH_REGISTRY = Registry("arch")
MODEL_REGISTRY = Registry("model")
