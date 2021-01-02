# covid-vaccination-monitor

Reads the latest numbers from the [github repository of Our World in Data](https://github.com/owid/covid-19-data/tree/master/public/data/vaccinations), and creates line charts for two sets of countries:
1. Big countries and forerunners (currently Israel, Bahrain, United Kingdom, United States, Canada, China, Russia, European Union, Japan)
2. Several European countries for which data is available

## Output
![main countries](out/main-countries.png)
![main countries](out/european-countries.png)

## Used python libraries:
* matplotlib, numpy, pandas, requests
see [lambda/requirements.txt](requirements.txt)

## AWS deployment
sdd [lambda/README.md](lambda/README.md)
