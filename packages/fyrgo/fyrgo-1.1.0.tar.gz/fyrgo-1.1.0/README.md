F(y)rgo
=======
A python module to easily load data from
[FargOCA](https://gitlab.oca.eu/DISC/fargOCA)
simulations into a python's scientific data analysis environment.

See `DataLoader`'s header in [`load.py`](fyrgo/load.py) for documentation.



Table of contents
-----------------
1. [Disclaimer](#disclaimer)
2. [Installation](#installation)
3. [Basic tests](#tests)
4. [Content](#content)
5. [Getting Started](#start)
6. [Fargo Version Compatibility](#version)


Disclaimer <a name="disclaimer"></a>
----------
The package is being developed and tested with **python 3.6**.

I will **not** implement compatibility for **python 2.7**.

The following known issues will be covered *when* and *if* at least one user
requires it :)

1. This package currently assumes 2D (r-phi) is being used.
2. Non-uniform grids defined via `used_rad.dat` are not supported yet.



Installation <a name="installation"></a>
------------

### Get the bleeding edge (git) version
**warning**
> The installation directory of your choosing is thereafter refered to as 
> `<instaldir>`.</p>
> This directory's parent will be made accessible through your `$PYTHONPATH` env
> variable, **so avoid putting it in your `$HOME/` **.

Copy the git repository to your local machine
```shell
# https fashion (fast installation)
git clone https://gitlab.oca.eu/crobert/fyrgo.git <instaldir>

# OR

#ssh fashion (recommended for regular contributors, but requires ssh integration with gitlab.oca.eu)
git clone git@gitlab.oca.eu:crobert/fyrgo.git <instaldir>
```

For a *local configuration*, you need to get fyrgo's python dependencies.
They can be easily installed with `pip`.
```shell
cd <instaldir>
sudo pip install -r requirements.txt
```
If you prefer using `conda` or any other python package manager,
read `requirements.txt` to know what is needed. Feedback on this part would be
appreciated.

> If you're working on @licallo.oca.eu, just run 
> `module load python/3.6<TAB><ENTER>`
> to load anaconda3 as your python distribution, which meets our requirements.

Finally, add the following line to your **~/.bashrc** file (or equivalent), and
`source` it
```bash
export PYTHONPATH=$PYTHONPATH:<instaldir>/../
# here, the path to <instaldir> should be absolute
```

### Get the latest tagged build only

```shell
pip install fyrgo
```
Yup, that's it.

### Test your installation
You should now be able to access the module's functionnalities from
any python context with the usual syntax (those are examples) :

```python
# recommended fashion
import fyrgo as fy

# cherry picking example
from fyrgo import DataLoader, profile
```

>As for many python packages, you can check your installed version number with
>```python
>import fyrgo
>print(fyrgo.__version__)
>```


Unit tests <a name="tests"></a>
-----------
If you installed fyrgo through git, you can (and should) run the unit test suite. 
```shell
cd <instaldir>
pytest
```
If any fails, please report (add a ticket or email the author).


Content <a name="content"></a>
-------

The package is organized as follow

* user accessible functions are gathered in [fyrgo/](fyrgo/)
* the main class `DataLoader` is defined in [load.py](fyrgo/load.py)
* post-processing functions such as `profile()` are defined in the 
  [postprocess.py](fyrgo/postprocess.py) module.
* some vastly used physics functions such as `hill_radius()` are defined in the
  [phys.py](fyrgo/phys.py) module.
* similarly, some geometry functions, useful for plotting circles/ellipses are
  defined in [geometry.py](fyrgo/geometry.py)
* internal machinery, data scrapping functions are defined in [utils/](fyrgo/utils/)



Getting started <a name="start"></a>
---------------

The included [Jupyter notebook](Intro_to_fyrgo.ipynb) demonstrates the main features of
the package, using sample [data/](data/).

![](gallery/fig1.png)
![](gallery/fig2.png)
![](gallery/fig3.png)



Fargo Version Compatibility <a name="version"></a>
---------------------------

[FargOCA](https://gitlab.oca.eu/DISC/fargOCA) is currently under development and
formats of files such as `planetXXX.dat`, `orbitXXX.dat` and `accXXX.dat` are
prone to changes, and are **already incompatible with their equivalent from the
official distribution of `FARGO`**.

If you use a different version of the program, you'll need to write a
configuration file similar to
[formats/default.def](formats/default.def) and specify it when
instancing the class `DataLoader`.