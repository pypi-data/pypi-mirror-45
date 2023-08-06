import pathlib
import pytest
from pandas import DataFrame

import fyrgo as fy

fyloc = fy.__path__[0]
fypath = pathlib.Path(fyloc)
datapath = fypath.parent / 'data'

def test_load_from_pathlib():
    args = dict(configfile = datapath / 'config.par',
                outputdir  = datapath)
    dl = fy.DataLoader(**args)
    assert(dl.configfile == str(datapath / 'config.par'))
    assert(dl.outputdir == str(datapath))

def test_load_exception():
    with pytest.raises(AssertionError):
        fy.DataLoader(
            configfile=datapath / 'config.par',
            outputdir='some_imaginary_path'
        )

def test_guess_outputdir():
    dl = fy.DataLoader(configfile = datapath / 'config.par')
    assert(dl.outputdir == str(datapath))

def test_load_full_datafile():
    dl = fy.DataLoader(configfile = datapath / 'config.par',
    )
    assert type(dl["acc"] == DataFrame)

def test_load_no_accfile():
    dl = fy.DataLoader(configfile = datapath / 'config.par',
                       outputdir = datapath / 'simpledata',
    )
    with pytest.raises(KeyError):
        dl["acc"]
