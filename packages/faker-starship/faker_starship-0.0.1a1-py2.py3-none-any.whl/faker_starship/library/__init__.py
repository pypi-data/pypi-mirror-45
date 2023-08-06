"""Library of starship data from various sources."""

import pkgutil

# Dynamically load all sibling modules, assuming each is a source.
source_names = []
__mypath = pkgutil.extend_path(__path__, __name__)
for _, module_name, __ in pkgutil.iter_modules(path=__mypath):
    __import__(__name__ + "." + module_name)
    source_names.append(module_name)

names = set()
classes = set()
registries = set()

for name in source_names:
    _module = globals().get(name)
    if hasattr(_module, "names"):
        names = names.union(_module.names)
    if hasattr(_module, "classes"):
        classes = classes.union(_module.classes)
    if hasattr(_module, "registries"):
        registries = registries.union(_module.registries)
