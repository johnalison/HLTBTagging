# Online BTagging measurements

## Plot scripts
The general idea for the plotting is to:
1. Define the sampels you want to use, as **Sample class** (see `modules/classes.py`)
2. Define the PlotObject definit the base properties of the plot, as **PlotBase class** (see `modules/classes.py`)
3. Use a plotting function with the correct type of PlotObject and sample.

All scitps are realized with the python standard logging module. The output level can be set with `--logging` argument. The standard value is 20 (level info). The modules of the plotting scripts can display additional information by setting it to 10 (level debug).   
Setting it to 0 (in words zero) reveals all **ROOT** messages with levels **kPrint, kInfo, kWarning**. Otherwise only **kError, kBreak, kSysError, kFatal** will be shown.

### shapeComparison.py
This scripts produces 
* discriminator shape comparisons (w/ and w/o matching to PF or CaloJets)
* online vs. offline 2D distribution in various combinations

| Flag | Description |
|---------------|----------------------------------------------------------------------------------------------|
| --mc | Run the MC sample |
| --data | Run the Data sample |
| --csv | Produce plots with the CSV discriminator |
| --deepcsv | Produce plots with the DeepCSV discriminator |
| --perJetComp | Produce 2D plots comparing online/offline for the activated discriminator |
| --sameTagger | Produce 2D plots with the same tagger |
| --crossTagger | Produce 2D cross tagger plots. **Both Taggers** need to be activated |
| --nomatch | Also produce discriminator comparisons without requiring PF/Calo jets matched to offline jet |
| --sampleComp | Produce discriminator comparisons between Data and MC sample |
| --skip1DComp | Skip the 1D discriminator comparison plots |


### efficiencies.py
This script produces
* Offline turn-ons for cuts on online values

| Flag        | Description                                          |
|-------------|------------------------------------------------------|
| --mc        | Run the MC sample                                    |
| --data      | Run the Data sample                                  |
| --csv       | Produce plots with the CSV discriminator             |
| --deepcsv   | Produce plots with the DeepCSV discriminator         |
| --csvWP     | Define online cuts for the turn-on for CSV plots     |
| --deepcsvWP | Define online cuts for the turn-on for DeepCSV plots |


### flavourComp.py
This script produces
* inclusive plots of the offline and online tagger distributions
* distributions and estimations for the b-tagging efficiency in ttbar with a Tag&Probe measurement
The MC is split by MC flavour of a matched GenJet.


| Flag        | Description                                                                                |
|-------------|--------------------------------------------------------------------------------------------|
| --data      | Run the MC sample                                                                          |
| --csv       | Produce plots with the CSV discriminator                                                   |
| --deepcsv   | Produce plots with the DeepCSV discriminator                                               |
| --inclusive | Make inclusive plots (all jets)                                                            |
| --TnP       | Run Tag&Probe method for this measurement and output plots                                 |
| --eff       | Run Tag&Probe method for this measurement and output plots, efficiencies for different Was |

Running with `--eff` also saves root files containing distributions (MC and data) used for efficiency calulation. With the script `makePeriodCompFromEff.py` plots/tables comparing the different run periods can be generated.
