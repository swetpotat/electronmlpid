------------------------------------------------------------------------------------------------------
The following is a few notes to the two data files in CSV format on electron PID with Machine Learning
------------------------------------------------------------------------------------------------------


The files are:
  -rw-r--r-- 1 petersen 956M Sep 21 12:53 MC_SigBkgElectrons_2000000ev.csv
  -rw-r--r-- 1 petersen 239M Sep 21 12:53 MC_SigBkgElectrons_500000ev.csv
and they contain 2.0M og 0.5M useful events (randomly divided), respectively,
with a little more background in than signal.

They are a mixture of signal (from Tag-and-Probe selection on Zee events)
and background (from W/Z-veto selection on jet-jet events). The way to
distinguish the source file (signal/background) and candidate type
(electron/non-electron) is described towards the end of this text file.

The variables for each event are listed below, subdivided by category.
Those with a "*" are those which are NOT includedd in the likelihood PID (LH_value).

Tracking variables:
-------------------
p_numberOfInnermostPixelHits,
p_numberOfPixelHits,
p_numberOfSCTHits,
p_d0,
p_d0Sig,
p_dPOverP,
p_deltaEta1,
p_deltaPhiRescaled2,
p_EptRatio,
p_TRTPID,
p_numberOfTRTHits,   (* - number of hits in the TRT detector in total)
p_TRTTrackOccupancy, (* - a measure of the occupancy/activity in the direction of the electron candidate)
p_numberOfTRTXenonHits, (* - not all TRT hits are in straws with xenon, which is the gas used for electron PID)

Calorimeter variables:
----------------------
p_Rhad1,
p_Rhad,
p_f3,
p_weta2,
p_Rphi,
p_Reta,
p_Eratio,
p_f1,
p_eta,  (* - a kinematic variable giving the direction of the electron candidate)
averageInteractionsPerCrossing, (* - provided by LHC)

Isolation variables: (normally, only the etcone30 variable is used)
--------------------
p_etcone20,
p_etcone30,
p_etcone40,
p_etcone20ptCorrection,
p_etcone30ptCorrection,
p_etcone40ptCorrection,
p_ptcone20,
p_ptcone30,
p_ptcone40,
p_ptPU30, (* - sum of pt inside cone of deltaR < 0.3 for PileUp tracks)

Other (but very important) variables:
-------------------------------------
Z_m,                         Mass of the Z from combining tag and probe electrons.
                             Nice peak for signal, set to 91.000 GeV for background.
p_LHValue,                   The likelihood value calculated by the ATLAS EGammma group - the "competitor".
p_et_calo,                   Transverse energy of the electron.
mva_Track_kBDT_conf1_mc,     BDT score for track variables
mva_Calo_kBDT_conf1_mc,      BDT score for calorimeter variables
mva_Iso_kBDT_conf1_mc,       BDT score for isolation variables
mva_kBDT_conf1_mc_final,     Linear (Fisher) combination of tracking and calo BDTs. Performance to be compared to LHvalue.
label0,                      1.0 for signal FILE, 0.0 for background FILE
label1,                      0.0 for signal FILE, 1.0 for background FILE
p_TruthType,                 What electron candidate matches in the truth record - Index refering to list below!
                             Here we define "=2" as signal, and the others as background
Truth                        1.0 if matched to signal (=2, isolated electron)
                             0.0 if matched to background (!=2, NOT isolated electron)

NOTE: In the original files, the Truth was always set to 0.0! However, using the p_TruthType, the information is there!

Thus, the selection one should use in order to get the truth matched sample wanted is:

Signal:
-------
  if (label0 > 0.5 and Truth > 0.5) ==> Signal
  if (label0 > 0.5 and p_TruthType == 2.0) ==> Signal

Background:
-----------
  if (label0 < 0.5 and Truth < 0.5) ==> Background
  if (label0 < 0.5 and p_TruthType != 2.0) ==> Background






From:
https://svnweb.cern.ch/trac/atlasoff/browser/PhysicsAnalysis/MCTruthClassifier/trunk/MCTruthClassifier/MCTruthClassifierDefs.h

25	namespace MCTruthPartClassifier {
26	
27	  enum ParticleType {
28	
29	   Unknown           =  0, 
30	   UnknownElectron   =  1, 
31	   IsoElectron       =  2,
32	   NonIsoElectron    =  3,
33	   BkgElectron       =  4,
34	   UnknownMuon       =  5, 
35	   IsoMuon           =  6,
36	   NonIsoMuon        =  7,
37	   BkgMuon           =  8,
38	   UnknownTau        =  9, 
39	   IsoTau            =  10,
40	   NonIsoTau         =  11,
41	   BkgTau            =  12,
42	   UnknownPhoton     =  13, 
43	   IsoPhoton         =  14,
44	   NonIsoPhoton      =  15,
45	   BkgPhoton         =  16,
46	   Hadron            =  17,
47	   Neutrino          =  18,
48	   NuclFrag          =  19,
49	   NonPrimary        =  20,
50	   GenParticle       =  21,
51	   SUSYParticle      =  22,
52	   BBbarMesonPart    =  23,   
53	   BottomMesonPart   =  24,
54	   CCbarMesonPart    =  25,
55	   CharmedMesonPart  =  26,
56	   BottomBaryonPart  =  27,
57	   CharmedBaryonPart =  28,
58	   StrangeBaryonPart =  29,
59	   LightBaryonPart   =  30,
60	   StrangeMesonPart  =  31,
61	   LightMesonPart    =  32,
62	   BJet              =  33,
63	   CJet              =  34,
64	   LJet              =  35,
65	   GJet              =  36,
66	   TauJet            =  37,
67	   UnknownJet        =  38 
68	  };

