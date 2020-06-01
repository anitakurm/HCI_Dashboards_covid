# -----------MODULE IMPORT-----------#
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State


# for graphs
# import plotly
# import plotly.graph_objs as go
import plotly.express as px
import textwrap

# for data
import os
import pandas as pd
from utils import binning
from utils import load_preprocess, filter_dataframe, get_vals_opts
from datetime import datetime as dt


# ----------DATA IMPORT-----------#
# load data <- CHANGE THAT FOR THE  FINAL WEBSITE SOLUTION
whole_df_path = "data/sample.csv"
df = load_preprocess(whole_df_path)

# Initiate the app
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

server = app.server


#-----------CONTROLS SET-UP (all dropdown menu options, etc)-----------#

#get total number of respondents
total = len(df)

#last update - latest datapoint
update_date = df['Date'].values[-1]
update_date = dt.strptime(update_date, '%Y-%m-%d').strftime("%b %d %Y")

#--- Settings menu- -----#
#country options
country_values, country_options = get_vals_opts(df['Country'])

#marital status options
mar_values, mar_options = get_vals_opts(df['Civilstand'])

#occupation options
occ_values, occ_options= get_vals_opts(df['Nuværende beskæftigelse'])

#housing options
house_values, house_options = get_vals_opts(df['Type af bolig kategorier'])

#education options
edu_values, edu_options = get_vals_opts(df['Uddannelse'])

column_values = [col for col in df][1:]
column_options = [{'label': i, 'value': i} for i in column_values]


#-----------APP LAYOUT-----------#
app.layout = html.Div(
    [
    #store data
    dcc.Store(id="filtered_data", data = df.to_dict()),

    # empty Div to trigger javascript file for graph resizing
    html.Div(id="output-clientside"),


    #TOP OF THE PAGE: Logo, Title, Learn More
    html.Div(
        [
            html.Div(
                [
                    html.Img(
                        #src=app.get_asset_url("/assets/chcaa-logoh.png"),  
                        src = "/assets/chcaa_logo.png",
                        id="chcaa-image",
                        style={
                            "height": "60px",
                            "width": "auto",
                            "margin-bottom": "25px",
                        },
                    )
                ],
                className="one-third column",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.H3(
                                "Epinion Covid-19 Survey",
                                style={"margin-bottom": "0px"},
                            ),
                            html.H5(
                                "Results Overview", style={"margin-top": "0px"}
                            ),
                        ]
                    )
                ],
                className="one-half column",
                id="title",
            ),
            html.Div(
                [
                    html.A(
                        html.Button("Learn More", id="learn-more-button"),
                        href="http://chcaa.io/#/",
                    )
                ],
                className="one-third column",
                id="button",
            ),
        ],
        id="header",
        className="row flex-display",
        style={"margin-bottom": "25px"},
    ),

    #FILTER AND GRPAH with overview boxes on top
    html.Div(
        [
            html.Div(
                [
                
                    html.H5("Filter settings", style = {'margin-left': 5}), 
                    html.P(
                            "Push 'Apply' button below to apply new settings",
                            className="control_label",
                         ),

                    html.P(
                            "Select country:",
                            className="control_label"
                        ),

                    dcc.Dropdown(
                        id = "select-country",
                        options = country_options,
                        value = country_values, #arbitrary default value
                        multi = True,
                        style = {'margin-left':5, 'margin-top':10, 'font-size': 11}
                    ),


                    html.P("Filter by gender:", className="control_label", style ={'margin-bottom':5}),

                    dcc.Checklist(
                        options=[
                            {'label': 'Male', 'value': 'Mand'},
                            {'label': 'Female', 'value': 'Kvinde'}
                            #{'label': 'Other', 'value': 'Other'}
                        ],
                        id = "select-gender",
                        value=['Mand', 'Kvinde'],
                        labelStyle={'display': 'inline-block'},
                        style = {'margin-left': 10, 'margin-bottom':10}
                    ),

                    html.P("Select age range (NA = age not specified by participant):", className="control_label", style ={'margin-bottom':5}),

                    dcc.RangeSlider(
                        id='select-age',
                        min=0,
                        max=100,
                        step=None,
                        value=[0, 100],
                        tooltip = { 'placement': 'bottom', 'always_visible': False},
                        marks={
                            0: {'label': 'NA'},
                            18: {'label': '18'},
                            25: {'label': '25'},
                            30: {'label': '30'},
                            35: {'label': '35'},
                            40: {'label': '40'},
                            45: {'label': '45'},
                            50: {'label': '50'},
                            55: {'label': '55'},
                            60: {'label': '60'},
                            65: {'label': '65'},
                            70: {'label': '70'},
                            75: {'label': '75'},
                            80: {'label': '80'},
                            85: {'label': '85'},
                            90: {'label': '90'},
                            95: {'label': '95'},
                            100: {'label': '100'}
                        }
                    ),

                    #html.P("Do you want to see respondents with unspecified age?", className="control_label", style ={'margin-bottom':5}),
                    # dcc.Checklist(
                    #     options=[{'label': 'Show respondents without specified age', 'value': 'yes'},
                    #     #{'label': 'No', 'value': 'no'}
                    #     ],
                    #     id = "show-noage",
                    #     value=['yes'],
                    #     labelStyle={'display': 'inline-block'},
                    #     style = {'margin-left': 10, 'margin-top':10}
                    # ),
                    
                    html.P(
                            "Filter by level of income:",
                            className="control_label",
                        ),
                    
                    dcc.RangeSlider(
                        id='select-income',
                        min=0,
                        max=1300000,
                        step=100000,
                        value=[0, 1300000],
                        tooltip = { 'placement': 'bottom', 'always_visible': False },
                        marks={0: {'label': "0"}, 1300000: {'label': "1.200.000+"}},
                        dots=True
                    ),

                    html.P("Filter by number of kids:", className="control_label"),
                    dcc.RangeSlider(
                        id='select-kids',
                        min=0,
                        max=6,
                        step=1,
                        value=[0, 6],
                        tooltip = { 'placement': 'bottom', 'always_visible': False },
                        marks={0 : {'label': "0"},6: {'label': "6+"}},
                        dots=True
                    ),


                    html.P("Filter by marital status:", className="control_label"),
                    dcc.Dropdown(
                        options= mar_options,
                        id = "select-marstatus",
                        value= mar_values,
                        multi=True,
                        style = {'margin-left':5, 'margin-top':10, 'font-size': 11}
                    ),

                    html.P("Filter by occupation:", className="control_label"),
                    dcc.Dropdown(
                        options= occ_options,
                        id = "select-occupation",
                        value= occ_values,
                        multi=True,
                        style = {'margin-left':5, 'margin-top':10, 'font-size': 11}
                    ),                    
                    html.P("Filter by housing type:", className="control_label"),
                    dcc.Dropdown(
                        options= house_options,
                        id = "select-housing",
                        value= house_values,
                        multi=True,
                        style = {'margin-left':5, 'margin-top':10, 'font-size': 11}
                    ),  

                    html.P("Filter by level of education:", className="control_label"),
                    dcc.Dropdown(
                        options= edu_options,
                        id = "select-education",
                        value= edu_values,
                        multi=True,
                        style = {'margin-left':5, 'margin-top':10, 'font-size': 11}
                    ),                     

                    html.Button(id = "filter-submit", n_clicks=0, children ="Apply"),
                ],
                className="pretty_container four columns",
                id="cross-filter-options",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [html.H6(id="respondent-text"), html.P("No. of respondents displayed")],
                                id="respondent_no",
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H6(id="out-text"), html.P("No. of respondents filtered out")],
                                id="missing_respondents",
                                className="mini_container",
                            ),

                            html.Div(
                                [html.H6(children = update_date), html.P("Last observation date")],
                                id="update-container",
                                className="mini_container",
                            ),
                            
                        ],
                        id="info-container",
                        className="row container-display",
                    ),
                    

                    html.Div(
                        [html.H5("Analyze filtered data"),
                        html.P("Show responses to the following question (search faster by typing):"),
                        dcc.Dropdown(id ="question-menu", optionHeight = 45, options = column_options, value = column_values[2], style = {'margin-bottom': 15,'font-size': 14}),
                        dcc.Graph(id = "counts-plot"),
                        html.P("See how ratio of answers differs by the following variable:"),
                        dcc.Dropdown(id ="main-menu-x", optionHeight = 40, options = column_options, value = 'Date', style = {'margin-bottom': 15,'font-size': 14}), 
                        dcc.Graph(id="main-plot")],
                        id="main-plot-container",
                        className="pretty_container",
                    ),

                ],
                id="right-column",
                className="eight columns",
            ),
        ],
        className="row flex-display",
    )
])


@app.callback(
    [Output("filtered_data", "data"),
    Output("respondent-text", "children" ),
    Output("out-text", "children")
    ],

    [Input("filter-submit", "n_clicks")],

    [State("select-country", "value"),
    State("select-gender", "value"),
    State('select-age', 'value'),
    State('select-income', 'value'),
    State('select-kids', 'value'),
    State('select-marstatus', 'value'),
    State('select-occupation', 'value'),
    State('select-housing', 'value'),
    State('select-education', 'value')]
)


def filter_data(n_clicks, country_values, gender_value, age_value, income_value, kids_value, mar_value, occ_value, housing_value, education_value): 

    filtered = filter_dataframe(df, country_values, gender_value, age_value, income_value, kids_value, mar_value, occ_value, housing_value, education_value)

    match = len(filtered)
    no_match = total-match

    return filtered.to_dict(), match, no_match #questionoptions, questionoptions[1]['value']



@app.callback(
    [Output('counts-plot', "figure"),
    Output("main-plot", "figure")],
    [Input("filtered_data", "data"),
    Input("question-menu", "value"),
    Input("main-menu-x", "value")]
    )

def update_mainplot(data_input, question_input, x_input):
    pd_df = pd.DataFrame.from_dict(data_input)


    demo_fig = px.histogram(pd_df, x=question_input, color_discrete_sequence= px.colors.qualitative.T10)
    
    split_text = textwrap.wrap(question_input, width=87)
    title_string = '<br>'.join(split_text)
    demo_fig.update_layout(
        title = dict(font = dict(size = 14), text = title_string, y = 0.955),
        margin=dict(l=30, r=30, b=20, t=85),
        hovermode="closest",
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9",
        legend=dict(font=dict(size=10), x = -0.04, y = 1.15, title = "", orientation = "h"),
        bargap=0.2
        )
    
    demo_fig.update_xaxes(title_text='')

    percentages = binning(pd_df, question_input, group_by=x_input)
    percentages = percentages.sort_values([x_input, question_input])
    fig = px.line(percentages, x=x_input, y="percent", color = question_input, color_discrete_sequence=px.colors.qualitative.T10)

    split_text = textwrap.wrap(question_input, width=87)
    title_string = '<br>'.join(split_text)

    
    fig.update_xaxes(showgrid=False, rangeslider=dict(visible = False))
    fig.update_yaxes(range=[0, 100])

    fig.update_traces(mode='lines+markers', marker=dict(symbol="diamond-open"))

    updatemenus=list([
        dict(
            buttons=list([
                dict(
                    args=['type', 'line'],
                    label='Trend plot',
                    method='restyle'
                ),
                dict(
                    args=['type', 'bar'],
                    label='Bar plot',
                    method='restyle'
                )
            ]),
            direction = 'down',
            pad = {'r': 10, 't': 10},
            showactive = True,
            x = 1.1,
            xanchor = 'right',
            y = 1.1,
            yanchor = 'top'
            ),
    ])

    fig.update_layout(
        #autosize=True,
        margin=dict(l=30, r=30, b=20, t=85),
        hovermode="closest",
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9",
        updatemenus = updatemenus,
        colorway = px.colors.qualitative.T10,
        title = dict(font = dict(size = 14),text = f"{title_string} by {x_input}", y = 0.955),
        legend=dict(font=dict(size=10), x = -0.04, y = 1.15, title = "", orientation = "h")
        )


    return demo_fig, fig


# Main
if __name__ == "__main__":
    app.run_server(debug=True)