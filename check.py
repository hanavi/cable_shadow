#!/usr/bin/env python

from ROOT import TFile, TH1F

tfile = TFile.Open("test.root")
data = tfile.Get("flasher_")
print data.GetEntries()
