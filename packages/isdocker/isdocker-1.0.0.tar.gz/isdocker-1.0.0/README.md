## isDocker [![pipeline status](https://gitlab.com/yoginth/isdocker/badges/master/pipeline.svg)](https://gitlab.com/yoginth/isdocker/commits/master)

> Check if the process is running inside a Docker container

## Demo

Demo on [Repl.it](https://repl.it/@yoginth/isdocker)

## Install

```
$ pip install isdocker
```

## Usage

```python
from isdocker import isDocker

if (isDocker()):
    print('Running inside a Docker container');
else:
    print('Running outside the Docker container');
```

## License

[MIT][LICENSE] Yoginth

[LICENSE]: https://mit.yoginth.com
