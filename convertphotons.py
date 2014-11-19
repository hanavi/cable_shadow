#!/usr/bin/env python

from I3Tray import *
from icecube import icetray, dataclasses, dataio, phys_services,clsim
import numpy as np
from icecube.simprod import segments

geofile = "GeoCalibDetectorStatus_2012.56063_V1.i3.gz"

#badDOMlist = "/nv/hp11/jcasey8/data3/icecube/clsim/src/BadDomList/resources/scripts/bad_data_producing_doms_list.txt"

for i in range(12):
    print "Run %d:" % i

    ca = np.pi*i/12.
    #fname = "data/dom_19_15_flashes_clsim_nosave.i3"
    fname = "data/dom_19_15_flashes_clsim_100.i3"
    #fname = "testdata/out_all_%d.i3" % i
    tray = I3Tray()


    cablemap = dataclasses.I3MapKeyDouble()
    cablemap[OMKey(19,15)] = ca

    tray.AddModule("I3Reader","reader",Filename=fname)
    #tray.AddModule("I3GCDAuditor","auditor")
    tray.AddModule("I3CableShadowModule","cableshadow",CableMap=cablemap)
    tray.AddService("I3SPRNGRandomServiceFactory","random",
                    seed = 12345,
                    nstreams = 10000,
                    streamnum = 1)
    tray.AddSegment(clsim.I3CLSimMakeHitsFromPhotons,
                    DOMOversizeFactor = 1.0,
                    MCPESeriesName = "MCPESeriesMap",
                    #PhotonSeriesName = "PropagatedPhotons",
                    PhotonSeriesName = "FilteredPropagatedPhotons",
                    RandomService = "random",
                    UnshadowedFraction = 1.0,)
    tray.AddSegment(segments.DetectorSim, "DetectorSim",
                    RandomService = "random",
                    GCDFile = geofile,
                    InputPESeriesMapName = "MCPESeriesMap",
                    KeepMCHits = True,
                    UseDOMLauncher = True,
                    SkipNoiseGenerator = False)
    tray.AddModule("I3Writer","writer", 
                   Filename = "data/dom_19_15_flash_clsim_1_id_%d.i3" %i)
    tray.Execute(6)


