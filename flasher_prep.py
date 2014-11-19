#!/usr/bin/env python

from I3Tray import *
from icecube import icetray, dataclasses, dataio, WaveCalibrator,wavedeform,DomTools
from icecube.WaveCalibrator import DOMCalBaselineModule
from os.path import expandvars;
import sys
import os
from glob import glob
from string import atof,atoi
from icecube.tableio    import I3TableWriter
from icecube.rootwriter import I3ROOTTableService

load("libdataclasses")
load("libphys-services")
load("libdataio")
load("libflasher-fill")
load("libI3Db")
load("libicepick")
#load("libquick-verification")
load("libpayload-parsing")
load("libdaq-decode")
#load("libpfauxiliary")
#load("libflasher-timing")
#load("libFeatureExtractor")
#load("libDOMcalibrator")
load("libflasher-verif")
load("libDomTools")
#load("libNFE")
load("libwavedeform")

tray = I3Tray()

#tools = expandvars("$I3_TOOLS")

#infile=sys.argv[1]


inice_rawdata                  = "InIceRawData"              # the name of the "InIce raw" DOMlaunch series frame-object
icetop_rawdata                 = "IceTopRawData"             # the name of the "IceTop raw" DOMlaunch series frame-object
inice_beacon                   = "InIceBeaconHits"           # the name of the "InIce beacon hits" DOMlaunch series frame-object
icetop_beacon                  = "IceTopBeaconHits"          # the name of the "IceTop beacon hits" DOMlaunch series frame-object
special_rawdata                = "SpecialRawData"            # the name of the "special DOM" DOMlaunch series frame-object
inice_clean_launches_name      = "InIceCleanedDomLaunches"   # the name of the "hit cleaned" InIce DOMlaunch series frame-object
icetop_clean_launches_name     = "IceTopCleanedDomLaunches"  # the name of the "hit cleaned" IceTop DOMlaunch series frame-object
inice_clean_launches_name_tmp  = "InIceCleanedDomLaunchesTmp"   # the name of the "hit cleaned" InIce DOMlaunch series frame-object
icetop_clean_launches_name_tmp = "IceTopCleanedDomLaunchesTmp"  # the name of the "hit cleaned" IceTop DOMlaunch series frame-object



inice_analysis_launches_name  = inice_clean_launches_name   # the name of the InIce DOMLaunch series to use in the analysis
icetop_analysis_launches_name = icetop_clean_launches_name  # the name of the IceTop DOMLaunches series to use in the analysis
hit_series                    = "InitialHitSeriesReco"      # the name of the "reco hit series" frame-object
pulse_series                  = "InitialPulseSeriesReco"    # the name of the "reco pulse series" frame-object

i3_header_name                = "I3DAQEventHeader"          # name of IceCube event header
i3_trigger_name               = "I3DAQTriggerHierarchy"     # name of IceCube trigger 
i3_buffer_name                = "I3DAQData"                 # name of raw IceCube buffer data

twr_header_name               = "TWRDAQEventHeader"         # name of TWR event header
twr_trigger_name              = "TWRDAQTriggerHierarchy"    # name of TWR trigger
twr_buffer_name               = "TWRDAQData"                # name of raw TWR buffer data
twr_raw_name                  = "TWRRawData"                # name of raw TWR frame object
twr_cleaned_name              = "TWRRawDataCleaned"         # name of cleaned raw TWR frame object
twr_reco_name                 = "TWRPulseSeriesReco"        # name of TWR reco pulse series, unshifted
twr_reco_shifted_name         = "TWRPulseSeriesRecoshifted" # name of TWR reco pulse series, shifted into IceCube time frame
twr_timeshift_name            = "TWRRawTimeCorrectionData"  # name of TWR time correction frame object
combined_reco_name            = "CombinedPulses"            # name of combined IceCube + TWR reco pulse series


infile=sys.argv[1]
outfile=sys.argv[2]
#fstr=int(sys.argv[3])
#fdom=int(sys.argv[4])


dbserver="dbs2.icecube.wisc.edu"
username="www"
workspace = expandvars("$I3_SRC")

tray.AddService("I3DbOMKey2MBIDFactory","omkey2mbid")(
    ("host",dbserver),
    ("username",username),
    ("database","I3OmDb")
    )  

tray.AddModule("I3Reader","readerfactory")(
    ("Filename", infile),
    )


tray.AddService("I3PayloadParsingEventDecoderFactory","i3eventdecode")(
  #  ("Year",2008),
    ("headerid",i3_header_name),
    ("triggerid",i3_trigger_name),
    ("specialdataid",special_rawdata),
    ("specialdataoms",[OMKey(0,91),OMKey(0,92)]),
    ("flasherdataid","Flasher"),
    ("CPUDataID","BeaconHits")
    )

tray.AddModule("I3FrameBufferDecode","i3decode")(
          ("BufferID",i3_buffer_name)
          )

tray.AddModule('I3LCCleaning','LCClean_inice',
                InIceInput = 'InIceRawData',
                InIceOutput = 'InIceRawDataClean',
                )

tray.AddModule('I3WaveCalibrator', 'wavecal',
                Launches='InIceRawDataClean',
                )

tray.AddModule('I3Wavedeform', 'wavedeform',)

tray.AddModule("I3NullSplitter","triggersplit")

#tray.AddModule("Dump","dumpit")

def PulseShift(frame):
    writeFrame = False
    shiftedpulses=dataclasses.I3RecoPulseSeriesMap()
    if (frame.Has("WavedeformPulses") and frame.Has("I3FlasherInfo")):
        writeFrame = True
        # print frame["SRTOfflinePulses"]
        pulse_map = frame["WavedeformPulses"]
        flashervect = frame.Get("I3FlasherInfo")
        for f in flashervect:
            ft = f.flash_time
        for om, pulse_series in pulse_map:
            vec = dataclasses.I3RecoPulseSeries()
            q_vect=[]
            t_vect=[]
            #print "OM Key: ", om
            for pulses in pulse_series:
                #print "Pulses: ", pulses        
                pulse = dataclasses.I3RecoPulse()
                q = pulses.charge
                t = pulses.time - ft
                pulse.time = t
                pulse.charge = q
                vec.append(pulse)
            shiftedpulses[om] = vec
    if (writeFrame):
        frame["FlasherShiftedPulses"] = shiftedpulses


tray.AddModule(PulseShift,"shifter",Streams=[icetray.I3Frame.Physics])


#tray.AddModule("I3Writer","outfile")(
#	("Filename","out.i3"),
#)

tray.AddModule(I3TableWriter, "rootfilewriter") (
        ("SubEventStreams", ['triggersplit',]),
        ("TableService",  I3ROOTTableService(outfile)),
        ("Keys",          ["FlasherShiftedPulses","WavedeformPulses"]),
        )

tray.AddModule("TrashCan","trash")

tray.Execute()
tray.Finish()

