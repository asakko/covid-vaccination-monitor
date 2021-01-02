import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

from utils import *

def lambda_handler(event, context):
    
    try:
        df = load_data()
        max_values = df.groupby('location').max('total_vaccinations_per_hundred').sort_values('total_vaccinations_per_hundred', ascending=False).reset_index(drop=False)
        print(','.join(sorted(df.location.unique().tolist())))
    except:
        warnings.warn('Cannot read vaccination data to pandas dataframe!')
        sys.exit(1)
    
    ## Main countries
    try:
        cmap = OrderedDict({k:main_country_vs_color[k] for k in [x for x in max_values.location if x in main_country_vs_color.keys()]})
        print('Main countries:     ', ",".join(list(cmap.keys())))
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize = (8, 5))
        plot_chart(ax, df[df.location.isin(cmap.keys())], cmap, 20)
        plt.tight_layout()
        plt.savefig('/tmp/main_countries.png', dpi=160)
    except:
        warnings.warn('Cannot plot main countries chart!')
        sys.exit(1)
        
        
    ## European countries
    try:
        cmap = OrderedDict({k:european_country_vs_color[k] for k in [x for x in max_values.location if x in european_country_vs_color.keys()]})
        print('European countries: ', ",".join(list(cmap.keys())))
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize = (8, 5))
        plot_chart(ax, df[df.location.isin(cmap.keys())], cmap, 20)
        plt.tight_layout()
        plt.savefig('/tmp/european_countries.png', dpi=160)
    except:
        warnings.warn('Cannot plot European countries chart!')
        sys.exit(1)

    return {
        'statusCode': 200,
        'body': json.dumps('my-test-lambda-function-01 completed!')
    }

if __name__ == "__main__":
    lambda_handler(None, None)