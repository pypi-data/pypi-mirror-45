"""
Script that tests the generation of an overview.html file.
"""

import sys
from pathlib import Path
import pandas as pd
import facetswrapper


def load_data():
    """Load UCI census train and test data into dataframes."""
    features = ["Age", "Workclass", "fnlwgt", "Education", "Education-Num", "Marital Status",
                "Occupation", "Relationship", "Race", "Sex", "Capital Gain", "Capital Loss",
                "Hours per week", "Country", "Target"]
    result = pd.read_csv(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.test",
        names=features,
        sep=r'\s*,\s*',
        skiprows=[0],
        engine='python',
        na_values="?")
    return result


def write_overview_html(data, output_filepath):
    """Generate overview html code and write it in a file."""
    overview_html = facetswrapper.overview.overview_html(data, groupby=["Target", "Sex"])
    with open(output_filepath, 'w') as file:
        file.write(overview_html)


if __name__ == "__main__":
    print("Loading data...  ", end='', flush=True)
    data = load_data()
    print('Done')
    print('Generating HTML page...  ', end='', flush=True)
    output_filepath = Path(sys.argv[0]).with_suffix('.html')
    write_overview_html(data, output_filepath)
    print('Done')







