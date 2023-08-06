[![Build Status](https://travis-ci.org/simontorres/simple-version-manager.svg?branch=master)](https://travis-ci.org/simontorres/simple-version-manager)
[![Coverage Status](https://coveralls.io/repos/github/simontorres/simple-version-manager/badge.svg?branch=master)](https://coveralls.io/github/simontorres/simple-version-manager?branch=master)
# Simplify version management

The idea behind the development of this small tool is to simplify the process
of increasing your version number. It is designed to work with a specific format
explained below.

## Version format supported

There are countless ways of handling your versions and there is no _right_ or 
_wrong_ way. The format I choose is  the following:

```
major.minor.patch.devN
```

Some examples in no particular order

```
0.0.1
1.1.1.dev1
30.1.1.dev5
```


## Usage
Please note that this will depend on the size of your team and complexity of the
project. Either way if the team is large there will be a manager that should 
control when the version is updated so in principle is the same for a large or 
even a one-person team. Here are some examples:

- You should use this program with `--dev` argument right after you pulled the
  latest changes from upstream

- You can use `--patch`, `--minor` or `--major` in combination with `--release`
  when you want to create a new release.

- Also you have the freedom of updating any of the fields independently


## Options
The argument options are better explained with examples. Let's say we currently are
working on version `1.2.3.dev4`

 - ``--dev`` will increase the development version by one leaving you with 
   `1.2.3.dev5`
 - ``--patch`` will give you `1.2.4.dev1` notice that the development version 
   is dropped back to one
 - ``--minor`` will change the version to `1.3.0.dev1` notice now that not only
   _dev_ is dropped to one but also the patch count drops to zero.
 - ``--major`` will change version to `2.0.0.dev1` which is the same as 
   `--minor` plus dropping _minor_ to zero.
 - ``--release`` will remove the `devN` part leaving you with `1.2.3`. `--release`
   can be used in combination of other options.
 - ``--set`` Let you set the version to any value.
 
 If you start from a _stable_ version like `2.0.0` you should use the `--dev` 
 argument that will increase the patch number and add the _dev1_ string. `2.0.1.dev1`


# References

- [distutils.version.LooseVersion](http://epydoc.sourceforge.net/stdlib/distutils.version.LooseVersion-class.html)
- [Semantic Version](https://semver.org/) (Not used here but a good reference on version numbering)
