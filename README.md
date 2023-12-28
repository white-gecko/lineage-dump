# RDF Export of the LineageOS Wiki and Stats

This dataset combines the device information from the [LineageOS Wiki](https://wiki.lineageos.org/devices/) with the current [usage statistics](https://stats.lineageos.org/).

## Usage

To use the data you need to import it into a Triple Store.
For instance you can use the [Quit Store](https://github.com/AKSW/QuitStore).
Download a [binary](https://github.com/AKSW/QuitStore/releases) change to this directory and execute:

```
quit -t .
```

Now you should find a query endpoint at `http://localhost:5000/sparql`.

## Queries

Now you can execute queries like:


**Most recent popular devices**

```sparql
PREFIX lins: <https://wiki.lineageos.org/devices/schema#>

SELECT * WHERE {
 GRAPH <https://wiki.lineageos.org/devices/> {
  ?sub a lins:Mobile ;
       lins:release ?release ;
       lins:usage_stat ?stats ;
       lins:current_branch ?current_branch .
    filter (?stats > 5000)
 }
}
ORDER BY DESC(?current_branch) DESC(?release) DESC(?stats)
LIMIT 100
```

## Extraction Process

To run this script you need to clone the lineage wiki into a separate directory so that you have the following directory setup:

- lineage-rdf
  - data <this directory>
  - lineage_wiki
    - _data
      - devices
      - …
    - …

The easiest is to execute the commands with `task` (https://taskfile.dev/).

Run the following to start

```
task repo:init
task install
task extract
```

To re-run the extraction to:

```
$ task repo:update
$ task extract
