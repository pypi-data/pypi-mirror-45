# intake_geopandas

[![Build Status](https://travis-ci.com/informatics-lab/intake_geopandas.svg?branch=master)](https://travis-ci.com/informatics-lab/intake_geopandas)

intake_geopandas: [Geopandas](http://geopandas.org/) plugin for [Intake](https://github.com/informatics-lab/intake_geopandas)

See [Intake docs](https://intake.readthedocs.io/en/latest/overview.html).

In `intake_geopandas`, there are plugins provided for reading geospatial datasets into a geopandas dataframe.
It currently supports reading from the following data sources:
  - GeoJSON files
  - PostGIS databases
  - ESRI Shapefiles
  - Spatialite databases

### Installation

The conda install instructions are:

```
conda install -c informaticslab -c intake intake_geopandas
```
