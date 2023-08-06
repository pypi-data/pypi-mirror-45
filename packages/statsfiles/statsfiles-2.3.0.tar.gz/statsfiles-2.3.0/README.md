
[![Build Status](https://travis-ci.org/ZGCDDoo/statsfiles.svg?branch=master)](https://travis-ci.org/ZGCDDoo/statsfiles)
[![codecov](https://codecov.io/gh/ZGCDDoo/statsfiles/branch/master/graph/badge.svg)](https://codecov.io/gh/ZGCDDoo/statsfiles)
[![Documentation Status](https://readthedocs.org/projects/statsfiles/badge/?version=latest)](https://statsfiles.readthedocs.io/en/latest/?badge=latest)


# Statsfiles
Please consult the bare bones documentation by clicking on the docs badge above.


Statsfiles is a small python module to compute simple statistics (average and means) of similarly named files. This can be usefull for simulations where a program outputs many files with the same name, but with a number appended. 

For exemple, a program that calculated the temperature on a given number of points in a city for each hour would ouput a file called: temperature1.dat, temperature2.dat , etc for each day starting from day 1.
The file would be composed of 24 rows (each hour of the day) and say 10 columns (10 places in the city). To get the average temperature for the year, one needs to do some statistics on these files. This is the usefullness of statsfiles. The previous files which have an array (matrix, i.e numpy) form are called **array_files**. Now if we are interseted in the number of coffees taken by the employeess of this temperature program (for the city broadcasting station),  would be logged in a file called cafe1.dat, cafe2.dat, etc. This file would contain the hour on the first column and the amount of coffee taken of the second column. These type of files are called **obs_files**. The first coulmn is ignored for the statistics, and the statistics for this type of files are saved in json format in the file called **statsobs.json**. 

The output of this module for this previous example is the folder **Stats-${date-time}** with temperature_moy.dat, temperature_et.dat for respectively the average value and the standard deviation, as well as statsobs.json.



## Installation
Simple as :
```bash
pip install statsfiles
```

### Dependencies
This module can run on python >= 3.6. The dependencies will be installed automatically by pip.


## Usage
I recommend taking a look and trying the example. Once this is done, it is quite easy to use it for your own sake. To run the exemple (after Installation):

```bash
    cd example
    python -m statsfiles 1 --file example.yml
```


The example is composed of a simple yaml file (see [pyyaml](https://pyyaml.org/)), that describes the files that will be used for the statistics. Let us explain in detail this yaml file.

### Yaml config file

#### obs_files
The name of the files which have a structure given by k.dat

#### array_files
The files which have a structure of matrices (the temperature files described above).

#### param_files


## README and example under construction.