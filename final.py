#!/usr/bin/env python

from I3Tray import *
from icecube import icetray, dataclasses, dataio, phys_services,clsim
import numpy as np

fname = "testdata/out_all_0.i3"
tray = I3Tray()

geofile = "/nv/hp11/jcasey8/data/icecube/ports/test-data/sim/GeoCalibDetectorStatus_IC86.55380_corrected.i3.gz"

tray.AddModule("I3Reader","reader",Filename=fname)

tray.AddService("I3SPRNGRandomServiceFactory","random",
    seed = 12345,
    nstreams = 10000,
    streamnum = 1)

from icecube.simprod import segments
tray.AddSegment(segments.DetectorSim, "DetectorSim",
            RandomService = "random",
            GCDFile = geofile,
            InputPESeriesMapName = "MCPESeriesMap",
            KeepMCHits = True,
            UseDOMLauncher = True,
            SkipNoiseGenerator = False)


tray.AddModule("I3Writer","writer", Filename = "testdata/test_out_all_0.i3" )
tray.Execute()
