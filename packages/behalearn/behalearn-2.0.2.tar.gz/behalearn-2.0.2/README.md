# Machine learning module
Main goal of this application is to prepare data for subsequent 
authentication. This module provides functionality for preprocessing data, 
authentication and visualization. 

Preprocessing part of functionality compute speed related columns, splits data 
into multiple movement segments and compute their length. 

Visualization part provides functionality to display FAR, FRR metrics 
and ROC, DET curves.

This project is part of [Behametrics-learn](http://labss2.fiit.stuba.sk/TeamProject/2018/team04iss-it/) team project 
at [Faculty of Informatics and Information Technologies STU in Bratislava](Faculty of Informatics and Information Technologies STU in Bratislava)

# Installation
The source code is currently hosted on [GitLab](https://gitlab.com/tp-fastar/ML-module).

The easiest way to install behalearn is using ``pip`` :
```
pip install behalearn
```

## Usage
After installation you can easily use module as any other python package, for 
example:
```
from behalearn.features import features_for_segment
```

# Documentation
The official documentation and structure of the module is available on 
[following link](https://tp-fastar.gitlab.io/ML-module/).

# License
Source code is provided under [**MIT License**](/LICENSE).