# 1. Import Dash
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px

# 2. Create a Dash app instance
#app = ____.____(
app = dash.Dash(    
    name='Isupplier',
    external_stylesheets=[dbc.themes.LUX]
)
app.title = 'Vendor Analytics Isupplier'


## --- NAVBAR
from dash import Input, Output, State, html
from dash_bootstrap_components._components.Container import Container

#PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
PLOTLY_LOGO = "http://depopipa.co.id/wp-content/uploads/2016/01/Sinar-mas.png"

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button(
                "Search", color="primary", className="ms-2", n_clicks=0
            ),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="50px")),
                        dbc.Col(
                            dbc.NavbarBrand ( "ISUPPLIER" ,className="g-2 fs-2", ),
                            ),
                    ],
                    align="center",
                    className="g-2 fs-2"
                    
                ),

            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="#cc0000",
    dark=True,
)


Footbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [                        
                    dbc.Col([],width=11,),
                    dbc.Col([dbc.NavbarBrand ( "Copyright© 2022 Sinarmas Mining. All Rights reserved" 
                    ,className="fs-6 align-center align-middle", )],width=1,),
                
                ],
            ),
        ]
    ),
    color="#cc0000",
    dark=True,
)



## --- LOAD DATASET
iss=pd.read_csv('Vendor_Training_Dashboard.csv',sep=';')

#option SAP

 
### CARD CONTENT

iss_active = iss[iss['status'] == 1]
total_active = [
    dbc.CardHeader([html.P('Total Active Vendor')]),
    dbc.CardBody([
        html.P(iss_active['status'].value_counts()) 
    ])
]

iss_aff = iss[iss['afiliasi'] == 1]
total_afiliasi = [
    dbc.CardHeader([html.P('Total Vendor Affiliate')]),
    dbc.CardBody([
        html.P(iss_aff['afiliasi'].value_counts()) # ,style{color:red}
    ]),
]

cond_ariba = iss['ariba_code'].notna().sum()
total_ariba = [
    dbc.CardHeader([html.P('Total Vendor Ariba')]),
    dbc.CardBody([
        html.P(cond_ariba) ,
    ]),
]

#agg
cond_sap = iss.notna().sum()
SAP_BCE = cond_sap[10]
SAP_GEMS = cond_sap[11]
SAP_BKES = cond_sap[12]

sap_card = [
    dbc.CardHeader([html.P('Total Vendor SAP')]),
    dbc.CardBody([
        html.P('BCE - ' + str(SAP_BCE) + ' | ' + 'GEMS - ' + str(SAP_GEMS) + ' | ' + 'BKES - ' + str(SAP_BKES)),
    ]),
]


asc = dbc.CardHeader([
        dcc.RadioItems(
        id='select_ascending',
        options= [ {'label':'Descending ' , 'value':1},   
                   {'label':'Ascending '  , 'value':0} 
                ],
        labelStyle={'display': 'inline-block'},
        value=1,
        inline = True,
        inputStyle={"margin-left": "20px"},

        )
        
 ],), 



#tree Map
agg_vendor_PraQ = pd.crosstab(
    index=iss['prakualifikasi'],
    columns='jumlah vendor'
).reset_index().sort_values(by = 'jumlah vendor', ascending = True)

agg_vendor_PraQ["all"] = "Prakualifikasi Vendor" # in order to have a single root node
fig = px.treemap(
    agg_vendor_PraQ, 
    path=['all', 'prakualifikasi'], 
    values='jumlah vendor',
    color_discrete_sequence =['#ff6600','salmon','#ff3333' ,'#ff9966']*len(agg_vendor_PraQ),
    )

fig.update_traces(
    root_color="lightgrey",
    hovertemplate='<b> %{label} </b> <br> Total Vendor: %{value}'
    )
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25)),





## --- DASHBOARD LAYOUT

#app.____ = html.Div([
app.layout = html.Div([

    # Navbar
    html.Div([
        navbar,
    ]),

    html.Div([
        dbc.Row([
            dbc.Col([     
                dbc.Card(total_active,color='#ff3333',inverse=True)],
                width=3,
                style={
                    'backgroundColor':'#ffbaba',
                }),
            dbc.Col([     
                dbc.Card(total_afiliasi,color='#ff3333',inverse=True)],
                width=3,
                style={
                    'backgroundColor':'#ffbaba',
                }),
            dbc.Col([     
                dbc.Card(total_ariba,color='#ff3333',inverse=True)],
                width=3,
                style={
                    'backgroundColor':'#ffbaba',
                }),                
            dbc.Col([     
                dbc.Card(sap_card,color='#ff3333',inverse=True)],
                width=3,
                style={
                    'backgroundColor':'#ffbaba',
                }),  

        dbc.Row([ html.Br(), html.Br(), ]),
        dbc.Row([             
            dbc.Col([
                dcc.Dropdown(
                    id='select',
                    #options=['provinsi','kota'] ,
                    options= [{'label':'Province', 'value':'provinsi'},{'label':'City', 'value':'kota'}],
                    value='provinsi'
                ),                
                     
                dcc.Graph(
                id='plot_pie',
                #figure=pie_vendor,
                )
            ],
            width=4,
            style={
            }), 
            dbc.Col([
                dbc.Card(asc,color='White',inverse=False),
                   
                 dbc.Row([
                #     dcc.Dropdown(
                #     id='select_ascending',
                #     options=[1,0],
                #     value=1
                #     ),

                    dcc.Graph(
                    id='bar_chart',
                    #figure=chart_badan,
                    )
                ],className="h-60"),
                dbc.Row([html.Br() ],className="h-10"),

                # dbc.Row([      
                #     dcc.Graph(
                #     id='tree_map',
                #     figure=fig,)
                # ]),
            ],
            width=8,
            ), 
        ],className="h-100"),

        dbc.Row([ html.Br(),]),   
        dbc.Row([      
                    dcc.Graph(
                    id='tree_map',
                    figure=fig,)
        ]),
    ]),
    html.Br(), html.Br(),
    ],
    style={
        'backgroundColor':'#ffbaba',
        'paddingRight':'30px',
        'paddingLeft':'40px',
        'paddingBottom':'30px',
        'paddingTop':'30px',
    }),

        html.Div([
        Footbar,
        ]),


])

## PLOTPIE Callback

@app.callback(
    Output(component_id='plot_pie', component_property='figure'),
    Input(component_id='select', component_property='value')
)

def update_plotbar(select):
    # Data aggregation
    agg_vendor_region = pd.crosstab(
    index=iss[select],
    columns='jumlah vendor'
    ).reset_index().sort_values('jumlah vendor').tail(5)
    
    # visualize
    pie_vendor = px.pie(
    agg_vendor_region,
    values='jumlah vendor',
    names=select,
    color_discrete_sequence=['#cc0000', 'salmon', '#ff3333', '#ff6600', '#ff9966'],
    template='plotly_white',
    title='Total Vendor Per Region',
    hole=0.4,
).update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="right",
    x=0.01)
)
    return pie_vendor

    
@app.callback(
    Output(component_id='bar_chart', component_property='figure'),
    Input(component_id='select_ascending', component_property='value')
)

def update_plotbar(select_ascending):
    # Data aggregation
    agg_vendor_badan_usaha = pd.crosstab(
    index=iss['Badan_usaha'],
    columns='jumlah vendor'
    ).reset_index().sort_values(by = 'jumlah vendor', ascending = select_ascending).tail(5)

    
    # visualize
    chart_badan=px.bar(
    agg_vendor_badan_usaha,
    x = 'jumlah vendor',
    y = 'Badan_usaha',
    template = 'plotly_white',
    title = 'Vendor Business Entity',
    color_discrete_sequence =['#ff3333']*len(agg_vendor_badan_usaha),
    labels = {
        'jumlah vendor': 'Total Vendor',
        'Badan_usaha' : 'Badan Usaha'
    }
)
    return chart_badan


# 3. Start the Dash server
if __name__ == "__main__":
    app.run_server()
