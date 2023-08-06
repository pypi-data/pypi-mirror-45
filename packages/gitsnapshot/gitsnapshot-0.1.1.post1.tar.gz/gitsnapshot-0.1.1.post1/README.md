# gitsnapshot

[![Build Status](https://travis-ci.org/kirillsulim/gitsnapshot.svg?branch=master)](https://travis-ci.org/kirillsulim/gitsnapshot)
[![PyPI version](https://badge.fury.io/py/gitsnapshot.svg)](https://badge.fury.io/py/gitsnapshot)

A simple library to load snapshots of git repository.

## Usage

To load git repository call `load_repo` as follows:

```python
from gitsnapshot import load_repo

load_repo('~/target/directory', 'git@github.com/test/repo')
```

This code creates folder `~/target/directory` if this folder doesn't exists, and then
clone shallow copy of repository `git@github.com/test/repo`. 
By default this function loads current `master` branch.

To load another branch (i.e. `develop`) pass branch name in `branch` parameter:

```python
from gitsnapshot import load_repo

load_repo('~/target/directory', 'git@github.com/test/repo', branch='develop')
``` 

Also you can load snapshot by tag:

```python
from gitsnapshot import load_repo

load_repo('~/target/directory', 'git@github.com/test/repo', tag='v0.1.2')
```

Or by commit hash:

```python
from gitsnapshot import load_repo

load_repo('~/target/directory', 'git@github.com/test/repo', commit='abcdef')
```

## Errors

`load_repo` function return optional string with error description.
If `load_repo` returned `None` then no errors was happened.

## Reusing of directory

If you try to load repository snapshot into existing directory with another snapshot 
of the same repository, `load_repo` will return error. 
To avoid this behavior pass `use_existing=True` as argument.

```python
from gitsnapshot import load_repo

load_repo('~/target/directory', 'git@github.com/test/repo', use_existing=True)
```

In this case `load_repo` will load repository index and will checkout to specified 
branch, tag or commit.
