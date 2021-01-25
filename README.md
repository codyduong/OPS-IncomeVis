# OPS-IncomeVis (v1.0.1)
A side project to practice data viz of employee income from publicly available info. 

Employee list retrieved [here](https://www.olatheschools.org/domain/50) and saved as directory.mhtml.

The data is scraped using [csvCreator.py](csvCreator/csvCreator.py) which takes approximately ~.5 seconds a search over 2000 searches results in ~15 minute
time to gather all the income data. This file does the whole process from processing mthml, accessing govsalaries and processing it, to saving the csv.

The employee positions are extradorinarly wide ranged, and I had to create [categoryCreator.py](csvCreator/categoryCreator.py) in order to
boil it down into the categories seen in the image below. If you're curious how I categorized positions, look in [CAT_KEY.json](csvCreator/CAT_KEY.json)

The CSV of scraped data is [here](income.csv)

Here is the final result created using [vizualizer.py](vizualizer.py):
![IncomeVizualization](income.png)
