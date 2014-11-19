#!/usr/bin/env python

from ROOT import TFile, TTree, TCanvas, TH1F, TLegend, gStyle, THStack
rfiles = {}
myhist = {}

rfiles_nofilter = {}
myhist_nofilter = {}

c = {}
#c1 = TCanvas("c1","Simulated Flashers Rotated Cable", 200, 10, 1000, 800 )
#c2 = TCanvas("c2","Simulated Flashers Rotated Cable", 200, 10, 1000, 800 )
#c3 = TCanvas("c3","Simulated Flashers Rotated Cable", 200, 10, 1000, 800 )
#c4 = TCanvas("c4","Simulated Flashers Rotated Cable", 200, 10, 1000, 800 )

#c1.Divide(2,3)
#c2.Divide(2,3)
#c3.Divide(2,3)
#c4.Divide(2,3)

for n in range(4):
    c[n] = TCanvas("c[%d]" %n,"Simulated Flashers Rotated Cable", 200, 10, 1000, 800 )
    c[n].Divide(2,3)

    for i in range(n*3,n*3+3):

        fname = "dom_19_15_flashes_clsim_1_id_%d.root" % i
        fname2 = "dom_19_15_flashes_clsim_1_id_%d_no_filter.root" % i

        rfiles[i] = TFile("data/%s" %fname)
        rfiles_nofilter[i] = TFile("data/%s" %fname2)

        myhist[i] = TH1F("myhist[%d]" % i,"Cable Angle: %d deg" % int(i/12.*360) ,200,0,3000)
        myhist[i].SetLineColor(1)
        myhist[i].SetLineWidth(1)

        myhist_nofilter[i] = TH1F("myhist_nofilter[%d]" % i,"Cable Angle (No Filter): %d deg" % int(i/12.*360),200,0,3000)
        myhist_nofilter[i].SetLineColor(1)
        myhist_nofilter[i].SetLineWidth(1)

        tree = rfiles[i].Get("FlasherShiftedPulses")
        tree_nofilter = rfiles_nofilter[i].Get("FlasherShiftedPulses")
        
        k = 2*i - 6*n
        c[n].cd(k+1)
        tree.Draw("time >> myhist[%d]" % i,"charge")
        c[n].cd(k+2)
        tree_nofilter.Draw("time >> myhist_nofilter[%d]" % i,"charge")

#for i in range(3,6):
#
#    fname = "dom_19_15_flashes_clsim_1_id_%d.root" % i
#    fname2 = "dom_19_15_flashes_clsim_1_id_%d_no_filter.root" % i
#
#    rfiles[i] = TFile("data/%s" %fname)
#    rfiles_nofilter[i] = TFile("data/%s" %fname2)
#
#    myhist[i] = TH1F("myhist[%d]" % i,"Cable Angle: %d deg" % int(i/12.*360) ,200,0,3000)
#    myhist[i].SetLineColor(1)
#    myhist[i].SetLineWidth(1)
#
#    myhist_nofilter[i] = TH1F("myhist_nofilter[%d]" % i,"Cable Angle (No Filter): %d deg" % int(i/12.*360),200,0,3000)
#    myhist_nofilter[i].SetLineColor(1)
#    myhist_nofilter[i].SetLineWidth(1)
#
#    tree = rfiles[i].Get("FlasherShiftedPulses")
#    tree_nofilter = rfiles[i].Get("FlasherShiftedPulses")
#    
#    k = 2*i - 6
#    c2.cd(k+1)
#    tree.Draw("time >> myhist[%d]" % i,"charge")
#    c2.cd(k+2)
#    tree_nofilter.Draw("time >> myhist[%d]" % i,"charge")
#
#for i in range(6,9):
#
#    fname = "dom_19_15_flashes_clsim_1_id_%d.root" % i
#    fname2 = "dom_19_15_flashes_clsim_1_id_%d_no_filter.root" % i
#
#    rfiles[i] = TFile("data/%s" %fname)
#    rfiles_nofilter[i] = TFile("data/%s" %fname2)
#
#    myhist[i] = TH1F("myhist[%d]" % i,"Cable Angle: %d deg" % int(i/12.*360) ,200,0,3000)
#    myhist[i].SetLineColor(1)
#    myhist[i].SetLineWidth(1)
#
#    myhist_nofilter[i] = TH1F("myhist_nofilter[%d]" % i,"Cable Angle (No Filter): %d deg" % int(i/12.*360),200,0,3000)
#    myhist_nofilter[i].SetLineColor(1)
#    myhist_nofilter[i].SetLineWidth(1)
#
#    tree = rfiles[i].Get("FlasherShiftedPulses")
#    tree_nofilter = rfiles[i].Get("FlasherShiftedPulses")
#    
#    k = 2*i - 12
#    c3.cd(k+1)
#    tree.Draw("time >> myhist[%d]" % i,"charge")
#    c3.cd(k+2)
#    tree_nofilter.Draw("time >> myhist[%d]" % i,"charge")
#
#for i in range(9,12):
#
#    fname = "dom_19_15_flashes_clsim_1_id_%d.root" % i
#    fname2 = "dom_19_15_flashes_clsim_1_id_%d_no_filter.root" % i
#
#    rfiles[i] = TFile("data/%s" %fname)
#    rfiles_nofilter[i] = TFile("data/%s" %fname2)
#
#    myhist[i] = TH1F("myhist[%d]" % i,"Cable Angle: %d deg" % int(i/12.*360) ,200,0,3000)
#    myhist[i].SetLineColor(1)
#    myhist[i].SetLineWidth(1)
#
#    myhist_nofilter[i] = TH1F("myhist_nofilter[%d]" % i,"Cable Angle (No Filter): %d deg" % int(i/12.*360),200,0,3000)
#    myhist_nofilter[i].SetLineColor(1)
#    myhist_nofilter[i].SetLineWidth(1)
#
#    tree = rfiles[i].Get("FlasherShiftedPulses")
#    tree_nofilter = rfiles[i].Get("FlasherShiftedPulses")
#    
#    k = 2*i - 18
#    c4.cd(k+1)
#    tree.Draw("time >> myhist[%d]" % i,"charge")
#    c4.cd(k+2)
#    tree_nofilter.Draw("time >> myhist[%d]" % i,"charge")
#
