#!/usr/bin/env python

from ROOT import TFile, TTree, TCanvas, TH1F, TLegend, gStyle, THStack

gStyle.SetOptStat(0)
leg = TLegend(.75,.75,.95,.95)
leg.SetHeader("Rotation Angle")

c1 = TCanvas("c1",'Simulated Flashers with Rotated Cable', 200, 10, 700, 500 )

rfiles = {}
myhist = {}
for i in range(12):
    fname = "dom_19_15_flashes_clsim_1_id_%d.root" % i
    rfiles[i] = TFile("data/%s" %fname)
    myhist[i] = TH1F("myhist[%d]" % i,"Charge Weighted Time",200,0,3000)
    myhist[i].SetLineColor(i)
    myhist[i].SetLineWidth(1)

    tree = rfiles[i].Get("FlasherShiftedPulses")
    fl_name = "Angle %d" % int(i/12.*360)
    leg.AddEntry(myhist[i],fl_name,"l")
    if i == 0:
        tree.Draw("time >> myhist[%d]" % i,"charge")
    else:
        tree.Draw("time >> myhist[%d]" % i,"charge","same")


leg.Draw()
