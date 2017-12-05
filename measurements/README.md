# Online BTagging measurements

## Plot scripts
The general idea for the plotting is to:
1. Define the sampels you want to use, as **Sample class** (see `modules/classes.py`)
2. Define the PlotObject definit the base properties of the plot, as **PlotBase class** (see `modules/classes.py`)
3. Use a plotting function with the correct type of PlotObject and sample.

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


