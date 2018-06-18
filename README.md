# Fahrradwetter


## 3rd BMVI Datarun 2018

* [Projektpräsentation](/docs/bmvi-datarun-2018/bmvi-datarun-2018-fahrradwetter.pdf)


## Niederschlagsdaten des DWD als Raster mit 1x1 km

* https://www.dwd.de/DE/leistungen/radolan/radolan_info/radolan_radvor_op_komposit_format_pdf.pdf?__blob=publicationFile

### Niederschlagsradar (Vorhersage - 120 Minuten)

* https://opendata.dwd.de/weather/radar/composit/fx/

### Stündliche Niederschlagsdaten (historisch)

* tp://ftp-cdc.dwd.de/pub/CDC/grids_germany/hourly/radolan
* ftp://ftp-cdc.dwd.de/pub/CDC/grids_germany/hourly/radolan/historical/bin

## Python-Library wradlib zur Verarbeitung der RADOLAN Binärdaten

* http://docs.wradlib.org/en/latest/notebooks/radolan.html

## Beispiele

### Ausgabe des RADLOAN Grids als GeoJSON

* [Python Script](/dwd/radar/grid/export-radar-grid.py)
* [Beispiel GeoJSON](/dwd/radar/grid/sample_grid_620_750_645_775.json)