"""
Based on https://raw.githubusercontent.com/PAIR-code/facets/master/facets_overview/Overview_demo.ipynb .
"""

# Add the facets overview python code to the python path
import sys

### sys.path.append("./facets_overview_python")

# from pathlib import Path
# print(Path.cwd())

from facets.facets_overview.python.generic_feature_statistics_generator import GenericFeatureStatisticsGenerator
import base64

# import pandas as pandas


OVERVIEW_HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html>
        <head>
            <link rel="import" href="https://raw.githubusercontent.com/PAIR-code/facets/master/facets-dist/facets-jupyter.html" >
            <style>

                .facets-overview-table-0 .chart-column.facets-overview-table {{
                    // width: 280px;
                    // min-width: 280px;
                    min-width: 2000px;
                    // text-align: center;
                }}

                .facets-overview-chart-0 .data-list-small.facets-overview-chart {{
                    // height: 60px;
                    height: unset;
                }}

                .facets-overview-chart-0 .dialog-table.facets-overview-chart {{
                    // clear: left;
                    background-color: lightgreen;
                }}

                .facets-overview-chart-0 .non-overflow-label-cell.facets-overview-chart {{
                    // width: 90px;
                    // max-width: 90px;
                    // min-width: 90px;
                    // overflow: hidden;
                    // white-space: nowrap;
                    white-space: unset;
                    // text-overflow: ellipsis;
                }}

                .facets-overview-chart-0 .label-cell.facets-overview-chart {{
                    // width: 90px;
                    // max-width: 90px;
                    // min-width: 90px;
                    width: 200px;
                    max-width: 200px;
                    min-width: 200px;
                    // overflow-wrap: break-word;
                }}

            </style>
        </head>   
        <body>
            <facets-overview id="elem"></facets-overview>
            <script>
                
                document.querySelector("#elem").protoInput = "{protostr}";

                document.addEventListener('click', function(e){{
                    if(e.target.tagName=="PAPER-BUTTON"){{
                        window.dispatchEvent(new Event('resize'));
                    }}
                }})

            </script>
        </body>
    </html>
"""

OVERVIEW_HTML_TEMPLATE_2 = """
    <link rel="import" href="https://raw.githubusercontent.com/PAIR-code/facets/master/facets-dist/facets-jupyter.html" >
    <facets-overview id="elem"></facets-overview>
    <script>
      document.querySelector("#elem").protoInput = "{protostr}";
    </script>
"""

# href="https://raw.githubusercontent.com/PAIR-code/facets/master/facets-dist/facets-jupyter.html
def overview_html(data, groupby=None):
    """Return the HTML code for an overview page."""
    data_groups = separate_data_in_groups(data, groupby)
    html = generate_overview_html(data_groups)
    return html


def separate_data_in_groups(data, groupby=None):
    """Returns a list of data groups formatted for protobuf."""
    if groupby:
        data_groups = []
        for group_name, group in data.groupby(groupby):
            data_groups.append({"name": str(group_name), "table": group})
    else:
        data_groups = [{"name": "data", "table": data}]
    return data_groups


def generate_overview_html(data_groups):
    """Return the HTML code of the overview of the data groups."""
    gfsg = GenericFeatureStatisticsGenerator()
    proto = gfsg.ProtoFromDataFrames(data_groups)
    protostr = base64.b64encode(proto.SerializeToString()).decode("utf-8")
    html = OVERVIEW_HTML_TEMPLATE.format(protostr=protostr)
    return html
