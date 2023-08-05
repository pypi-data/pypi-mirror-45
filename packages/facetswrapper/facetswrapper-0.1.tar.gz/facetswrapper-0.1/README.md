# facets-wrapper

A wrapper to two visualizations in [Facets](https://pair-code.github.io/facets/), namely Facets Overview and Facets Dive.

## Facets Overview wrapper
* The general idea follows one of the provided [original examples](https://raw.githubusercontent.com/PAIR-code/facets/master/facets_overview/Overview_demo.ipynb).
* The wrapper takes only one dataframe as input, but allows to use optionally a list of columns to perform a groupby. In such a case, the groups of the groupby correspond to the multiple datasets of the original example.
* The CSS of the wrapping HTML page is used to tweak the HTML code returned by facets, in order to accommodate gracefully more than 2 groups of data. A sprinkle of JavaScript is also used to enhance some functionalities.

## Facets Dive wrapper
* Not yet implemented, planned for end of may 2019.