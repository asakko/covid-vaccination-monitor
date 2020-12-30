import requests
import altair as alt
import numpy as np
import pandas as pd
import sys
import warnings

from collections import OrderedDict 
from datetime import datetime, timezone
from io import StringIO

def plot_chart(df, cmap):
    return alt.Chart(df[df.location.isin(cmap.keys())]).mark_line(point=True, strokeWidth=2).encode(
        x       = alt.X('date:T', title='Date'),
        y       = alt.Y('total_vaccinations_per_hundred:Q', title='Vaccinated [%]'),
        color   = alt.Color('location:N', title='Country', scale=alt.Scale(
                domain = list(cmap.keys()),
                range  = list(cmap.values())
        )),    tooltip = ['location', 'date:T', 'total_vaccinations_per_hundred']
    ).configure_point(
        size=50
    ).properties(width=200*1.61, height=200, title=f'Vaccination status {datetime.now().astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M")} (UTC)')

def main():
    try:
        url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'
        r = requests.get(url, allow_redirects=True)
        df = pd.read_csv(StringIO(r.content.decode("utf-8")))[['location', 'date', 'total_vaccinations_per_hundred']]
        max_values = df.groupby('location').max('total_vaccinations_per_hundred').sort_values('total_vaccinations_per_hundred', ascending=False).reset_index(drop=False)
    except:
        warnings.warn('Cannot read vaccination data to pandas dataframe!')
        sys.exit(1)
        
    ## Main countries
    country_vs_color = OrderedDict({
        'Israel':         'lightblue',
        'Bahrain':        'yellow',
        'United Kingdom': 'purple',
        'United States':  'blue',
        'Canada':         'lightgray',
        'China':          'red',
        'Russia':         'brown',
        'European Union': 'orange',
        'Japan':          'gray'
    })
    cmap = OrderedDict({k:country_vs_color[k] for k in [x for x in max_values.location if x in country_vs_color.keys()]})
    print('Main countries:     ', ",".join(list(cmap.keys())))
    chart = plot_chart(df, cmap)
    chart.save('out/main-countries.png')
    
    ## European countries
    country_vs_color = OrderedDict({
        'Portugal': 'green',
        'Denmark': 'red',
        'Lithuania': 'orange',
        'Germany': 'brown',
        'Estonia': 'lightblue',
        'Latvia': 'pink',
        'Italy': 'lightgreen',
        'Poland': 'lightgray',
        'Romania': 'yellow'
    })
    cmap = OrderedDict({k:country_vs_color[k] for k in [x for x in max_values.location if x in country_vs_color.keys()]})
    print('European countries: ', ",".join(list(cmap.keys())))
    chart = plot_chart(df, cmap)
    chart.save('out/european-countries.png')
    
if __name__ == "__main__":
    main()