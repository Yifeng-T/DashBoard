import pandas as pd
import dash
import plotly.express as px  
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import numpy as np



#prepare the dataframe:
df1 = pd.read_excel('PHDofEng&Sci.xlsx',header=[0,1,2])
df1=df1.set_index(df1.columns[0])
df1=df1.stack(level=0).stack(level=0).stack(level=0).reset_index()
df1.columns=list(df1.columns[1:].insert(0,'Institute'))
df1 = df1.rename(columns={0: 'StudentNumber', 
                          "level_1": "Sience/Engineering",
                          "level_2": "Faculty",
                          "level_3": "Major"})

df1['Major'] = df1['Major'].replace(['Agricultural sciences and natural resources'],'Agricultural sciences')
df1['Major'] = df1['Major'].replace(['Geosciences, atmospheric sciences, and ocean sciences'],'Geo/Atomo/Ocea scien')
df1['Major'] = df1['Major'].replace(['Biological and biomedical sciences'],'Bio')
df1['Major'] = df1['Major'].replace(['Political science and government'],'Political science')
df1['Major'] = df1['Major'].replace(['Aerospace, aeronautical, and astronautical'],'Aerospace and related')
df1['Major'] = df1['Major'].replace(['Computer and information sciences'],'CS')
df1['Major'] = df1['Major'].replace(['Mathematics and statistics '],'Math & Stat')
df1['Major'] = df1['Major'].replace(['Bioengineering and biomedical'],'BioEng')
df1['Major'] = df1['Major'].replace(['Electrical, electronics, and communications'],'ECE')
                    

state_names = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", 
               "California", "Colorado", "Connecticut", "District ", "of Columbia", 
               "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", 
               "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", 
               "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", 
               "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", 
               "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", 
               "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", 
               "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", 
               "Wisconsin", "West Virginia", "Wyoming"]

code = {'Alabama': 'AL',
        'Alaska': 'AK',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'}




Ins_School = []
Ins_SE = []
Ins_fac = []
Ins_major = []
Ins_value = []

State_name = []
State_SE = []
State_fac = []
State_major = []
State_value = []

#c = pd.DataFrame({"a":a,"b":b})

for index,row in df1.iterrows():
    if row["Institute"] in state_names:
        State_name.append(row["Institute"])
        State_SE.append(row["Sience/Engineering"])
        State_fac.append(row["Faculty"])
        State_major.append(row["Major"])
        State_value.append(row["StudentNumber"])
    elif row["Institute"] == "All institutions":
        continue
    else:
        Ins_School.append(row["Institute"])
        Ins_SE.append(row["Sience/Engineering"])
        Ins_fac.append(row["Faculty"])
        Ins_major.append(row["Major"])
        Ins_value.append(row["StudentNumber"])

df_institu = pd.DataFrame({"Institute":Ins_School, "Science/Engineering":Ins_SE, 
                           "Faculty":Ins_fac, "Major":Ins_major, "StudentNumber": Ins_value})

df_state = pd.DataFrame({"State":State_name, "Science/Engineering":State_SE, 
                           "Faculty":State_fac, "Major":State_major, "StudentNumber": State_value})

#state summ
dff1 = df_state
dff1 = dff1.groupby("State").sum()
dff1.reset_index(inplace=True)
dff1['Code'] = dff1['State'].map(code)

#major sum
dff2 = df_institu
dff2 = dff2.groupby("Major").sum()
dff2.reset_index(inplace=True)
dff2 = dff2.loc[dff2["Major"] != "Total"]

#major-ins
df_major_ins = df_institu.groupby(["Major", "Institute"]).sum()
df_major_ins.reset_index(inplace=True)

#S/E
df_se = df_institu.groupby(["Science/Engineering", "Major"]).sum()
df_se.reset_index(inplace=True)

#s:
df_ses = df_se[df_se["Science/Engineering"] == "Science"]
df_ses = df_ses.loc[df_ses["Major"] != "Total"]
df_see = df_se[df_se["Science/Engineering"] == "Engineering"]
df_see = df_see.loc[df_see["Major"] != "Total"]
#=====================
external_stylesheets = [dbc.themes.LUX]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Doctorate-granting👨‍🎓 institutions, by state or location and major science and engineering fields of study: 2017"), className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(html.H6(children='Data visulization made by Yifeng Tang'), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H6(children='Could access resources at https://github.com/Yifeng-T/DashBoard'), className="mb-4")
        ]),
        html.Hr(),
#===============
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Overvie of Granting Doctors by States',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mb-4")
        ]),
        dbc.Row([
        dbc.Col(html.H5(children='Heat Map of granting phds by states', className="text-center"),
                className="mt-4")]),

        dcc.Graph(id='geograph',
                  figure=px.choropleth(data_frame=dff1, locationmode='USA-states',
                                                        locations='Code',
                                                        scope="usa",
                                                        color='StudentNumber',
                                                        hover_data=['StudentNumber'],
                                                        color_continuous_scale=px.colors.sequential.YlOrRd,
                                                        labels={'Pct of Colonies Impacted'})),
        html.Hr(),
    
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Overview of Grading Doctors By Institutes and Majors',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mt-4 mb-5")
        ]),
        
        dbc.Row([
        dbc.Col(html.H5(children='Major Diversity of 👨‍🎓PhDs Granting', className="text-center"),
                className="mt-4")
    ]),
        dcc.Graph(id='bargraph',figure=px.bar(dff2, x='Major',y="StudentNumber")),
        html.Hr(),

        dbc.Row([
        dbc.Col(html.H5(children='Institutions Diversity of 👨‍🎓PhDs Granting', className="text-center"),
                className="mt-4")]),
        
        html.Div(children=[html.Div(children="Institute", className="menu-title"),
                           dcc.Dropdown(id="ins-filter", 
                                        options=[{"label": region, "value": region} for region in np.sort(df_institu["Institute"].unique())],
                                        value="Harvard U.",
                                        clearable=False,
                                        className="dropdown",),]),
        dcc.Graph(id='inst_graph',config={"displayModeBar": False}),

        html.Hr(),
        dbc.Row([
        dbc.Col(html.H5(children='Majors and Institutions compared of PHD GRANTING', className="text-center"),
                className="mt-4")]),
        html.Div(children=[html.Div(children="Select Majors", className="menu-title"),
                                    dcc.Dropdown(id='major_select', value=['Chemistry','Psychology'], multi=True, 
                                    options=[{'label': x, 'value': x} for x in df_major_ins["Major"].unique()])]),
        
        html.Div(children=[html.Div(children="Select Institutes", className="menu-title"),
                                    dcc.Dropdown(id='ins_select', value=['Boston U.','Emory U.','Harvard U.'], multi=True, 
                                    options=[{'label': x, 'value': x} for x in df_institu["Institute"].unique()])]),
    
        dbc.Row([dbc.Col(dcc.Graph(id='pie-graph', figure={}, className='six columns'), width=4),
                 dbc.Col(dcc.Graph(id='my-graph',
                            figure={}, clickData=None, hoverData=None,
                            config={'staticPlot': False,     
                                    'scrollZoom': True,      
                                    'doubleClick': 'reset',  
                                    'showTips': False,       
                                    'displayModeBar': True,  
                                    'watermark': True,}, 
                            className='six columns'), width=8)]),
        html.Hr(),
        
        dbc.Row([dbc.Col(dbc.Card(html.H3(children='Overview of Grading Doctors By Faculty',
                                          className="text-center text-light bg-dark"), body=True, color="dark"), 
                                className="mt-4 mb-5")]),
        
        dbc.Row([
        dbc.Col(html.H5(children='Major diversity for science', className="text-center"),
                width=6, className="mt-4"),
        dbc.Col(html.H5(children='Major diversity for engineering', className="text-center"), width=6,
                className="mt-4"),
        ]),

        dbc.Row([dbc.Col(dcc.Graph(figure = px.bar(data_frame=df_ses, x='Major', y="StudentNumber").update_xaxes(tickangle=45)), width=6),
                 dbc.Col(dcc.Graph(figure = px.bar(data_frame=df_see, x='Major', y="StudentNumber").update_xaxes(tickangle=45)), width=6)]),

        html.Hr(),

    ])
])
    

@app.callback(Output('inst_graph', 'figure'),
              [Input('ins-filter', "value")])

def update_graph(ins_name):
    df_selec = df_institu[df_institu["Institute"] == ins_name]
    df_selec = df_selec.groupby("Major").sum()
    df_selec.reset_index(inplace=True)

    df_selec = df_selec.loc[df_selec["Major"] != "Total"]

    a = px.bar(df_selec, x='Major', y=['StudentNumber'], title=f'Majors diversity in: {ins_name}')
    return a

@app.callback([Output(component_id='pie-graph', component_property='figure'),
               Output(component_id='my-graph', component_property='figure')],
              [Input(component_id='major_select', component_property='value'),
               Input(component_id='ins_select', component_property='value')])

def draw(major_chosen, ins_select):
    df_two_1 = df_major_ins[df_major_ins["Major"].isin(major_chosen)]
    df_two_1 = df_two_1[df_two_1["Institute"].isin(ins_select)]

    fig = px.bar(df_two_1, x='Institute', y='StudentNumber', color='Major', title="Stack Histogram analysis")
    fig2 = px.pie(data_frame=df_two_1, values='StudentNumber', names='Major', title='Pie chart ANALYSIS')
    return fig2, fig




if __name__=='__main__':
    app.run_server(debug=True)


