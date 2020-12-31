import requests
import altair as alt
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
    ).properties(width=300*1.61, height=300, title=f'Vaccination status {datetime.now().astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M")} (UTC)')

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
        'Israel':         '#1A85FF',
        'Bahrain':        '#FEFE62',
        'United Kingdom': '#40B0A6',
        'United States':  '#4B0092',
        'Canada':         '#D35FB7',
        'China':          '#DC3220',
        'Russia':         '#994F00',
        'European Union': '#E66100',
        'Japan':          '#E1BE6A',
        'Australia':      '#000000',
        'India':          '#D35FB7'
    })

    cmap = OrderedDict({k:country_vs_color[k] for k in [x for x in max_values.location if x in country_vs_color.keys()]})
    print('Main countries:     ', ",".join(list(cmap.keys())))
    chart = plot_chart(df, cmap)
    chart.save('out/main-countries.png')
    
    ## European countries
    country_vs_color = OrderedDict({
        'Austria':    '#000000',
        'Bulgaria':   '#004949',
        'Croatia':    '#009292',
        'Denmark':    '#ff6db6',
        'Estonia':    '#ffb6db',
        'France':     '#490092',
        'Germany':    '#006ddb',
        'Greece':     '#b66dff',
        'Hungary':    '#6db6ff',
        'Italy':      '#b6dbff',
        'Latvia':     '#920000',
        'Lithuania':  '#924900',
        'Luxembourg': '#db6d00',
        'Poland':     '#24ff24',
        'Portugal':   '#ffff6d',
        'Romania':    '#000000'
    })

    cmap = OrderedDict({k:country_vs_color[k] for k in [x for x in max_values.location if x in country_vs_color.keys()]})
    print('European countries: ', ",".join(list(cmap.keys())))
    chart = plot_chart(df, cmap)
    chart.save('out/european-countries.png')
    
if __name__ == "__main__":
    main()