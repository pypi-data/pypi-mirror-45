![Geomancer Logo](https://storage.googleapis.com/tm-geomancer/assets/header.png)
---

[![PyPI](https://img.shields.io/pypi/v/geomancer.svg?color=brightgreen&style=flat-square)](https://pypi.org/project/geomancer/)
[![Build Status](https://img.shields.io/badge/dynamic/json.svg?color=brightgreen&label=build&query=status&url=https%3A%2F%2Fcloud.drone.io%2Fapi%2Frepos%2Fthinkingmachines%2Fgeomancer%2Fbuilds%2Flatest%3Fref%3Drefs%2Fheads%2Fmaster&style=flat-square)](https://cloud.drone.io/thinkingmachines/geomancer)
[![Read the Docs](https://img.shields.io/readthedocs/geomancer.svg?style=flat-square)](https://geomancer.readthedocs.io/en/latest/)
[![Coveralls github](https://img.shields.io/coveralls/github/thinkingmachines/geomancer.svg?style=flat-square)](https://coveralls.io/github/thinkingmachines/geomancer)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT)

Geomancer is a geospatial feature engineering library. It leverages geospatial
data such as [OpenStreetMap (OSM)](https://www.openstreetmap.org/) alongside a
data warehouse like BigQuery. You can use this to create, share, and iterate
geospatial features for your downstream tasks (analysis, modelling,
visualization, etc.). 

## Features

Geomancer can perform geospatial feature engineering for all types of vector data
(i.e. points, lines, polygons).

- Feature primitives for geospatial feature engineering
- Ability to switch out data warehouses (BigQuery, SQLite, PostgreSQL (*In Progress*))
- Compile and share your features using our SpellBook 

## Setup and Installation

### Installing the library

Geomancer can be installed using `pip`.

```
$ pip install geomancer
```

This will install **all** dependencies for every data-warehouse we support. If
you wish to do this only for a specific warehouse, then you can add an
identifier:

```
$ pip install geomancer[bq] # For BigQuery
$ pip install geomancer[sqlite] # For SQLite
$ pip install geomancer[psql] # For PostgreSQL
```

Alternatively, you can also clone the repository then run `install`.

```
$ git clone https://github.com/thinkingmachines/geomancer.git
$ cd geomancer
$ python setup.py install
```

### Setting up your data warehouse

Geomancer is powered by a geospatial data warehouse: we highly-recommend using
[BigQuery](https://cloud.google.com/bigquery/) as your data warehouse and
[Geofabrik's OSM catalog](https://www.geofabrik.de/data/download.html) as your
source of Points and Lines of interest. 

[![Geomancer architecture](https://storage.googleapis.com/tm-geomancer/assets/architecture.png
)](https://github.com/thinkingmachines/geomancer)

You can see the set-up instructions in [this link](https://geomancer.readthedocs.io/en/latest/setup.html#setting-up-your-data-warehouse)

## Basic Usage

All of the feature engineering functions in Geomancer are called "spells". For
example, you want to get the distance to the nearest supermarket for each
point.

```python
from geomancer.spells import DistanceToNearest

# Load your dataset in a pandas dataframe
# df = load_dataset()

dist_spell = DistanceToNearest(
    "supermarket",
    source_table="ph_osm.gis_osm_pois_free_1",
    feature_name="dist_supermarket",
    dburl="bigquery://project-name",
).cast(df)
```

You can specify the type of filter  using the format `{column}:{filter}`.  By
default, the `column` value is `fclass`. For example, if you wish to look for
roads on a bridge, then pass `bridge:T`:

```python
from geomancer.spells import DistanceToNearest

# Load the dataset in a pandas dataframe
# df = load_dataset()

dist_spell = DistanceToNearest(
    "bridge:T",
    source_table="ph_osm.gis_osm_roads_free_1",
    feature_name="dist_road_bridges",
    dburl="bigquery://project-name",
).cast(df)
```

Compose multiple spells into a "spell book" which you can export as a JSON file.

```python
from geomancer.spells import DistanceToNearest
from geomancer.spellbook import SpellBook

spellbook = SpellBook([
    DistanceToNearest(
        "supermarket",
        source_table="ph_osm.gis_osm_pois_free_1",
        feature_name="dist_supermarket",
        dburl="bigquery://project-name",
    ),
    DistanceToNearest(
        "embassy",
        source_table="ph_osm.gis_osm_pois_free_1",
        feature_name="dist_embassy",
        dburl="bigquery://project-name",
    ),
])
spellbook.to_json("dist_supermarket_and_embassy.json")
```

You can share the generated file so other people can re-use your feature extractions
with their own datasets.

```python
from geomancer.spellbook import SpellBook

# Load the dataset in a pandas dataframe
# df = load_dataset()

spellbook = SpellBook.read_json("dist_supermarket_and_embassy.json")
dist_supermarket_and_embassy = spellbook.cast(df)
```

## Contributing

This project is open for contributors! Contibutions can come in the form of
feature requests, bug fixes, documentation, tutorials and the like! We highly
recommend to file an Issue first before submitting a [Pull
Request](https://help.github.com/en/articles/creating-a-pull-request).

Simply fork this repository and make a Pull Request! We'd definitely appreciate:

- Implementation of new features
- Bug Reports
- Documentation
- Testing

Also, we have a
[CONTRIBUTING](https://github.com/thinkingmachines/geomancer/blob/master/CONTRIBUTING.rst)
and a [CODE_OF_CONDUCT](https://github.com/thinkingmachines/geomancer/blob/master/CODE_OF_CONDUCT.rst),
so please check that one out!

## License

MIT License © 2019, Thinking Machines Data Science
