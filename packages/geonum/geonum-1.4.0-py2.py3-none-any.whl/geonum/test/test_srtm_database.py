# -*- coding: utf-8 -*-
"""Test environment for base.py module."""
from __future__ import (absolute_import, division)
import numpy.testing as npt
import pytest
from geonum import SRTM_AVAILABLE
from geonum import TopoDataAccess

# custom skipif marker that is used below for test functions that 
# require SRTM.py to be installed
srtm_avail = pytest.mark.skipif(SRTM_AVAILABLE==False,
                   reason='Skipping SRTM database tests. srtm.py library is '
                   'not installed')
                    #allow_module_level=True)
    
@pytest.fixture(scope='session')
@srtm_avail
def guallatiri_data():
    # Coordinates around Guallatiri volcano
    lat0 = -18.55
    lon0 = -69.2
    lat1 = -18.35  
    lon1 = -69.0
    
    acc = TopoDataAccess()
    
    return acc.get_data(lat0, lon0, lat1, lon1)

@srtm_avail    
def test_guallatiri_topo(guallatiri_data):
    data = guallatiri_data
    npt.assert_array_equal(data.shape, (242, 122))
    npt.assert_array_almost_equal([data.min, data.max, data.mean(), data.std()],
                                  [4084., 6057., 4690.692827, 393.816227])
    
    return data
    
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    plt.close('all')
    
    data = guallatiri_data()
    
    data.plot_2d()
    
    data.plot_3d()
    
    test_guallatiri_topo(data)
    
    
    
