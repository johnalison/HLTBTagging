#include <algorithm>
#include <map>
#include "TLorentzVector.h"


int leptonoverlap(float jetpt, float jeteta, float jetphi, float lpt, float leta, float lphi){
  int ret = 0;

  TLorentzVector jetvec;
  TLorentzVector lvec;

  jetvec.SetPtEtaPhiE(jetpt,jeteta,jetphi,jetpt);
  lvec.SetPtEtaPhiE(lpt,leta,lphi,0);

  if (jetvec.DeltaR(lvec) < 0.4){
    ret = 1;
  }
  
  return ret;
}


float get_puWeight(float x){
  std::map<int, float> weights;
  /* RUN C
  weights[28] = 1.59325393696;
  weights[29] = 1.58848124052;
  weights[30] = 1.59663957708;
  weights[31] = 1.53420548465;
  weights[32] = 1.45334574869;
  weights[33] = 1.33527100019;
  weights[34] = 1.22305173306;
  weights[35] = 1.07210772553;
  weights[36] = 0.928622457055;
  weights[37] = 0.784112902621;
  weights[38] = 0.639775855346;
  weights[39] = 0.510899959118;
  weights[40] = 0.398125899913;
  weights[41] = 0.307638150965;
  weights[42] = 0.226780603297;
  weights[43] = 0.165002601938;
  weights[44] = 0.119874549669;
  weights[45] = 0.0850144955442;
  weights[46] = 0.058701799521;
  weights[47] = 0.0396452237318;
  weights[48] = 0.027043574489;
  weights[49] = 0.0180313149026;
  weights[50] = 0.011954666911;
  weights[51] = 0.0075585257186;
  weights[52] = 0.00483521022938;
  weights[53] = 0.00306711666495;
  weights[54] = 0.00187439307028;
  weights[55] = 0.00113450037439;
  weights[56] = 0.000674138516539;
  weights[57] = 0.000397886601771;
  weights[58] = 0.000230415739527;
  weights[59] = 0.000127235103689;
  weights[60] = 6.99241636028e-05;
  weights[61] = 3.76306306638e-05;
  weights[62] = 2.00694144054e-05;
  */
  /* Run C+D */
  weights[28] = 1.72375464547;
  weights[29] = 1.70234624672;
  weights[30] = 1.67898927145;
  weights[31] = 1.5709301302;
  weights[32] = 1.44227861083;
  weights[33] = 1.28261844458;
  weights[34] = 1.13856486227;
  weights[35] = 0.970131952128;
  weights[36] = 0.820299156667;
  weights[37] = 0.679652102106;
  weights[38] = 0.546960288493;
  weights[39] = 0.432709700227;
  weights[40] = 0.335079999964;
  weights[41] = 0.257704424199;
  weights[42] = 0.189141874398;
  weights[43] = 0.136952256861;
  weights[44] = 0.0989379626558;
  weights[45] = 0.069722218319;
  weights[46] = 0.0478156486007;
  weights[47] = 0.0320694686846;
  weights[48] = 0.0217286992077;
  weights[49] = 0.0143980044245;
  weights[50] = 0.00949583164223;
  weights[51] = 0.00598136443831;
  weights[52] = 0.00382023038724;
  weights[53] = 0.00242671001828;
  weights[54] = 0.00149099797485;
  weights[55] = 0.000911850507363;
  weights[56] = 0.00055086489353;
  weights[57] = 0.000333005323233;
  weights[58] = 0.000199255906583;
  weights[59] = 0.000114859267136;
  weights[60] = 0.0;
  weights[61] = 0.0;
  weights[62] = 0;
  weights[63] = 0;

  for(auto elem : weights){
    if(x >= elem.first && x < (elem.first + 1)){
      return elem.second;
    }
  }
  return 0.0;
}


