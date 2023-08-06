# MHCLovac
MHC binding prediction based on modeled physicochemical properties of peptides.

*__New release - MHCLovac 2.0__*

*__MHCLovac 2.0 makes almost somewhat accurate predictions. 
It really is not precise.__*

* [About](#About)
* [Installation](#Installation)
* [Usage](#Usage)

<hr>

### About 

MHCLovac uses Bayesian linear regression for binding affinity prediction
based on modeled physicochemical properties of peptides.
MHCLovac uses pre-developed [**`proteinko`**](https://github.com/stefs304/proteinko) 
package to obtain modeled distributions of physicochemical properties. 

![modeled_distributions](https://raw.githubusercontent.com/stefs304/proteinko/dev/resources/plot1.png)

Physicochemical properties in question are:
* Hydropathy
* Number of donor hydrogen bonds
* Number of acceptor hydrogen bonds
* Isoelectric point
* Van der Waals molecular volume
 
 Once the distributions are obtained, the area under the curve (AUC) is 
 calculated using a sliding frame technique. The AUC values for each of five
 physicochemical properties are concatenated into single feature vector. 
 
Model training is performed on standardized AUC values. We tested number of 
linear regression models and concluded that BayesianRidge algorithm from `sklearn`
package produces most consistent predictions across various training set 
configurations.

![regression_models](https://raw.githubusercontent.com/stefs304/mhclovac/dev/resources/plots/REGRESSION-MODELS.2019-04-27T21%3A12%3A47.348099.png)

MHCLovac makes modestly accurate predictions, which can be seen on plots below.

![binding_predictions](https://raw.githubusercontent.com/stefs304/mhclovac/dev/resources/plots/BINDING_PREDICTIONS.2019-05-01T13%3A31%3A05.698974.png)
  

### Installation

Install from PyPI repository
```
pip install mhclovac
```

Download and install from git repository
```
git clone https://github.com/stefs304/mhclovac
cd mhclovac
pip install .
```

### Usage
```
mhclovac --fasta <fasta file> 
         --hla <hla type (ex. HLA-A*02:01)> 
         --peptide_length <peptide length>
         --output <output file (optional)>
```
