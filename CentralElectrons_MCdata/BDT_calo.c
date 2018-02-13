#include <cstdlib>
#include <iostream>
#include <map>
#include <string>
#include "TChain.h"
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TObjString.h"
#include "TSystem.h"
#include "TROOT.h"
#include "TMVA/Factory.h"
#include "TMVA/DataLoader.h"
#include "TMVA/Tools.h"
#include "TMVA/TMVAGui.h"
#include "TMVA/Types.h"

int BDT_calo( TString myMethodList = "" ){

   // This loads the library
   TMVA::Tools::Instance();

   // Default MVA methods to be trained + tested
   std::map<std::string,int> Use;

   // Cut optimisation - kept as the default values
   Use["Cuts"]            = 1;
   Use["CutsD"]           = 1;
   Use["CutsPCA"]         = 0;
   Use["CutsGA"]          = 0;
   Use["CutsSA"]          = 0;
   
   // Boosted Decision Trees - only Adaptive Boost was used
   Use["BDT"]             = 1; // uses Adaptive Boost
   Use["BDTG"]            = 0; // uses Gradient Boost
   Use["BDTB"]            = 0; // uses Bagging
   Use["BDTD"]            = 0; // decorrelation + Adaptive Boost
   Use["BDTF"]            = 0; // allow usage of fisher discriminant for node splitting

   // ---------------------------------------------------------------
   
   std::cout << std::endl;
   std::cout << "==> Start BDTClassification" << std::endl;

   // Select methods (don't look at this code - not of interest)
   if (myMethodList != "") {
      for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) it->second = 0;
      std::vector<TString> mlist = TMVA::gTools().SplitString( myMethodList, ',' );
      for (UInt_t i=0; i<mlist.size(); i++) {
         std::string regMethod(mlist[i]);
         if (Use.find(regMethod) == Use.end()) {
            std::cout << "Method \"" << regMethod << "\" not known in TMVA under this name. Choose among the following:" << std::endl;
            for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) std::cout << it->first << " ";
            std::cout << std::endl;
            return 1;
         }
         Use[regMethod] = 1;
      }
   }

   // --------------------------------------------------------------------------------------------------

   // Read training data
   TString fname_training = "./data/MC_SigBkgElectrons_2000000ev.root";
   if (gSystem->AccessPathName( fname_training ))  
      std::cout << "FILE DOES NOT EXIST" << std::endl;
   TFile *input_training = TFile::Open( fname_training );
   std::cout << "--- BDTClassification       : Using input training file: " << input_training->GetName() << std::endl;

   // Register the training trees
   TTree *signalTree_training     = (TTree*)input_training->Get("data");
   TTree *background_training     = (TTree*)input_training->Get("data");

   // Read test data
   TString fname_testing = "./data/MC_SigBkgElectrons_500000ev.root";
   if (gSystem->AccessPathName( fname_testing ))
   	  std::cout << "FILE DOES NOT EXIST" << std::endl;
   TFile *input_testing = TFile::Open( fname_testing );
   std::cout << "--- BDTClassificaion        : Using input testing file: " << input_testing->GetName() << std::endl;

   // Register the testing trees
   TTree *signalTree_testing      = (TTree*)input_testing->Get("data");
   TTree *background_testing      = (TTree*)input_testing->Get("data");

   // Create a ROOT output file where TMVA will store ntuples, histograms, etc.
   TString outfileName( "BDT_calo_results.root" );
   TFile* outputFile = TFile::Open( outfileName, "RECREATE" );

   // Create the factory object. Later you can choose the methods
   // whose performance you'd like to investigate. The factory is
   // the only TMVA object you have to interact with
   //
   // The first argument is the base of the name of all the
   // weightfiles in the directory weight/
   //
   // The second argument is the output file for the training results
   // All TMVA output can be suppressed by removing the "!" (not) in
   // front of the "Silent" argument in the option string
   TMVA::Factory *factory = new TMVA::Factory( "BDTClassification", outputFile, "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification" );
   TMVA::DataLoader *dataloader=new TMVA::DataLoader("dataset");

   // Define the input variables that shall be used for the MVA training - calorimeter variables
   dataloader->AddVariable( "p_Rhad1", "Rhad1", "units", 'F' );
   dataloader->AddVariable( "p_Rhad", "Rhad", "units", 'F' );
   dataloader->AddVariable( "p_f3", "f3", "units", 'F' );
   dataloader->AddVariable( "p_weta2", "weta2", "units", 'F' );
   dataloader->AddVariable( "p_Rphi", "Rphi", "units", 'F' );
   dataloader->AddVariable( "p_Reta", "Reta", "units", 'F' );
   dataloader->AddVariable( "p_Eratio", "Eratio", "units", 'F' );
   dataloader->AddVariable( "p_f1", "f1", "units", 'F' );
   dataloader->AddVariable( "p_eta", "eta", "units", 'F' );
   dataloader->AddVariable( "averageInteractionsPerCrossing", "averageInteractionsPerCrossing", "units", 'F' );

   // Global event weights per tree
   Double_t signalWeight     = 1.0;
   Double_t backgroundWeight = 1.0;

   // You can add an arbitrary number of signal or background trees
   dataloader->AddSignalTree    ( signalTree_training, signalWeight, TMVA::Types::kTraining);
   dataloader->AddBackgroundTree( background_training, backgroundWeight, TMVA::Types::kTraining );
   dataloader->AddSignalTree    ( signalTree_testing, signalWeight, TMVA::Types::kTesting);
   dataloader->AddBackgroundTree( background_testing, backgroundWeight, TMVA::Types::kTesting);

   // Set individual event weights (the variables must exist in the original TTree)
   // -  for signal    : `dataloader->SetSignalWeightExpression    ("weight1*weight2");`
   // -  for background: `dataloader->SetBackgroundWeightExpression("weight1*weight2");`
   dataloader->SetBackgroundWeightExpression( "weight" );

   // Apply additional cuts on the signal and background samples (can be different)
   TCut mycuts = ""; 
   TCut mycutb = ""; 

   // Tell the dataloader how to use the training and testing events
   dataloader->PrepareTrainingAndTestTree( mycuts, mycutb, "nTrain_Signal=1000000:nTrain_Background=1000000:nTest_Signal=250000:nTest_Background=250000:SplitMode=Random:!V");
  
   // Book the MVA method
   // Boosted Decision Trees
   if (Use["BDTG"]) // Gradient Boost
      factory->BookMethod( dataloader, TMVA::Types::kBDT, "BDTG","!H:!V:NTrees=1000:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=2" 	 );

   if (Use["BDT"])  // Adaptive Boost
      factory->BookMethod( dataloader, TMVA::Types::kBDT, "BDT","!H:!V:NTrees=200:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20"
   );

   if (Use["BDTB"]) // Bagging
      factory->BookMethod( dataloader, TMVA::Types::kBDT, "BDTB","!H:!V:NTrees=400:BoostType=Bagging:SeparationType=GiniIndex:nCuts=20" 
   );

   if (Use["BDTD"]) // Decorrelation + Adaptive Boost
      factory->BookMethod( dataloader, TMVA::Types::kBDT, "BDTD","!H:!V:NTrees=400:MinNodeSize=5%:MaxDepth=3:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=20:VarTransform=Decorrelate"
   );

  if (Use["BDTF"])  // Allow Using Fisher discriminant in node splitting for linearly correlated variables
      factory->BookMethod( dataloader, TMVA::Types::kBDT, "BDTF","!H:!V:NTrees=50:MinNodeSize=2.5%:UseFisherCuts:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:SeparationType=GiniIndex:nCuts=20"
   );

 
   // --------------------------------------------------------------------------------------------------
   
   // Train MVAs using the set of training events
   factory->TrainAllMethods();
   // Evaluate all MVAs using the set of test events
   factory->TestAllMethods();
   // Evaluate and compare performance of all configured MVAs
   factory->EvaluateAllMethods();

   // --------------------------------------------------------------

   // Save the output
   outputFile->Close();
   std::cout << "==> Wrote root file: " << outputFile->GetName() << std::endl;
   std::cout << "==> BDTClassification is done!" << std::endl;
   delete factory;
   delete dataloader;

   // Launch the GUI for the root macros
   if (!gROOT->IsBatch()) TMVA::TMVAGui( outfileName );
  	 return 0;

}

int main( int argc, char** argv ){

   // Select methods (don't look at this code - not of interest)
   TString methodList;
   for (int i=1; i<argc; i++) {
      TString regMethod(argv[i]);
      if(regMethod=="-b" || regMethod=="--batch") continue;
      if (!methodList.IsNull()) methodList += TString(",");
      	methodList += regMethod;
   }

   return BDT_calo(methodList);

}

