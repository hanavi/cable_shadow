#!/usr/bin/env python

from ROOT import TFile, TTree, TCanvas, TH1F, TLegend, gStyle, THStack
rfiles = {}
myhist = {}
leg = {}

rfiles_nofilter = {}
myhist_nofilter = {}

gStyle.SetOptStat(0)
c = {}

for n in range(4):
    c[n] = TCanvas("c[%d]" %n,"Simulated Flashers Rotated Cable", 200, 10, 600, 800 )
    c[n].Divide(1,3)
    ofname = "figs/set_%d.png" % n

    for i in range(n*3,n*3+3):
        leg[i] = TLegend(.75,.75,.95,.95)

        fname = "dom_19_15_flashes_clsim_1_id_%d.root" % i
        fname2 = "dom_19_15_flashes_clsim_1_id_%d_no_filter.root" % i

        rfiles[i] = TFile("data/%s" %fname)
        rfiles_nofilter[i] = TFile("data/%s" %fname2)

        myhist[i] = TH1F("myhist[%d]" % i,"Cable Angle: %d deg" % int(i/12.*360) ,200,0,3000)
        myhist[i].SetLineColor(2)
        myhist[i].SetLineWidth(1)

        myhist_nofilter[i] = TH1F("myhist_nofilter[%d]" % i,"Cable Angle: %d deg" % int(i/12.*360),200,0,3000)
        myhist_nofilter[i].SetLineColor(1)
        myhist_nofilter[i].SetLineWidth(1)

        leg[i].AddEntry(myhist_nofilter[i],"No Shadow","l")
        leg[i].AddEntry(myhist[i],"With Shadow","l")

        tree = rfiles[i].Get("FlasherShiftedPulses")
        tree_nofilter = rfiles_nofilter[i].Get("FlasherShiftedPulses")
        
        k = i - 3*n
        c[n].cd(k+1)
        #c[n].cd(k+2)
        tree_nofilter.Draw("time >> myhist_nofilter[%d]" % i,"charge")
        tree.Draw("time >> myhist[%d]" % i,"charge","same")

        leg[i].Draw()
    c[n].Print(ofname,"name png")






