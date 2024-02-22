import json
import os
import plotly.graph_objs as go
import dash
from dash import html, dcc

# Function to load and parse JSON data
def load_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading file at {file_path}: {e}")
        return None

# Define file path
file_path = os.path.join(os.path.dirname(__file__), 'C:\\Users\\luizm\\webscraper\\phase3\\estudio_data.json')

# Load the data from the updated file
data = load_json_data(file_path)

# Assign the values to the variables
seo_status = data.get('seo_status') if data is not None else None
load_time = data.get('load_time') if data is not None else None
design_status = data.get('design_status') if data is not None else None
pwa_features_status = data.get('pwa_features_status') if data is not None else None

# Update the variable basic_seo_score with the actual value
basic_seo_score = seo_status.get('basic_seo_score') if seo_status is not None else None

# Helper functions to create sections
basic_seo_score_chart = dcc.Graph(
    id='basic-seo-score-chart',
    figure={
        'data': [
            go.Indicator(
                mode="gauge+number",
                value=basic_seo_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Basic SEO Score"}
            )
        ],
        'layout': go.Layout(title='Basic SEO Score')
    }
)

def create_seo_section(seo_data):
    if seo_data is None:
        return html.Div(id='seo-status', children=[
            html.H2('SEO Status (Data Not Available)')
        ])

    # Access the nested 'seo_status' dictionary
    seo_status_data = seo_data.get('seo_status', {})

    # Access 'basic_seo_score' from the nested dictionary
    basic_seo_score = seo_status_data.get('basic_seo_score', 0)  # Default to 0 if not found

    additional_seo_items = [
        html.Li(f"{key}: {value}") for key, value in seo_data.get('additional_seo_data', {}).items()
    ]

    advanced_seo_analysis_items = []
    for category, details in seo_data.get('advanced_seo_analysis', {}).items():
        advanced_seo_analysis_items.append(html.H4(category.replace('_', ' ').title()))
        for key, value in details.items():
            advanced_seo_analysis_items.append(html.P(f"{key.replace('_', ' ').title()}: {value}"))

    # Access 'basic_seo_detail_' items from the nested dictionary
    basic_seo_details_items = [
        html.Li(f"{key.split('_')[-1]}: {detail['weight']} ({detail['group']})") 
        for key, detail in seo_status_data.items() 
        if key.startswith('basic_seo_detail_')
    ]

    return html.Div([
        html.H2('SEO Status'),
        basic_seo_score_chart,
        html.Div([
            html.H3('Additional SEO Data'),
            html.Ul(additional_seo_items)
        ]),
        html.Div([
            html.H3('Advanced SEO Analysis'),
            *advanced_seo_analysis_items
        ]),
        html.Div([
            html.H3('Basic SEO Details'),
            html.Ul(basic_seo_details_items)
        ])
    ])

def create_load_time_section(load_time_data):
    if load_time_data is None:
        return html.Div(id='load-time', children=[
            html.H2('Load Time Analysis (Data Not Available)')
        ])

    return html.Div(id='load-time', children=[
        html.H2('Load Time Analysis'),
        dcc.Graph(id='load-time-graph', figure={
            'data': [
                go.Bar(
                    x=list(load_time_data.keys()),
                    y=list(load_time_data.values()),
                    name='Load Time'
                )
            ],
            'layout': go.Layout(
                title='Load Time Analysis',
                xaxis={'title': 'Page'},
                yaxis={'title': 'Load Time (ms)'}
            )
        })
    ])


def create_design_status_section(design_data):
    if design_data is None:
        return html.Div(id='design-status', children=[
            html.H2('Design Status (Data Not Available)')
        ])

    # CSS Framework and JavaScript Usage
    css_framework = design_data.get("CSS Framework", "N/A")
    js_usage = design_data.get("Modern JavaScript Usage", "N/A")

    # Mobile Usability
    mobile_usability = design_data.get("Mobile Usability", {})
    mobile_usability_items = [
        html.P(f"{key}: {value}") 
        for key, value in mobile_usability.items()
    ]

    # Responsive Design, HTML5 Usage, and Accessibility
    responsive_design = design_data.get("Responsive Design", "N/A")
    html5_usage = design_data.get("HTML5 Usage", "N/A")
    accessibility = design_data.get("Accessibility Features", "N/A")

    # PageSpeed Insights
    pagespeed_insights = design_data.get("PageSpeed Insights", {})
    pagespeed_insights_items = [
        html.P(f"{key}: {value}") 
        for key, value in pagespeed_insights.items()
    ]

    return html.Div([
        html.H2('Design Status'),
        html.Div([
            html.H3('CSS Framework and JavaScript Usage'),
            html.P(f"CSS Framework: {css_framework}"),
            html.P(f"JavaScript Usage: {js_usage}")
        ]),
        html.Div([
            html.H3('Mobile Usability'),
            *mobile_usability_items
        ]),
        html.Div([
            html.H3('General Design Features'),
            html.P(f"Responsive Design: {responsive_design}"),
            html.P(f"HTML5 Usage: {html5_usage}"),
            html.P(f"Accessibility Features: {accessibility}")
        ]),
        html.Div([
            html.H3('PageSpeed Insights'),
            *pagespeed_insights_items
        ])
    ])

def create_pwa_features_section(pwa_data):
    if pwa_data is None or 'score' not in pwa_data:
        return html.Div(id='pwa-features', children=[
            html.H2('PWA Features Status (Data Not Available)')
        ])

    return html.Div(id='pwa-features', children=[
        html.H2('PWA Features Status'),
        dcc.Graph(id='pwa-features-score', figure={
            'data': [go.Indicator(
                mode="gauge+number", 
                value=pwa_data['score'], 
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "PWA Score"},
                gauge={'axis': {'range': [None, 1]}}
            )],
            'layout': go.Layout(title='PWA Features Score')
        }),
        html.Div([
            html.H3('Detailed PWA Features'),
            html.Ul([
                html.Li([
                    html.Strong(detail['title']),
                    html.P(detail['description']),
                    html.P(f"Score: {detail['score']}"),
                    html.Ul([
                        html.Li(reason_item['reason']) 
                        for reason_item in detail.get('details', {}).get('items', []) 
                        if 'reason' in reason_item
                    ]) if 'details' in detail and detail['details'] is not None else None
                ]) for detail in pwa_data['details'].values()
            ]),
            html.H3('PWA Improvement Areas'),
            html.Ul([
                html.Li([
                    html.Strong(improvement['area']),
                    html.P(improvement['advice']),
                    html.Ul([
                        html.Li(detail_item.get('reason', 'N/A')) 
                        for detail_item in improvement.get('details', {}).get('items', [])
                    ]) if improvement.get('details') else None
                ]) for improvement in pwa_data.get('improvements', [])
            ])
        ])
    ])

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1('Website Analysis Dashboard'),
    html.Div(id='seo-status-section', children=create_seo_section(seo_status)),
    html.Div(id='load-time-section', children=create_load_time_section(load_time)),
    html.Div(id='design-status-section', children=create_design_status_section(design_status)),
    html.Div(id='pwa-features-section', children=create_pwa_features_section(pwa_features_status))
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)