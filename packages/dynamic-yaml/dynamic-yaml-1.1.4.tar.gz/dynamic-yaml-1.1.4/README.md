[![Build Status](https://travis-ci.org/childsish/dynamic-yaml.svg?branch=master)](https://travis-ci.org/childsish/dynamic-yaml)

dynamic-yaml
============

Dynamic YAML is a couple of classes and functions that add extra functionality to YAML that turns it into a great configuration language for Python. If you prefer JSON, then see [dynamic-json][dynamic-json].

YAML already provides:

* A very readable and clean syntax
* Infinitely nestable key:value pairs
* Sequence types
* A regulated portable syntax that conforms to strict standards

In addition, the PyYAML parser provides:

* Automatic type identification (a result of implementing the YAML standard)

Finally, the classes introduced by Dynamic YAML enable:

* Dynamic string resolution

Dynamic PyYAML requires PyYAML (https://bitbucket.org/xi/pyyaml).

Usage
-----
The key feature that was introduced is the ability for a string scalar to reference other parts of the configuration tree. This is done using the Python string formatting syntax. The characters '{' and '}' enclose a reference to another entry in the configuration structure. The reference takes the form key1.key2 where key1 maps to another mapping object and can be found in the root mapping, and key2 can be found in key1's mapping object. Multiple levels of nesting can be used (eg. key1.key2.key3 etc...).

An example yaml configuration:
```yaml
project_name: hello-world
dirs:
    home: /home/user
    venv: "{dirs.home}/venvs/{project_name}"
    bin: "{dirs.venv}/bin"
    data: "{dirs.venv}/data"
    errors: "{dirs.data}/errors"
    sessions: "{dirs.data}/sessions"
    databases: "{dirs.data}/databases"
exes:
    main: "{dirs.bin}/main"
    test: tests
```

Reading in a yaml file:

```python
import dynamic_yaml

with open('/path/to/file.yaml') as fileobj:
    cfg = dynamic_yaml.load(fileobj)
```

Now, the entry `cfg.dirs.venv` will resolve to `"/home/user/venvs/hello-world"`.

Installation
------------

To install, simply run:

```bash
pip install git+https://github.com/childsish/dynamic-yaml
```

Restrictions
------------

Due to the short amount of time I was willing to spend on working upon this, there are a few restrictions required for a valid YAML configuration file.

* **Wild card strings must be surrounded by quotes.** Braces ('{' and '}') in a YAML file usually enclose a mapping object. However, braces are also used by the Python string formatting syntax to enclose a reference. As there is no way to change either of these easily, strings that contain wildcards must be explicitly declared using single or double quotes to enclose them.
* **Variables are always dynamically resolved.** This possibly introduces significant slow downs, but hopefully your configuration object isn't too big anyway.

[dynamic-json]: https://github.com/childsish/dynamic-json
