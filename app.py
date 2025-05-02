import dash
from dash import html, dcc, Input, Output, State
from dash.dependencies import ALL, MATCH
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from DGP import DGP_sample


#Custom trend function dictionary, with min, max and default value for each parameter for each trend function
trend_functions = {
    "Linear": {
        "function": lambda x, t, scale=2, offset=0: scale * x * t + offset,
        "params": {
            "scale": {"value": 2, "min": 0.1, "max": 10, "step": 0.1, "help": "Slope of the linear trend"},
            "offset": {"value": 0, "min": -1000, "max": 1000, "step": 1, "help": "Vertical shift of the line"}
        }
    },
    "Piecewise": {
        "function": lambda x, t, scale=2, breakpoint=25, post_scale=0.5:
            scale * x * t if t <= breakpoint else scale * breakpoint * x + post_scale * x * (t - breakpoint),
        "params": {
            "scale": {"value": 2, "min": 0.1, "max": 10, "step": 0.1, "help": "Initial slope before breakpoint"},
            "breakpoint": {"value": 25, "min": 1, "max": 1000, "step": 1, "help": "Time step at which slope changes"},
            "post_scale": {"value": 0.5, "min": 0.1, "max": 10, "step": 0.1, "help": "Slope after breakpoint"}
        }
    },
    "Exponential": {
        "function": lambda x, t, scale=1, rate=0.03: scale * x * np.exp(rate * t),
        "params": {
            "scale": {"value": 1, "min": 0.1, "max": 10, "step": 0.1, "help": "Scale of the exponential curve"},
            "rate": {"value": 0.03, "min": 0.001, "max": 1, "step": 0.001, "help": "Growth rate"}
        }
    },
    "Logarithmic": {
        "function": lambda x, t, scale=1: scale * x * np.log(t + 1),
        "params": {
            "scale": {"value": 1, "min": 0.1, "max": 10, "step": 0.1, "help": "Amplitude of the log curve"}
        }
    },
    "Wavy": {
        "function": lambda x, t, scale=1, amplitude=1000, frequency=0.2:
            scale * x * t + amplitude * np.sin(frequency * t),
        "params": {
            "scale": {"value": 1, "min": 0.1, "max": 10, "step": 0.1, "help": "Linear growth component"},
            "amplitude": {"value": 1000, "min": 0, "max": 5000, "step": 100, "help": "Height of the wave"},
            "frequency": {"value": 0.2, "min": 0.01, "max": 2, "step": 0.01, "help": "How frequent the wave oscillates"}
        }
    },
    "Polynomial": {
        "function": lambda x, t, a=0.1, b=2, c=100:
            a * x * t**2 - b * t + c,
        "params": {
            "a": {"value": 0.1, "min": 0.01, "max": 1, "step": 0.01, "help": "Quadratic coefficient"},
            "b": {"value": 2, "min": 0, "max": 10, "step": 0.1, "help": "Linear subtraction term"},
            "c": {"value": 100, "min": -500, "max": 500, "step": 10, "help": "Vertical shift"}
        }
    },
    "Recovery": {
        "function": lambda x, t, a=0.4, b=-5, c=50:
            a * x * t**2 + b * t + c,
        "params": {
            "a": {"value": 0.4, "min": 0.01, "max": 2, "step": 0.01, "help": "Recovery curve sharpness"},
            "b": {"value": -5, "min": -20, "max": 0, "step": 1, "help": "Initial downward slope"},
            "c": {"value": 50, "min": -100, "max": 200, "step": 5, "help": "Vertical base shift"}
        }
    }
}

#Caching some values for controlling updates and for download
cache = {
    "n_clicks": 0,
    "df": 0,
    "error": 0, 
    "trend_params": 0
}

# Safe wrapper for DGP generation
def safe_generate_dgp(**kwargs):
    try:
        return DGP_sample(**kwargs), ""
    except Exception as e:
        return pd.DataFrame(), str(e)

# App layout
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css"
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, title="Time Series Generator")

#App layout
app.layout = html.Div( children = [dbc.Container([
    html.Div([ #Documentation section
        html.H1("Time Series Generator (DGP Simulation)", className = "mb-4 mx-3 text-center"),
        dbc.Accordion([
            dbc.AccordionItem([
                html.H5("📚 Overview — What is a Data Generating Process (DGP)?", className="mb-2"),
                html.P("A Data Generating Process (DGP) is a way of describing how data comes to life — it's the combination of all the underlying patterns, rules, and randomness that produce the numbers we observe over time."),
                html.P("In time series, the DGP usually includes elements like:"),
                html.Ul([
                    html.Li("📉 A trend - representing long-term growth or decline"),
                    html.Li("🌤️ Seasonality - repeating patterns like monthly or yearly cycles"),
                    html.Li("🎲 Noise - unpredictable fluctuations or randomness")
                ], className = "list-unstyled px-3"),
                html.P("Think of the DGP as the invisible machine behind your data — it shapes how your series behaves, even if you can't see it directly."),
                html.P("With this interactive tool, you will be able to generate and explore generated time series data using a flexible and customizable Data Generating Process (DGP). It's designed for both learning and experimentation."),
                html.Hr(),
                html.H5("⚙️ Key Features", className="mt-4 mb-2"),
                html.Ul([
                    html.Li("📈 Basic trend, seasonality, and noise simulation with adjustable values"),
                    html.Li("🔁 Choose between absolute or relative seasonality and noise behaviors"),
                    html.Li("📊 Visualize each component (trend, seasonality, noise) individually with toggle checkboxes"),
                    html.Li("📐 Select from a variety of built-in trend types (linear, exponential, wavy, etc.)"),
                    html.Li("🧠 Built-in caching — only regenerates when relevant inputs change"),
                    html.Li("💾 Download generated time series as CSV"),
                    html.Li("🎚️ Support for custom trend parameters per function (e.g., slope, frequency, amplitude)"),
                    html.Li("🧪 Experiment with endless time series forms using parameter tuning")
                ], className = "list-unstyled px-3"),
                html.Hr(),
                html.H5("🔧 How It Works", className="mt-4 mb-2"),
                html.P("The system constructs the final time series value as a combination of three parts:"),
                html.Ol([
                    html.Li("A trend component, generated from a mathematical function you choose"),
                    html.Li("A seasonal component, active only at the positions you specify in the cycle"),
                    html.Li("A random noise component, drawn from a uniform distribution")
                ]),
                html.P("You can simulate realistic patterns, visualize how components interact, and download the data as a CSV file to test forecasting models or statistical tools."),

                html.Hr(),
                html.H5("🎯 Suggested Values for Trend, Seasonality, and Noise"),
                html.P("Use these ranges as starting points to generate clear and realistic patterns for each trend type:"),

                dbc.Table([
                    html.Thead(html.Tr([
                        html.Th("Trend Type"),
                        html.Th("Trend"),
                        html.Th("Seasonality"),
                        html.Th("Noise")
                    ])),
                    html.Tbody([
                        html.Tr([html.Td("Linear / Piecewise"), html.Td("100 - 300"), html.Td("500 - 1500"), html.Td("100 - 1000")]),
                        html.Tr([html.Td("Exponential / Logarithmic"), html.Td("500 - 1000"), html.Td("200 - 600"), html.Td("200 - 400")]),
                        html.Tr([html.Td("Wavy"), html.Td("50-150"), html.Td("200 - 400"), html.Td("100 - 200")]),
                        html.Tr([html.Td("Polynomial"), html.Td("0.05 - 10"), html.Td("5 - 200"), html.Td("5 - 50")]),
                        html.Tr([html.Td("Recovery"), html.Td("0.05 - 0.9"), html.Td("5 - 30"), html.Td("5 - 20")]),
                    ])
                ], bordered=True, striped=True, hover=True, responsive=True),
                html.Hr(),
                html.H5("🚀 Get Started", className="mt-4 mb-2"),
                html.P(["Adjust the controls below, hit ",html.B('Generate Time Series'), ", and explore the dynamic plots! ✨"])
            ], title=html.B("About this Tool"), style = {"background-color": "#f6f6f6"}, className = "shadow")
        ], className="mb-4", start_collapsed=True),
    ],className="my-4"),

    dbc.Row([
        dbc.Col([ #Main Controls
            html.Div([
                html.H3(["Main Controls"], className = "text-center mb-3"), 
                
                dbc.Label("Base Trend Value (numeric growth)"),
                dbc.Input(id='trend-input', type='number', value=150, className = "mb-2"),

                dbc.Label("Seasonality Magnitude (e.g. 500 or 0.1 for relative)"),
                dbc.Input(id='seasonality-input', type='number', value=1000, className = "mb-2"),

                dbc.Label("Noise Range (+/- amount of randomness)"),
                dbc.Input(id='noise-input', type='number', value=500, className = "mb-2"),

                dbc.Label("Seasonality Cycle (e.g. 12 for monthly)"),
                dbc.Input(id='seasonality-cycle', type='number', value=12, className = "mb-2"),

                dbc.Label("Seasonality Active Points (select multiple within cycle)"),
                dcc.Dropdown(id='seasonality-points', multi=True, value = [9]),
            ],className = "rounded p-3 shadow h-100", style = {"background-color": "#f6f6f6"})
        ], width=6),

        dbc.Col([ #More Customization
            html.Div([
                html.H3(["More Customization"], className = "text-center mb-3"), 
                dbc.Label("Start Date of Series (YYYY-MM-DD)"),
                dcc.DatePickerSingle(id='start-date', date='2000-01-01', style={'display': 'block'}, className = "mb-2"),

                dbc.Label("Date Interval (D, M, Y)"),
                dcc.Dropdown(id='date-interval', options=[
                    {'label': 'Daily', 'value': 'D'},
                    {'label': 'Monthly', 'value': 'ME'},
                    {'label': 'Yearly', 'value': 'Y'}
                ], value='ME', className = "mb-2"),

                dbc.Label("Trend Function"),
                dcc.Dropdown(id='trend-func', options=[
                    {'label': name, 'value': name} for name in trend_functions.keys()
                ], value='Piecewise', className = "mb-2"),

                dbc.Label("Seasonality Mode"),
                dcc.Dropdown(id='seasonality-mode', options=[
                    {'label': 'Absolute', 'value': 'absolute'},
                    {'label': 'Relative', 'value': 'relative'}
                ], value='absolute', className = "mb-2"),

                dbc.Label("Noise Mode"),
                dcc.Dropdown(id='noise-mode', options=[
                    {'label': 'Absolute', 'value': 'absolute'},
                    {'label': 'Relative', 'value': 'relative'}
                ], value='absolute')
            ], className = "rounded p-3 shadow h-100", style = {"background-color": "#f6f6f6"})
        ], width=6)
    ], className = "align-items-stretch"),
    
    dbc.Container([ #Generate button section
        dbc.Row([
            dbc.Col([
                dbc.Label("Number of Time Points to Generate"),
                dbc.Input(id='samples-input', type='number', value=50),
            ],width = 3, className = "d-flex flex-column"),
            dbc.Col([
                dbc.Button("Generate Time Series", id='generate-btn', color='primary'),
            ],width = 3, className = "d-flex align-items-end")
        ], className = "rounded p-3 shadow h-100", style = {"background-color": "#f6f6f6"})
    ], className = "flex mt-3 mb-3"),
    
    dbc.Container([ #Graph controls and download option
        dbc.Row([
            dbc.Col([
                dbc.Checklist(
                    options=[
                        {"label": "Show Trend", "value": "show_trend"},
                        {"label": "Show Seasonality", "value": "show_seasonality"},
                        {"label": "Show Noise", "value": "show_noise"}
                    ],
                    value=["show_trend", "show_seasonality"],
                    id="component-toggles",
                    inline=True,
                    className="custom-checklist"
                )
            ], width = 9, className = "d-flex align-items-center"), 
            
            dbc.Col([
                dbc.Button("Download Data", id='download-btn', color='primary', className = "w-75"),
                dcc.Download(id="download-dataframe-csv")
            ], width = 3, className = "d-flex align-items-center") 
        ], className = "rounded p-3 shadow h-100", style = {"background-color": "#f6f6f6"})
    ], className = "flex mt-5"),
    
    
    html.Div(id='error-message', style={"color": "red", "fontWeight": "bold"}), #Error section
    
    dbc.Container([ #Graph
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='ts-graph', className = "w-100", style = {"height":"450px"})],
                width = 12, className = "d-flex justify-content-center")
        ], className = "rounded shadow h-100", style = {"background-color": "#f6f6f6"})
    ], className = "flex my-2"),
    
    dbc.Container([ #Advanced contols for trends
        dbc.Accordion([
            dbc.AccordionItem([
                html.Div(id='trend-params-container', className='my-4')
            ], title="Advanced Controls", id = "advanced_controls_title", style = {"background-color": "#f6f6f6"}, className = "shadow")
        ], start_collapsed=True),
    ], className = "flex mt-2 p-0"),
    
    html.Div(id='ts-info', style={"fontWeight": "bold"}, className = "py-3 text-center"), #info
    
    html.Hr(),
    
    html.Div([ #Footer
        html.P("Made with ❤️ by Ali Adel", style={"marginRight": "15px", "color":"#707070"}),
        html.A(html.I(className="bi bi-linkedin"), href="https://www.linkedin.com/in/ali-adel-84b390101/", target="_blank", style={"marginRight": "20px"}),
        html.A(html.I(className="bi bi-github"), href="https://github.com/adelian14", target="_blank")
    ], style={"textAlign": "center", "marginTop": "30px", "fontSize": "1.2rem"})

])], style={"minHeight": "100vh"})


#--------------------Callback functions----------------------------

# A function that updates the seasonality points values based on the seasonality cycle value
@app.callback(
    Output('seasonality-points', 'options'),
    Input('seasonality-cycle', 'value')
)
def update_seasonality_options(cycle):
    if cycle and cycle > 0:
        return [{'label': str(i), 'value': i} for i in range(1, cycle + 1)]
    return []


# A function to download the dataframe as a csv file
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("download-btn", "n_clicks"),
    prevent_initial_call=True
)
def download_df(n_clicks):
    return dcc.send_data_frame(cache['df'].to_csv, "time_series_data.csv", index=False)


# A function that updates the parameters of the advanced section according to the selected trend function
@app.callback(
    Output('trend-params-container', 'children'),
    Output('advanced_controls_title', 'title'),
    Input('trend-func', 'value')
)
def update_param_sliders(selected_trend):
    trend_info = trend_functions.get(selected_trend)
    if not trend_info:
        return "No parameters available.", html.B("Parameter Controls")

    sliders = []
    for param_name, meta in trend_info["params"].items():
        sliders.append(
            html.Div([
                dbc.Label(f"{param_name} ({meta['help']})"),
                dcc.Slider(
                    id={"type": "trend-param", "index": param_name},
                    min=meta["min"],
                    max=meta["max"],
                    step=meta["step"],
                    value=meta["value"],
                    marks={
                        round(v, 2): str(round(v, 2))
                        for v in np.linspace(meta["min"], meta["max"], num=15)
                    },
                    tooltip={"placement": "bottom", "always_visible": False}
                ),
                html.Br()
            ])
        )
    return sliders, html.B(f"Parameter Controls for {selected_trend} Trend")


# The main callback function that generates the dataframe and draws the graph
@app.callback(
    [Output('ts-graph', 'figure'), Output('ts-info', 'children'), Output('error-message', 'children'), Output('error-message', 'className')],
    Input('generate-btn', 'n_clicks'),
    Input('component-toggles', 'value'),
    Input({'type': 'trend-param', 'index': ALL}, 'value'),
    State('trend-input', 'value'),
    State('seasonality-input', 'value'),
    State('noise-input', 'value'),
    State('samples-input', 'value'),
    State('trend-func', 'value'),
    State('seasonality-points', 'value'),
    State('seasonality-cycle', 'value'),
    State('start-date', 'date'),
    State('date-interval', 'value'),
    State('seasonality-mode', 'value'),
    State('noise-mode', 'value')
)
def generate_series(n_clicks, toggles, param_values, trend, seasonality, noise, samples, trend_func_name,
                    seasonality_points, seasonality_cycle, start_date, date_interval,
                    seasonality_mode, noise_mode):
    
    fig = go.Figure() #Creating empty graph
    fig.update_layout(
        plot_bgcolor='#eee',
        paper_bgcolor="#f6f6f6"
    )
    
    #checking for missing inputs
    if None in [trend, seasonality, noise, samples, seasonality_cycle] or not trend_func_name:
        return fig, "Invalid input. Please fill in all required fields.", "Missing required input.", "py-3 text-center"
    
    #Building trend params dictionary
    param_names = list(trend_functions[trend_func_name]["params"].keys())
    trend_params = {name: value for name, value in zip(param_names, param_values)}
    
    
    #Generating dataframe or using the cached dataframe based on the input values 
    if n_clicks != cache['n_clicks'] or cache.get('trend_params') != trend_params:
        df, error = safe_generate_dgp(
            trend=trend,
            seasonality=seasonality,
            noise=noise,
            num_samples=samples,
            trend_function= lambda x, t: trend_functions[trend_func_name]["function"](x, t, **trend_params),
            seasonality_points=seasonality_points or [],
            seasonality_cycle=seasonality_cycle,
            start_date=start_date,
            date_interval=date_interval,
            seasonality_mode=seasonality_mode,
            noise_mode=noise_mode
        )
        #Caching values
        cache['n_clicks'] = n_clicks
        cache['df'] = df
        cache['error'] = error
        cache['trend_params'] = trend_params
    else:
        df = cache['df']
        error = cache['error']
    
    #Showing Error
    if error:
        return fig, "", f"Error generating series: {error}", "py-3 text-center"


    #Plotting data
    fig.add_trace(go.Scatter(x=df['date'], y=df['value'], name='Total Value'))
    if 'show_trend' in toggles:
        fig.add_trace(go.Scatter(x=df['date'], y=df['trend'], name='Trend', line=dict(dash='dot')))
    if 'show_seasonality' in toggles:
        fig.add_trace(go.Scatter(x=df['date'], y=df['seasonality'], name='Seasonality', line=dict(dash='dash')))
    if 'show_noise' in toggles:
        fig.add_trace(go.Scatter(x=df['date'], y=df['noise'], name='Noise', line=dict(dash='dashdot')))
    fig.update_layout(title="Synthetic Time Series", xaxis_title="Date", yaxis_title="Value")

    description = f"Series generated using '{trend_func_name}' trend, seasonality mode: {seasonality_mode}, noise mode: {noise_mode}."

    return fig, description, "", ""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
