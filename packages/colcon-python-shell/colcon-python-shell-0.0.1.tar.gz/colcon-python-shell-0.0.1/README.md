# Colcon Python Shell

This is an extension to [colcon](https://colcon.readthedocs.io/en/released/) that makes things easier when working within a python shell. It extends `colcon build` so in addition to creating local_setup.sh/setup.sh files, it also creates `local_setup.py`/`setup_chain.py` files.

These files can be used to add a colcon prefix to an already-running python interpreter:
```
Python 3.6.7 (default, Oct 22 2018, 11:32:17) 
[GCC 8.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import os
>>> before = set(os.environ.items())
>>> import runpy
>>> _ = runpy.run_path('install/local_setup.py')
Activating Colcon prefix: /home/snuc/colcon_ws/install
  Running scripts for packages: colcon-python-shell, colcon-venv, keystroke
Colcon prefix activated
>>> after = set(os.environ.items())
>>> from pprint import pprint
>>> pprint(dict(after-before))
{'AMENT_PREFIX_PATH': '/home/snuc/colcon_ws/install/keystroke:',
 'PATH': '/home/snuc/colcon_ws/install/keystroke/bin:/home/snuc/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin',
 'PYTHONPATH': '/home/snuc/colcon_ws/install/keystroke/lib/python3.6/site-packages:/home/snuc/colcon_ws/install/colcon-venv/lib/python3.6/site-packages:/home/snuc/colcon_ws/install/colcon-python-shell/lib/python3.6/site-packages:'}
```
 
Or to start an interactive python interpreter with a colcon prefix:

```bash
python3 -i install/setup_local.py
```
```bash
python3 -i install/setup_chain.py
```

