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


float get_puWeight_CD(float x){
  std::map<int, float> weights;
  /* Run C+D */
  weights[0] = 3.92524999357e-06;
  weights[1] = 1.10028909832e-05;
  weights[2] = 1.90667164898e-05;
  weights[3] = 7.04997943604e-05;
  weights[4] = 0.000100120920656;
  weights[5] = 0.00012874701489;
  weights[6] = 0.000167872274428;
  weights[7] = 0.000182245889329;
  weights[8] = 0.000202097880155;
  weights[9] = 0.000255426783251;
  weights[10] = 0.000399594873343;
  weights[11] = 0.000836891480933;
  weights[12] = 0.0019437401574;
  weights[13] = 0.00417270931327;
  weights[14] = 0.00773118748445;
  weights[15] = 0.0125942711947;
  weights[16] = 0.0188295443809;
  weights[17] = 0.025962998839;
  weights[18] = 0.0324313358291;
  weights[19] = 0.0375173903032;
  weights[20] = 0.0414851148076;
  weights[21] = 0.044142354439;
  weights[22] = 0.0454932471454;
  weights[23] = 0.0464621205276;
  weights[24] = 0.0479052051417;
  weights[25] = 0.0499071141356;
  weights[26] = 0.0519870178118;
  weights[27] = 0.053552537657;
  weights[28] = 0.0542001904214;
  weights[29] = 0.0536745083294;
  weights[30] = 0.0518445655889;
  weights[31] = 0.0488052286312;
  weights[32] = 0.0448476506942;
  weights[33] = 0.0403006932348;
  weights[34] = 0.0354402020398;
  weights[35] = 0.0304992870761;
  weights[36] = 0.0256887947697;
  weights[37] = 0.0211850239902;
  weights[38] = 0.0171130193546;
  weights[39] = 0.0135418747843;
  weights[40] = 0.0104956399517;
  weights[41] = 0.00796619101839;
  weights[42] = 0.00592172056075;
  weights[43] = 0.00431345332164;
  weights[44] = 0.0030817133643;
  weights[45] = 0.00216219625025;
  weights[46] = 0.00149188996669;
  weights[47] = 0.00101366229213;
  weights[48] = 0.000678965228716;
  weights[49] = 0.000448699085339;
  weights[50] = 0.000292713753019;
  weights[51] = 0.000188552403307;
  weights[52] = 0.000119942165141;
  weights[53] = 7.53495457764e-05;
  weights[54] = 4.67500486365e-05;
  weights[55] = 2.8650927116e-05;
  weights[56] = 1.73491785406e-05;
  weights[57] = 1.03852489914e-05;
  weights[58] = 6.14983436462e-06;
  weights[59] = 3.60600406405e-06;
  weights[60] = 0.0;
  weights[61] = 0.0;
  weights[62] = 0.0;
  weights[63] = 0.0;
  weights[64] = 0.0;
  weights[65] = 0.0;
  weights[66] = 0.0;
  weights[67] = 0.0;
  weights[68] = 0.0;

  for(auto elem : weights){
    if(x >= elem.first && x < (elem.first + 1)){
      return elem.second;
    }
  }
  return 0.0;
}



float get_puWeight_E(float x){
  std::map<int, float> weights;
  /* Run E */
  weights[0] = 9.58220322691e-09;
  weights[1] = 0.00176914031212;
  weights[2] = 0.0411712048187;
  weights[3] = 0.0373946649003;
  weights[4] = 0.07100405072;
  weights[5] = 0.0784540073009;
  weights[6] = 0.0871088498111;
  weights[7] = 0.192054873371;
  weights[8] = 0.116546210838;
  weights[9] = 0.127007580113;
  weights[10] = 0.0759412569132;
  weights[11] = 0.128999839786;
  weights[12] = 0.204241371828;
  weights[13] = 0.281624585913;
  weights[14] = 0.294711325094;
  weights[15] = 0.386372018003;
  weights[16] = 0.444168248635;
  weights[17] = 0.478387109889;
  weights[18] = 0.65140108071;
  weights[19] = 0.718439661178;
  weights[20] = 0.822854854343;
  weights[21] = 0.869219145748;
  weights[22] = 0.969796310161;
  weights[23] = 0.95348500653;
  weights[24] = 0.966017642342;
  weights[25] = 0.970498305098;
  weights[26] = 0.953581353641;
  weights[27] = 0.964617198517;
  weights[28] = 0.968137051101;
  weights[29] = 1.01187562253;
  weights[30] = 1.07052603321;
  weights[31] = 1.07978679135;
  weights[32] = 1.0748960807;
  weights[33] = 1.1311107252;
  weights[34] = 1.12229858354;
  weights[35] = 1.12950491824;
  weights[36] = 1.20068263606;
  weights[37] = 1.25112174579;
  weights[38] = 1.24029026697;
  weights[39] = 1.28767764939;
  weights[40] = 1.33036461855;
  weights[41] = 1.33864884997;
  weights[42] = 1.43164848983;
  weights[43] = 1.65924829331;
  weights[44] = 1.80290640559;
  weights[45] = 1.86683217277;
  weights[46] = 1.90382210293;
  weights[47] = 1.91432857589;
  weights[48] = 1.80568995546;
  weights[49] = 1.79628566672;
  weights[50] = 1.65360845333;
  weights[51] = 1.48478510101;
  weights[52] = 1.30465621136;
  weights[53] = 1.13720483007;
  weights[54] = 0.935297114209;
  weights[55] = 0.791956198987;
  weights[56] = 0.649962393186;
  weights[57] = 0.531224328903;
  weights[58] = 0.435764935597;
  weights[59] = 0.359171234179;
  weights[60] = 0.303747344991;
  weights[61] = 0.258326636608;
  weights[62] = 0.240637923859;
  weights[63] = 0.223829879358;
  weights[64] = 0.217871129576;
  weights[65] = 0.18456978578;
  weights[66] = 0.150404200685;
  weights[67] = 0.138807854673;
  weights[68] = 0.131302860808;
  weights[69] = 0.0836773067277;
  weights[70] = 0.0836267720942;
  weights[71] = 0.0549310867477;
  weights[72] = 0.0837026724996;
  weights[73] = 0.0884154380156;
  weights[74] = 0.0637557939233;
  weights[75] = 0.0642247128376;
  weights[76] = 0.056182564714;
  weights[77] = 0.0726338183597;
  weights[78] = 0.0677407758536;
  weights[79] = 0.0512202818497;
  weights[80] = 0.00780203850674;
  weights[81] = 0.0630480405644;
  weights[82] = 0.0398852712099;
  weights[83] = 0.0300151063756;
  weights[84] = 0.000274327770076;
  weights[85] = 0.0574368222523;
  weights[86] = 0.011680059235;
  weights[87] = 0.0;
  weights[88] = 0.0126746371787;
  weights[89] = 0.0;
  weights[90] = 0.0;
  weights[91] = 0.0;
  weights[92] = 0.0;
  weights[93] = 0.0;
  weights[94] = 0.0;
  weights[95] = 0.0;
  weights[96] = 0.0;
  weights[97] = 0.0;
  weights[98] = 0.0;

  for(auto elem : weights){
    if(x >= elem.first && x < (elem.first + 1)){
      return elem.second;
    }
  }
  return 0.0;
}


float get_puWeight_F(float x){
  std::map<int, float> weights;
  /* Run F */
  weights[0] = 0.000860796770742;
  weights[1] = 0.0565521053537;
  weights[2] = 0.347182425768;
  weights[3] = 0.265703542667;
  weights[4] = 0.123504541957;
  weights[5] = 0.123743229714;
  weights[6] = 0.11704706388;
  weights[7] = 0.16094774575;
  weights[8] = 0.181667213194;
  weights[9] = 0.837942677354;
  weights[10] = 0.819551189996;
  weights[11] = 1.09161932301;
  weights[12] = 0.953034586101;
  weights[13] = 0.686789820342;
  weights[14] = 0.439118890517;
  weights[15] = 0.411037463167;
  weights[16] = 0.386722844364;
  weights[17] = 0.352949369406;
  weights[18] = 0.411386414275;
  weights[19] = 0.400833318956;
  weights[20] = 0.437736429967;
  weights[21] = 0.488368174377;
  weights[22] = 0.604370621337;
  weights[23] = 0.647278573555;
  weights[24] = 0.685667830447;
  weights[25] = 0.699357686813;
  weights[26] = 0.684857111612;
  weights[27] = 0.677821615952;
  weights[28] = 0.656001559226;
  weights[29] = 0.658960273137;
  weights[30] = 0.673963167102;
  weights[31] = 0.664433403329;
  weights[32] = 0.655768935377;
  weights[33] = 0.69399208115;
  weights[34] = 0.70060676108;
  weights[35] = 0.724462507966;
  weights[36] = 0.798298274979;
  weights[37] = 0.867555192742;
  weights[38] = 0.897639307317;
  weights[39] = 0.96907297712;
  weights[40] = 1.03768563407;
  weights[41] = 1.0853852341;
  weights[42] = 1.22159201763;
  weights[43] = 1.52083621108;
  weights[44] = 1.81766690757;
  weights[45] = 2.11335037265;
  weights[46] = 2.45169852784;
  weights[47] = 2.81520649801;
  weights[48] = 3.01891629846;
  weights[49] = 3.37761333921;
  weights[50] = 3.44517390669;
  weights[51] = 3.36843740111;
  weights[52] = 3.16238886288;
  weights[53] = 2.88912078291;
  weights[54] = 2.4440814124;
  weights[55] = 2.09057151959;
  weights[56] = 1.70448107588;
  weights[57] = 1.36368650421;
  weights[58] = 1.08174715921;
  weights[59] = 0.854511615802;
  weights[60] = 0.689143103262;
  weights[61] = 0.558824979043;
  weights[62] = 0.499089475671;
  weights[63] = 0.450473776502;
  weights[64] = 0.43370490858;
  weights[65] = 0.373039045345;
  weights[66] = 0.318731677473;
  weights[67] = 0.319746822738;
  weights[68] = 0.341142188861;
  weights[69] = 0.253866105211;
  weights[70] = 0.305280858757;
  weights[71] = 0.247163471012;
  weights[72] = 0.472700958387;
  weights[73] = 0.634837515304;
  weights[74] = 0.587172302608;
  weights[75] = 0.763146166442;
  weights[76] = 0.864667689166;
  weights[77] = 1.45170042909;
  weights[78] = 1.76171952659;
  weights[79] = 1.73624318445;
  weights[80] = 0.34528050918;
  weights[81] = 3.64907624009;
  weights[82] = 3.02474212987;
  weights[83] = 2.98859752056;
  weights[84] = 0.0359416758103;
  weights[85] = 9.92466185706;
  weights[86] = 2.66803041849;
  weights[87] = 0.0;
  weights[88] = 5.09579024475;
  weights[89] = 0.0;
  weights[90] = 0.0;
  weights[91] = 0.0;
  weights[92] = 0.0;
  weights[93] = 0.0;
  weights[94] = 0.0;
  weights[95] = 0.0;
  weights[96] = 0.0;
  weights[97] = 0.0;
  weights[98] = 0.0;

  for(auto elem : weights){
    if(x >= elem.first && x < (elem.first + 1)){
      return elem.second;
    }
  }
  return 0.0;
}





float get_puWeight_CD_old(float x){
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







float get_puWeight_C_ReReco(float x){
  std::map<int, float> weights;
  /* Run C */
  weights[-1] = 0.0;
  weights[0] = 0.00027834123043;
  weights[1] = 0.0133448789389;
  weights[2] = 0.0283759203344;
  weights[3] = 0.0767076635737;
  weights[4] = 0.125677077009;
  weights[5] = 0.0835070881354;
  weights[6] = 0.10831509361;
  weights[7] = 0.250987841037;
  weights[8] = 0.180218284944;
  weights[9] = 0.277307209862;
  weights[10] = 0.229621584119;
  weights[11] = 0.447849140975;
  weights[12] = 0.79598671161;
  weights[13] = 1.2597211484;
  weights[14] = 1.44643809183;
  weights[15] = 1.88834324126;
  weights[16] = 1.95317427632;
  weights[17] = 1.76147744774;
  weights[18] = 1.96002783272;
  weights[19] = 1.79340929863;
  weights[20] = 1.77427200928;
  weights[21] = 1.69600836807;
  weights[22] = 1.78080621768;
  weights[23] = 1.70230681779;
  weights[24] = 1.72421221304;
  weights[25] = 1.76088999617;
  weights[26] = 1.75898404908;
  weights[27] = 1.78432041116;
  weights[28] = 1.75757074738;
  weights[29] = 1.75892311264;
  weights[30] = 1.73818838659;
  weights[31] = 1.60109372202;
  weights[32] = 1.42864737391;
  weights[33] = 1.32779382224;
  weights[34] = 1.14827596344;
  weights[35] = 0.992368427996;
  weights[36] = 0.889285620171;
  weights[37] = 0.764241363865;
  weights[38] = 0.610046330694;
  weights[39] = 0.497691989145;
  weights[40] = 0.394586241791;
  weights[41] = 0.297944868274;
  weights[42] = 0.234186553857;
  weights[43] = 0.195721070167;
  weights[44] = 0.150789434483;
  weights[45] = 0.109143854131;
  weights[46] = 0.0769587606728;
  weights[47] = 0.0531191417816;
  weights[48] = 0.0342792590543;
  weights[49] = 0.023338121191;
  weights[50] = 0.0147549987553;
  weights[51] = 0.00915159297556;
  weights[52] = 0.00559544477684;
  weights[53] = 0.00342063539075;
  weights[54] = 0.00198843962709;
  weights[55] = 0.0011984233626;
  weights[56] = 0.000704202169072;
  weights[57] = 0.00041392013874;
  weights[58] = 0.000244886738145;
  weights[59] = 0.000145766824776;
  weights[60] = 8.90172039288e-05;
  weights[61] = 5.45994563883e-05;
  weights[62] = 3.66022565405e-05;
  weights[63] = 2.44333896738e-05;
  weights[64] = 1.70140924102e-05;
  weights[65] = 1.02758802061e-05;
  weights[66] = 5.94813213409e-06;
  weights[67] = 3.8842490976e-06;
  weights[68] = 2.58889877618e-06;
  weights[69] = 1.15716512525e-06;
  weights[70] = 8.06978968762e-07;
  weights[71] = 3.67791409729e-07;
  weights[72] = 3.86428365933e-07;
  weights[73] = 2.79532263051e-07;
  weights[74] = 1.37023485291e-07;
  weights[75] = 9.30997367335e-08;
  weights[76] = 5.44826801875e-08;
  weights[77] = 4.67223597528e-08;
  weights[78] = 2.86547351404e-08;
  weights[79] = 1.41227893333e-08;
  weights[80] = 1.38979661942e-09;
  weights[81] = 7.19092460677e-09;
  weights[82] = 2.88655330491e-09;
  weights[83] = 1.36592230256e-09;
  weights[84] = 7.77889859873e-12;
  weights[85] = 1.00558509164e-09;
  weights[86] = 1.25096910399e-10;
  weights[87] = 0.0;
  weights[88] = 4.94020212672e-11;
  weights[89] = 0.0;
  weights[90] = 0.0;
  weights[91] = 0.0;
  weights[92] = 0.0;
  weights[93] = 0.0;
  weights[94] = 0.0;
  weights[95] = 0.0;
  weights[96] = 0.0;
  weights[97] = 0.0;
  weights[98] = 0.0;
  for(auto elem : weights){
    if(x >= elem.first && x < (elem.first + 1)){
      return elem.second;
    }
  }
  return 0.0;
}
