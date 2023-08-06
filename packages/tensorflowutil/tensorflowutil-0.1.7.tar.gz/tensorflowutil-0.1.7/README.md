# Tensorflow utility package 

- installs and imports tensorflow
- will expose several utility api that can be used commonly in multiple other machine learning and tensorflow specific projects.

### Push to the main PYPI server:

Build source (and/or wheel distribution using setup tools)

Optionally: `$make clean`

```bash
$ make distribution
```

Upload to the main pypi server using `twine`:

```bash
$ make upload
```

Install package using the main PYPI server (beware of caching problem)

```bash
$ make pip-install
```

OR

```bash
$ pip install tensorflowutil==CURRENT_VERSION
```

### Installation verification

Finally, verify installation using the exposed entry point:

```bash
$ tfutil --version
```

Should print something like:

```
Package: tensorflowutil 
Version: 0.1.5
```

## Using test server
Push to test server: `--repository-url https://test.pypi.org/legacy`, then:

```
$ pip install -i https://test.pypi.org/simple/ tensorflowutil
```

Expected Error: because `tensorflow==1.13.1` is not installed in the test pypi server.

> ERROR: Could not find a version that satisfies the requirement tensorflow==1.13.1 
> (from versions: 0.12.1, 2.0.0a0)
> ERROR: No matching distribution found for tensorflow==1.13.1


## Notes
- Read version information to be used appropriately in a source distribution.
  - environment variable approach isn't a very good idea
  - [A few good suggestions here.](https://stackoverflow.com/questions/2058802/how-can-i-get-the-version-defined-in-setup-py-setuptools-in-my-package)
  
## Limitations
- GPU support?

# License
> Please refer to LICENSE file for detail.
