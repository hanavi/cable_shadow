#!/usr/bin/env python

from I3Tray import *
from icecube import icetray, dataclasses, dataio, phys_services,clsim
import numpy as np
from icecube.simprod import segments

#geofile = "data/GeoCalibDetectorStatus_2012.56063_V1.i3.gz"
#geofile = "gcd.i3"
geofile = "data/GeoCalibDetectorStatus_IC86.55697_V2.i3.gz"
SEED = 12345

for i in range(1):
    #print "Run %d:" % i

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

    tray.AddService("I3SPRNGRandomServiceFactory","I3RandomService",
                    seed = 12345,
                    nstreams = 10000,
                    streamnum = 1)
    tray.AddSegment(clsim.I3CLSimMakeHitsFromPhotons,
                    DOMOversizeFactor = 1.0,
                    MCPESeriesName = "MCPESeriesMapFiltered",
                    #PhotonSeriesName = "PropagatedPhotons",
                    PhotonSeriesName = "FilteredPropagatedPhotons",
                    RandomService = "I3RandomService",
                    UnshadowedFraction = 0.99999,)
    tray.AddSegment(segments.DetectorSim, "DetectorSim",
                    RandomService = "I3RandomService",
                    GCDFile = geofile,
                    InputPESeriesMapName = "MCPESeriesMap",
                    KeepMCHits = True,
                    #UseDOMLauncher = True,
                    SkipNoiseGenerator = False)
    tray.AddModule("I3Writer","writer", 
                   Filename = "data/dom_19_15_flash_clsim_100_id_%d.i3" %i)
    tray.AddModule("TrashCan", "the can")
    tray.Execute()

    tray.Finish()

