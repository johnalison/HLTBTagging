#include <iostream>
#include <string>
#include <sstream>
#include <map>
#include <vector>

#include "TFile.h"
#include "TTree.h"
#include "TChain.h"
#include "TString.h"
#include "TObjString.h"
#include "TSystem.h"
#include "TROOT.h"

using namespace std;

void reProcessNtuples( )
{
  bool data = true;
  
  //Create file for output
  //TString outfilename("test.root");
  char* outfilename = getenv("OUTPUTFILE");
  TFile* outputFile = new TFile( outfilename, "RECREATE" );
  cout << "Using name for ouputfile: " << outfilename << endl;

  //Set up input tree
  //TChain* InputChain = new TChain("tree");
  //const char* filenames = "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v2/MuonEG/tree_70.root";
  //const char* filenames = "/mnt/t3nfs01/data01/shome/koschwei/scratch/HLTBTagging/DiLepton_v2/MuonEG/tree_70.root";
  const char* filenames = getenv("INPUTFILES");
  cout << "Processing file: " << filenames << endl;
  TFile* file = TFile::Open( (filenames), "update" );
  TTree *InputChain = (TTree*)file->Get("tree");
  /*

  string buf;
  stringstream ss(filenames);
  while (ss >> buf){
    InputChain->Add(buf.c_str());
  }
  */
  Float_t event;
  Int_t nOffJets, nOffJets2, nGenJets, nPFJets, nCaloJets, nL1Jets;
  Float_t off_pt[50], off_eta[50], off_csv[50], off_deepcsv_b[50], off_deepcsv_bb[50];
  Int_t off_matchGen[50];
  Float_t off_i1CSV, off_i2CSV, off_i3CSV, off_i4CSV;
  Float_t off_i1DeepCSV, off_i2DeepCSV, off_i3DeepCSV, off_i4DeepCSV;
  Float_t off_LooseID[50], off_TightID[50], off_TightLepID[50];
  Float_t off_rankCSV[50], off_rankDeepCSV[50];
  Int_t pf_matchOff[50], calo_matchOff[50];
  Int_t gen_mcF[50];

  cout << "Setting branch status 0" << endl;
  //InputChain->SetBranchStatus("*",1);
  InputChain->SetBranchStatus("offJets*",0);
  InputChain->SetBranchStatus("offTightJets*",0);
  outputFile->cd();
  TTree* outputTree = InputChain->CloneTree();
  //TTree* outputTree = new TTree("tree","tree");
  file->cd();
  cout << "Setting branch status 1" << endl;
  InputChain->SetBranchStatus("offJets*",1);
  InputChain->SetBranchStatus("offTightJets*",1);





  
  cout << "Setting event variables" << endl;
  InputChain->SetBranchAddress("evt",&event);
  
  InputChain->SetBranchAddress("l1Jets_num", &nL1Jets);
  InputChain->SetBranchAddress("offTightJets_num", &nOffJets);
  InputChain->SetBranchAddress("offJets_num", &nOffJets2);
  //InputChain->SetBranchAddress("genJets_num", &nGenJets);
  InputChain->SetBranchAddress("pfJets_num", &nPFJets);
  InputChain->SetBranchAddress("caloJets_num", &nCaloJets);

  cout << "Setting jet variables" << endl;
  InputChain->SetBranchAddress("offTightJets_pt[offTightJets_num]", &off_pt);
  InputChain->SetBranchAddress("offTightJets_eta[offTightJets_num]", &off_eta);
  InputChain->SetBranchAddress("offTightJets_csv[offTightJets_num]", &off_csv);
  InputChain->SetBranchAddress("offTightJets_deepcsv[offTightJets_num]", &off_deepcsv_b);
  InputChain->SetBranchAddress("offTightJets_deepcsv_bb[offTightJets_num]", &off_deepcsv_bb);
  InputChain->SetBranchAddress("offTightJets_ileadingCSV", &off_i1CSV);
  InputChain->SetBranchAddress("offTightJets_isecondCSV", &off_i2CSV);
  InputChain->SetBranchAddress("offTightJets_ithirdCSV", &off_i3CSV);
  InputChain->SetBranchAddress("offTightJets_ifourthCSV", &off_i4CSV);
  InputChain->SetBranchAddress("offTightJets_ileadingDeepCSV", &off_i1DeepCSV);
  InputChain->SetBranchAddress("offTightJets_isecondDeepCSV", &off_i2DeepCSV);
  InputChain->SetBranchAddress("offTightJets_ithirdDeepCSV", &off_i3DeepCSV);
  InputChain->SetBranchAddress("offTightJets_ifourthDeepCSV", &off_i4DeepCSV);
  InputChain->SetBranchAddress("offTightJets_passesLooseID[offTightJets_num]", &off_LooseID);
  InputChain->SetBranchAddress("offTightJets_passesTightID[offTightJets_num]", &off_TightID);
  InputChain->SetBranchAddress("offTightJets_passesTightLeptVetoID[offTightJets_num]", &off_TightLepID);
  //InputChain->SetBranchAddress("offTightJets_matchGen", &off_matchGen);
  InputChain->SetBranchAddress("offTightJets_rankCSV[offTightJets_num]", &off_rankCSV);
  InputChain->SetBranchAddress("offTightJets_rankDeepCSV[offTightJets_num]", &off_rankDeepCSV);
  InputChain->SetBranchAddress("caloJets_matchOff[caloJets_num]", &calo_matchOff);
  InputChain->SetBranchAddress("pfJets_matchOff[pfJets_num]", &pf_matchOff);
  //InputChain->SetBranchAddress("genJets_mcFlavour", &gen_mcF);

  
  outputFile->cd();
  
  
  int nOffJetsOUT;
  float off_ptOUT[50], off_etaOUT[50], off_csvOUT[50], off_deepcsvOUT[50], off_deepcsv_bOUT[50], off_deepcsv_bbOUT[50];
  int off_matchGenOUT[50], off_matchCaloOUT[50], off_matchPFOUT[50], off_mcFlavourOUT[50];
  int off_i1CSVOUT, off_i2CSVOUT, off_i3CSVOUT, off_i4CSVOUT;
  int off_i1DeepCSVOUT, off_i2DeepCSVOUT, off_i3DeepCSVOUT, off_i4DeepCSVOUT;
  int off_LooseIDOUT[50], off_TightIDOUT[50], off_TightLepIDOUT[50];
  int off_rankCSVOUT[50],off_rankDeepCSVOUT[50];
  int calo_mcFlavourOUT[50], pf_mcFlavourOUT[50];

  int nCSVOffJetsOUT;
  float offCSV_ptOUT[50], offCSV_etaOUT[50], offCSV_csvOUT[50], offCSV_deepcsvOUT[50], offCSV_deepcsv_bOUT[50], offCSV_deepcsv_bbOUT[50];
  int offCSV_matchGenOUT[50], offCSV_matchCaloOUT[50], offCSV_matchPFOUT[50], offCSV_mcFlavourOUT[50];
  int offCSV_i1CSVOUT, offCSV_i2CSVOUT, offCSV_i3CSVOUT, offCSV_i4CSVOUT;
  int offCSV_i1DeepCSVOUT, offCSV_i2DeepCSVOUT, offCSV_i3DeepCSVOUT, offCSV_i4DeepCSVOUT;
  int offCSV_LooseIDOUT[50], offCSV_TightIDOUT[50], offCSV_TightLepIDOUT[50];
  int offCSV_rankptOUT[50];


  
  int nDeepCSVOffJetsOUT;
  float offDeepCSV_ptOUT[50], offDeepCSV_etaOUT[50], offDeepCSV_csvOUT[50], offDeepCSV_deepcsvOUT[50], offDeepCSV_deepcsv_bOUT[50], offDeepCSV_deepcsv_bbOUT[50];
  int offDeepCSV_matchGenOUT[50], offDeepCSV_matchCaloOUT[50], offDeepCSV_matchPFOUT[50], offDeepCSV_mcFlavourOUT[50];
  int offDeepCSV_i1CSVOUT, offDeepCSV_i2CSVOUT, offDeepCSV_i3CSVOUT, offDeepCSV_i4CSVOUT;
  int offDeepCSV_i1DeepCSVOUT, offDeepCSV_i2DeepCSVOUT, offDeepCSV_i3DeepCSVOUT, offDeepCSV_i4DeepCSVOUT;
  int offDeepCSV_LooseIDOUT[50], offDeepCSV_TightIDOUT[50], offDeepCSV_TightLepIDOUT[50];
  int offDeepCSV_rankCSVOUT[50],offDeepCSV_rankDeepCSVOUT[50];
  int offDeepCSV_rankptOUT[50];

  
  cout << "Setting pt ordered branches" << endl;
  TBranch *offnum = outputTree->Branch("offJets_num", &nOffJetsOUT, "offJets_num/I");
  TBranch *offpt = outputTree->Branch("offJets_pt", &off_ptOUT, "offJets_pt[offJets_num]/F");
  TBranch *offeta = outputTree->Branch("offJets_eta", &off_etaOUT, "offJets_eta[offJets_num]/F");
  TBranch *offcsv = outputTree->Branch("offJets_csv", &off_csvOUT, "offJets_csv[offJets_num]/F");
  TBranch *offdeepcsv = outputTree->Branch("offJets_deepcsv", &off_deepcsvOUT, "offJets_deepcsv[offJets_num]/F");
  TBranch *offdeepcsvb = outputTree->Branch("offJets_deepcsv_b", &off_deepcsv_bOUT, "offJets_deepcsv_b[offJets_num]/F");
  TBranch *offdeepcsvbb = outputTree->Branch("offJets_deepcsv_bb", &off_deepcsv_bbOUT, "offJets_deepcsv_bb[offJets_num]/F");
  TBranch *offlID = outputTree->Branch("offJets_passesLooseID", &off_LooseIDOUT, "offJets_passesLooseID[offJets_num]/I");
  TBranch *offtID = outputTree->Branch("offJets_passesTightID",&off_TightIDOUT,"offJets_passesTightID[offJets_num]/I");
  TBranch *offtlID = outputTree->Branch("offJets_passesTightLeptVetoID", &off_TightLepIDOUT,"offJets_passesTightLeptVetoID[offJets_num]/I");
  TBranch *off1CSV = outputTree->Branch("offJets_ileadingCSV", &off_i1CSVOUT,"offJets_ileadingCSV/I");
  TBranch *off2CSV = outputTree->Branch("offJets_isecondCSV", &off_i2CSVOUT,"offJets_isecondCSV/I");
  TBranch *off3CSV = outputTree->Branch("offJets_ithirdCSV", &off_i3CSVOUT,"offJets_ithirdCSV/I");
  TBranch *off4CSV = outputTree->Branch("offJets_ifourthCSV", &off_i4CSVOUT,"offJets_ifourthCSV/I");
  TBranch *off1DeepCSV = outputTree->Branch("offJets_ileadingDeepCSV", &off_i1DeepCSVOUT,"offJets_ileadingDeepCSV/I");
  TBranch *off2DeepCSV = outputTree->Branch("offJets_isecondDeepCSV", &off_i2DeepCSVOUT,"offJets_isecondDeepCSV/I");
  TBranch *off3DeepCSV = outputTree->Branch("offJets_ithirdDeepCSV", &off_i3DeepCSVOUT,"offJets_ithirdDeepCSV/I");
  TBranch *off4DeepCSV = outputTree->Branch("offJets_ifourthDeepCSV", &off_i4DeepCSVOUT,"offJets_ifourthDeepCSV/I");
  TBranch *offmatchPF = outputTree->Branch("offJets_matchPF",&off_matchPFOUT, "offJets_matchPF[offJets_num]/I");
  TBranch *offmatchCalo = outputTree->Branch("offJets_matchCalo",&off_matchCaloOUT, "offJets_matchCalo[offJets_num]/I");
  TBranch *offmcF = outputTree->Branch("offJets_mcFlavour",&off_mcFlavourOUT, "offJets_mcFlavour[offJets_num]/I");
  TBranch *offmatchGen = outputTree->Branch("offJets_machGen",&off_matchGenOUT, "offJets_matchGen[offJets_num]/I");
  TBranch *offrankCSV = outputTree->Branch("offJets_rankCSV",&off_rankCSVOUT, "offJets_rankCSV[offJets_num]/I");
  TBranch *offrankDeepCSV = outputTree->Branch("offJets_rankDeepCSV",&off_rankDeepCSVOUT, "offJets_rankDeepCSV[offJets_num]/I");

  cout << "Setting csv ordered branches" << endl;
  TBranch *offDeepCSVnum = outputTree->Branch("offDeepCSVJets_num", &nDeepCSVOffJetsOUT, "offDeepCSVJets_num/I");
  TBranch *offDeepCSVpt = outputTree->Branch("offDeepCSVJets_pt", &offDeepCSV_ptOUT, "offDeepCSVJets_pt[offDeepCSVJets_num]/F");
  TBranch *offDeepCSVeta = outputTree->Branch("offDeepCSVJets_eta", &offDeepCSV_etaOUT, "offDeepCSVJets_eta[offDeepCSVJets_num]/F");
  TBranch *offDeepCSVcsv = outputTree->Branch("offDeepCSVJets_csv", &offDeepCSV_csvOUT, "offDeepCSVJets_csv[offDeepCSVJets_num]/F");
  TBranch *offDeepCSVdeepcsv = outputTree->Branch("offDeepCSVJets_deepcsv", &offDeepCSV_deepcsvOUT, "offDeepCSVJets_deepcsv[offDeepCSVJets_num]/F");
  TBranch *offDeepCSVdeepcsvb = outputTree->Branch("offDeepCSVJets_deepcsv_b", &offDeepCSV_deepcsv_bOUT, "offDeepCSVJets_deepcsv_b[offDeepCSVJets_num]/F");
  TBranch *offDeepCSVdeepcsvbb = outputTree->Branch("offDeepCSVJets_deepcsv_bb", &offDeepCSV_deepcsv_bbOUT, "offDeepCSVJets_deepcsv_bb[offDeepCSVJets_num]/F");
  TBranch *offDeepCSVlID = outputTree->Branch("offDeepCSVJets_passesLooseID", &offDeepCSV_LooseIDOUT, "offDeepCSVJets_passesLooseID[offDeepCSVJets_num]/I");
  TBranch *offDeepCSVtID = outputTree->Branch("offDeepCSVJets_passesTightID",&offDeepCSV_TightIDOUT,"offDeepCSVJets_passesTightID[offDeepCSVJets_num]/I");
  TBranch *offDeepCSVtlID = outputTree->Branch("offDeepCSVJets_passesTightLeptVetoID", &offDeepCSV_TightLepIDOUT,"offDeepCSVJets_passesTightLeptVetoID[offDeepCSVJets_num]/I");
  TBranch *offDeepCSVmatchPF = outputTree->Branch("offDeepCSVJets_matchPF",&offDeepCSV_matchPFOUT, "offDeepCSVJets_matchPF[offDeepCSVJets_num]/I");
  TBranch *offDeepCSVmatchCalo = outputTree->Branch("offDeepCSVJets_matchCalo",&offDeepCSV_matchCaloOUT, "offDeepCSVJets_matchCalo[offDeepCSVJets_num]/I");
  TBranch *offDeepCSVmcF = outputTree->Branch("offDeepCSVJets_mcFlavour",&offDeepCSV_mcFlavourOUT, "offDeepCSVJets_mcFlavour[offDeepCSVJets_num]/I");
  TBranch *offDeepCSVmatchGen = outputTree->Branch("offDeepCSVJets_machGen",&offDeepCSV_matchGenOUT, "offDeepCSVJets_matchGen[offDeepCSVJets_num]/I");
  TBranch *offDeepCSVrankpt = outputTree->Branch("offDeepCSVJets_rankpt",&offDeepCSV_rankptOUT, "offDeepCSVJets_rankpt[offDeepCSVJets_num]/I");

  cout << "Setting deepcvs ordered branches" << endl;
  TBranch *offCSVnum = outputTree->Branch("offCSVJets_num", &nCSVOffJetsOUT, "offCSVJets_num/I");
  TBranch *offCSVpt = outputTree->Branch("offCSVJets_pt", &offCSV_ptOUT, "offCSVJets_pt[offCSVJets_num]/F");
  TBranch *offCSVeta = outputTree->Branch("offCSVJets_eta", &offCSV_etaOUT, "offCSVJets_eta[offCSVJets_num]/F");
  TBranch *offCSVcsv = outputTree->Branch("offCSVJets_csv", &offCSV_csvOUT, "offCSVJets_csv[offCSVJets_num]/F");
  TBranch *offCSVdeepcsv = outputTree->Branch("offCSVJets_deepcsv", &offCSV_deepcsvOUT, "offCSVJets_deepcsv[offCSVJets_num]/F");
  TBranch *offCSVdeepcsvb = outputTree->Branch("offCSVJets_deepcsv_b", &offCSV_deepcsv_bOUT, "offCSVJets_deepcsv_b[offCSVJets_num]/F");
  TBranch *offCSVdeepcsvbb = outputTree->Branch("offCSVJets_deepcsv_bb", &offCSV_deepcsv_bbOUT, "offCSVJets_deepcsv_bb[offCSVJets_num]/F");
  TBranch *offCSVlID = outputTree->Branch("offCSVJets_passesLooseID", &offCSV_LooseIDOUT, "offCSVJets_passesLooseID[offCSVJets_num]/I");
  TBranch *offCSVtID = outputTree->Branch("offCSVJets_passesTightID",&offCSV_TightIDOUT,"offCSVJets_passesTightID[offCSVJets_num]/I");
  TBranch *offCSVtlID = outputTree->Branch("offCSVJets_passesTightLeptVetoID", &offCSV_TightLepIDOUT,"offCSVJets_passesTightLeptVetoID[offCSVJets_num]/I");
  TBranch *offCSVmatchPF = outputTree->Branch("offCSVJets_matchPF",&offCSV_matchPFOUT, "offCSVJets_matchPF[offCSVJets_num]/I");
  TBranch *offCSVmatchCalo = outputTree->Branch("offCSVJets_matchCalo",&offCSV_matchCaloOUT, "offCSVJets_matchCalo[offCSVJets_num]/I");
  TBranch *offCSVmcF = outputTree->Branch("offCSVJets_mcFlavour",&offCSV_mcFlavourOUT, "offCSVJets_mcFlavour[offCSVJets_num]/I");
  TBranch *offCSVmatchGen = outputTree->Branch("offCSVJets_machGen",&offCSV_matchGenOUT, "offCSVJets_matchGen[offCSVJets_num]/I");
  TBranch *offCSVrankpt = outputTree->Branch("offCSVJets_rankpt",&offCSV_rankptOUT, "offCSVJets_rankpt[offCSVJets_num]/I");


  long nEvents = InputChain->GetEntries();
  for (long i = 0; i < nEvents; i++){
    cout << "processing event: " <<  i << endl;
    //if(i == 10){ break; };
    InputChain->GetEvent(i);

    nCSVOffJetsOUT = nOffJets;
    nDeepCSVOffJetsOUT = nOffJets;
    nOffJetsOUT = nOffJets;

    cout << "Number of offline Jets: " << nOffJets << " " << endl;
    for (int j = 0; j < nOffJets; j++){

      if (i == 0){ cout << "Processing Jet: " << j << endl; }
      if (i == 0 and j == 0){ cout << "Setting pt: " << endl; }
      off_ptOUT[j] = off_pt[j];
      if (i == 0 and j == 0){ cout << "Setting eta: " << endl; }
      off_etaOUT[j] = off_eta[j];
      off_csvOUT[j] = off_csv[j];
      if (i == 0 and j == 0){ cout << "Setting deepCSV: " << endl; }
      off_deepcsvOUT[j] = off_deepcsv_b[j] + off_deepcsv_bb[j];
      if (i == 0 and j == 0){ cout << "Saving b and bb deepCSV: " << endl; }
      off_deepcsv_bOUT[j] = off_deepcsv_b[j];
      off_deepcsv_bbOUT[j] = off_deepcsv_bb[j];
      off_LooseIDOUT[j] = off_LooseID[j];
      off_TightIDOUT[j] = off_TightID[j];
      off_TightLepIDOUT[j] = off_TightLepID[j];
      //off_matchPFOUT[j] = off_matchPF[j];
      //off_matchCaloOUT[j] = off_matchCalo[j];
      off_matchGenOUT[j] = -1;
      off_rankCSVOUT[j] = off_rankCSV[j];
      if (i == 0 and j == 0){ cout << "Setting gen match: " << endl; }
      if (off_matchGen[j] != -1 and !data){
	off_mcFlavourOUT[j] = gen_mcF[off_matchGen[j]];
      }
      else {
	off_mcFlavourOUT[j] = -1;
      }

      if (i == 0 and j == 0){ cout << "Setting PF and Calo matching: " << endl; }
      //PF and Calo Matching
      off_matchPFOUT[j] = -1;
      for (int pfj = 0; pfj < nPFJets; pfj++){
	if (pf_matchOff[pfj] == j){
	  off_matchPFOUT[j] = pfj;
	}
      }
      off_matchCaloOUT[j] = -1;
      for (int caloj = 0; caloj < nCaloJets; caloj++){
	if (calo_matchOff[caloj] == j){
	  off_matchCaloOUT[j] = caloj;
	}
      }	     
    }
    off_i1CSVOUT = off_i1CSV;
    off_i2CSVOUT = off_i2CSV;
    off_i3CSVOUT = off_i3CSV;
    off_i4CSVOUT = off_i4CSV;

    if (i == 0){ cout << "Getting CSV and DeepCSV order: " << endl; }
    map<float, int, greater<float>> CSVlist;
    map<float, int, greater<float>> DeepCSVlist;

    for (int j = 0; j < nOffJetsOUT; j++){
      CSVlist[off_csvOUT[j]] = j;
      DeepCSVlist[off_deepcsvOUT[j]] = j;
    }

    
    map<float, int>::iterator it = DeepCSVlist.begin();
    if(nOffJetsOUT >= 1){
      cout << "0 DeepCSV" << it->first << " " << it->second << endl;
      off_i1DeepCSVOUT = it->second;      
    }
    if(nOffJetsOUT >= 2){
      it++;
      cout << "1 DeepCSV" << it->first << " " << it->second << endl;
      off_i2DeepCSVOUT = it->second;      
    }
    if(nOffJetsOUT >= 3){
      it++;
      cout << "2 DeepCSV" << it->first << " " << it->second << endl;
      off_i3DeepCSVOUT = it->second;      
    }
    if(nOffJetsOUT >= 4){
      it++;
      cout << "3 DeepCSV" << it->first << " " << it->second << endl;
      off_i4DeepCSVOUT = it->second;      
    }
    
    int inew = 0;
    for(auto elem : CSVlist){
      int ijet = elem.second;
      
      offCSV_ptOUT[inew] = off_pt[ijet];
      offCSV_etaOUT[inew] = off_eta[ijet];
      offCSV_csvOUT[inew] = off_csv[ijet];
      offCSV_deepcsvOUT[inew] = off_deepcsv_b[ijet] + off_deepcsv_bb[ijet];
      offCSV_deepcsv_bOUT[inew] = off_deepcsv_b[ijet];
      offCSV_deepcsv_bbOUT[inew] = off_deepcsv_bb[ijet];
      offCSV_LooseIDOUT[inew] = off_LooseID[ijet];
      offCSV_TightIDOUT[inew] = off_TightID[ijet];
      offCSV_TightLepIDOUT[inew] = off_TightLepID[ijet];
      offCSV_matchPFOUT[inew] = off_matchPFOUT[ijet];
      offCSV_matchCaloOUT[inew] = off_matchCaloOUT[ijet];
      offCSV_mcFlavourOUT[inew] = off_mcFlavourOUT[ijet];
      offCSV_matchGenOUT[inew] = -1;
      offCSV_rankptOUT[inew] = ijet;
      inew++;
    }

    inew = 0;
    for(auto elem : DeepCSVlist){
      int ijet = elem.second;
      
      offDeepCSV_ptOUT[inew] = off_pt[ijet];
      offDeepCSV_etaOUT[inew] = off_eta[ijet];
      offDeepCSV_csvOUT[inew] = off_csv[ijet];
      offDeepCSV_deepcsvOUT[inew] = off_deepcsv_b[ijet] + off_deepcsv_bb[ijet];
      offDeepCSV_deepcsv_bOUT[inew] = off_deepcsv_b[ijet];
      offDeepCSV_deepcsv_bbOUT[inew] = off_deepcsv_bb[ijet];
      offDeepCSV_LooseIDOUT[inew] = off_LooseID[ijet];
      offDeepCSV_TightIDOUT[inew] = off_TightID[ijet];
      offDeepCSV_TightLepIDOUT[inew] = off_TightLepID[ijet];
      offDeepCSV_matchPFOUT[inew] = off_matchPFOUT[ijet];
      offDeepCSV_matchCaloOUT[inew] = off_matchCaloOUT[ijet];
      offDeepCSV_mcFlavourOUT[inew] = off_mcFlavourOUT[ijet];
      offDeepCSV_matchGenOUT[inew] = -1;
      offDeepCSV_rankptOUT[inew] = ijet;
      //Set DeepCSV rank for pt ordered jets
      off_rankDeepCSVOUT[ijet] = inew;
      inew++;
    }
    cout << "Filling pt ordered branches" << endl;
    offnum->Fill();
    offpt->Fill();
    offeta->Fill();
    offcsv->Fill();
    offdeepcsv->Fill();
    offdeepcsvb->Fill();
    offdeepcsvbb->Fill();
    offlID->Fill();
    offtID->Fill();
    offtlID->Fill();
    off1CSV->Fill();
    off2CSV->Fill();
    off3CSV->Fill();
    off4CSV->Fill();
    off1DeepCSV->Fill();
    off2DeepCSV->Fill();
    off3DeepCSV->Fill();
    off4DeepCSV->Fill();
    offmatchPF->Fill();
    offmatchCalo->Fill();
    offmcF->Fill();
    offmatchGen->Fill();
    offrankCSV->Fill();
    offrankDeepCSV->Fill();
    
    cout << "Filling csv ordered branches" << endl;
    offDeepCSVnum->Fill();
    offDeepCSVpt->Fill();
    offDeepCSVeta->Fill();
    offDeepCSVcsv->Fill();
    offDeepCSVdeepcsv->Fill();
    offDeepCSVdeepcsvb->Fill();
    offDeepCSVdeepcsvbb->Fill();
    offDeepCSVlID->Fill();
    offDeepCSVtID->Fill();
    offDeepCSVtlID->Fill();
    offDeepCSVmatchPF->Fill();
    offDeepCSVmatchCalo->Fill();
    offDeepCSVmcF->Fill();
    offDeepCSVmatchGen->Fill();
    offDeepCSVrankpt->Fill();
    
    cout << "Filling deepcvs ordered branches" << endl;
    offCSVnum->Fill();
    offCSVpt->Fill();
    offCSVeta->Fill();
    offCSVcsv->Fill();
    offCSVdeepcsv->Fill();
    offCSVdeepcsvb->Fill();
    offCSVdeepcsvbb->Fill();
    offCSVlID->Fill();
    offCSVtID->Fill();
    offCSVtlID->Fill();
    offCSVmatchPF->Fill();
    offCSVmatchCalo->Fill();
    offCSVmcF->Fill();
    offCSVmatchGen->Fill();
    offCSVrankpt->Fill();

  }

  
  outputFile->Write();

}
