import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import requests
import sys
import warnings

from collections import OrderedDict 
from datetime import datetime, timezone
from io import StringIO

def load_data():
    url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'
    r = requests.get(url, allow_redirects=True)
    df = pd.read_csv(StringIO(r.content.decode("utf-8")), low_memory=False, parse_dates=['date'])[['location', 'date', 'total_vaccinations_per_hundred']]
    return df

def plot_chart(ax, df, cmap, m:int = 30):
    n = len(df.date.unique())
    min_date, max_date = df.date.min(), df.date.max()
    days = (max_date-min_date).days
    delta = 1+days//m
    dates = [min_date+pd.Timedelta(days=i*delta) for i in range(1+days//delta)]
    
    for loc, color in cmap.items():
        ax.plot('date', 'total_vaccinations_per_hundred', data=df[(df.location==loc) & (~df.total_vaccinations_per_hundred.isna())].sort_values('date'), marker='o', color=color, label=loc)
        
    ax.set_ylabel('Vaccinated [%]')
    ax.legend(loc=2)
    ax.set_xticks(dates)
    ax.set_xticklabels(dates)
    ax.tick_params(axis='x', labelrotation=45)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    
main_country_vs_color = OrderedDict({
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

european_country_vs_color = OrderedDict({
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