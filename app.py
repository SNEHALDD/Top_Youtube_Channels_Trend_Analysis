import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Input, Output, dcc, html
from create_charts import fig, fig2, fig4, fig5, fig6, fig8, fig9, template
from data_loader import (mega_df2, mega_df3, category_data_new, channel_data,
                         video_sentiment_data)

app = dash.Dash(external_stylesheets=[
                dbc.themes.DARKLY], suppress_callback_exceptions=True)

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": "#303030",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "marginLeft": "22rem",
    "marginRight": "2rem",
    "padding": "2rem 1rem",
}

# create a list of categories that aren't null
categories = category_data_new['topic_category'].unique().tolist()

# create a list of dictionaries for the dropdown
category_options = [{'label': i, 'value': i} for i in categories]


def transform_value(value):
    return 10 ** value


ml_viz_options_num = [
    {'label': ' Channel Views',
     'value': 'channel_view_count'},
    {'label': ' Subscribers',
     'value': 'subscriber_count'},
    {'label': ' Channel Video Count',
     'value': 'channel_video_count'},
    {'label': ' Video Likes',
     'value': 'like_count'},
    {'label': ' Number of Comments',
     'value': 'comment_count'},
    {'label': ' Video Views',
        'value': 'view_count'},
    {'label': ' Length of Video',
     'value': 'video_length_seconds'},
    {'label': ' Sentiment Score',
        'value': 'sentiment'},
]


ml_viz_options_color = [
    {'label': ' Topic Category',
        'value': 'topic_category'},
    {'label': ' Video Views Binned',
        'value': 'video_views_binned'},
    {'label': ' View count',
        'value': 'view_count'},
    {'label': ' Weekday Published',
        'value': 'day_of_week_published'},
    {'label': ' Sentiment Score',
        'value': 'sentiment'},
    {'label': ' None',
        'value': 'none'},
]

ml_viz_options_symbol = [
    {'label': ' Topic Category',
        'value': 'topic_category'},
    {'label': ' Video Views Binned',
        'value': 'video_views_binned'},
    {'label': ' Weekday Published',
        'value': 'day_of_week_published'},
    {'label': ' None',
        'value': 'none'},
]


# create the sidebar
sidebar = html.Div([
    # add image
    html.Img(src='https://upload.wikimedia.org/wikipedia/commons/0/09/YouTube_full-color_icon_%282017%29.svg', style={
        'width': '100%', 'height': 'auto'}),
    html.H3("YouTube Analysis", className='header',
            style={'color': 'red', 'textAlign': 'center', 'width': '100%'}),
    html.P('"Group 4" Final Project Dashboard for UT-Austin Data Analytics Bootcamp',
           style={'textAlign': 'center'}),
    html.Hr(),
    dbc.Nav(
        [
            dbc.NavLink("Home", href="/", active="exact"),
            dbc.NavLink("Channel Category Metrics",
                        href="/page-1", active="exact"),
            dbc.NavLink("Top Channels", href="/page-5",
                        active="exact"),
            dbc.NavLink("Video Length Metrics",
                        href="/page-8", active="exact"),
            dbc.NavLink("Comment Sentiment Analysis",
                        href="/page-2", active="exact"),
            dbc.NavLink("Video Publishing Metrics",
                        href="/page-3", active="exact"),
            dbc.NavLink("Machine Learning Analysis",
                        href="/page-4", active="exact"),
            dbc.NavLink("Machine Learning Visualization", href="/page-7",
                        active="exact"),
            dbc.NavLink("Additional Analysis (Tableau)",
                        href="/page-6", active="exact"),
        ],
        vertical=True,
        pills=True,
    ),
],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")],
)
def render_page_content(pathname):
    # ------------------------------------------------------------
    if pathname == "/":
        return html.Div([html.H1('YouTube Video Analysis Home Page'), html.Hr(),
                         dcc.Markdown('''
# Overview

Our goal is to create a machine learning model that will be trained to predict whether or not a youtube video has the potential to be viral. This will be based on features which include amount of subscribers that channel has, total amount of views on the channel and video, which category the video belongs to, and total amount of likes on the video. From these features, we will have over 7,000 videos to train and test this algorithm on so the model can learn which features best predict if the video will be viral. We are basing the term viral as a video that gets over 1 million views. If the video can get over 1 million views than it will be given the value of 1 which equates to viral. If the video would get less than 1 million views then it would be given the value of 0, for not viral.

We chose 1 million views as our differentiating point of viral vs. not viral. Due to a growing number of Internet and social media users, while still a big achievement, reaching that mythical million is no longer as much of a challenge. There are simply too many videos with that many views to make them all stand out. It’s safe to assume that currently, it’s better to aim at gaining at least [1 million views](https://mint.intuit.com/blog/relationships/how-much-do-youtubers-make/) to reap the benefits of going viral. If you can get 1 million views on your video that is the equivialant to about $5,000. So, to answer the question of how many views is viral - there is no simple answer here. In reality, not all viral videos are created equal, so the more views you get, the better, but for our machine learning model's sake, we chose 1 million views.

# Contributors:
1. Zara Khan - zaraxkhan - Circle Role

2. Kevin MacDonald - macdkw89 - Triangle Role

3. Justin Tapia - justint42 - X Role

4. Snehal Desavale - SNEHALDD - Square Role

# Resources

1. Youtube v3 API (https://www.googleapis.com/youtube/v3)
    - All data used in this project is sourced directly from the Youtube API
    - API Resources used
      - Channels
      - Comments
      - CommentThreads
      - Videos

2. Dataset Category References:
   1. [Best Youtube Channels for every category](https://blog.hubspot.com/marketing/best-youtube-channels)
      - Using this article, we obtained each channel listed under each category for our purposes
      - We opted to not use the "Yoga" category due to its similarity to the "Fitness" category.
   2. [List of most-subscribed YouTube channels - Wikipedia](https://en.wikipedia.org/wiki/List_of_most-subscribed_YouTube_channels)
      - Using this link, we sorted the table and grabbed the top 20 English Language channels by subscriber count for use in our analysis
      - There are a handful of duplicate channels in this data when compared to the categorical channel list mentioned above. Our analysis will drop these to avoid duplicate entries.


3. Software :
    - Python 3.9.12
    - Scikit-learn 1.0
    - Numpy 1.21.5
    - pandas 1.4.2
    - psycopg2-binary-2.9.5
    - vaderSentiment - SentimentIntensityAnalyzer

4. Relational Database : PostgresSQL 11 connected to AWS database server.

5. Tools / Software : Tableau public, git, pgAdmin, VS Code.

''')],)

# ------------------------------------------------------------
# Channel Category Metrics
    elif pathname == "/page-1":
        return html.Div([html.H3(children='Video Metrics by Category'),
                         html.Hr(),
                         # Container for first section
                         dbc.Row(children=[
                             # Container for left side of first section
                             dbc.Col(width="auto", children=[
                                 # Label for selections
                                 html.H5('Select metric to view:'),
                                 # Selections
                                 dcc.RadioItems(
                                     id='xaxis', options=[
                                         {'label': ' Views',
                                             'value': 'channel_view_count'},
                                         {'label': ' Subscribers',
                                          'value': 'subscriber_count'},
                                         {'label': ' Videos',
                                             'value': 'channel_video_count'},
                                         {'label': ' Average Video Length',
                                             'value': 'avg_length'},
                                     ],
                                     value='channel_view_count',
                                     labelStyle={'display': 'block'}
                                 ),
                                 # space
                                 html.Hr(),
                                 # Label for category selection
                                 html.H5('Select categories:'),
                                 # Category selection
                                 dcc.Checklist(id='checklist',
                                               options=category_options, value=categories, labelStyle={'display': 'block'}),
                                 # get user input for wether or not to display as log scale
                                 html.Hr(),
                                 html.H5('Display as log scale?'),
                                 dcc.RadioItems(
                                     id='logscale', options=[
                                         {'label': ' Yes',
                                          'value': 'log'},
                                         {'label': ' No',
                                          'value': 'linear'},
                                     ],
                                     value='linear',
                                     labelStyle={'display': 'block'}
                                 ),
                             ]),
                             # Container for right side of first section
                             dbc.Col(width="auto", children=[
                                 # Graph
                                 dcc.Graph(
                                     id='bar-chart',
                                     figure=fig
                                 ),
                                 html.P('Analysis commentary:'),
                             ]),
                         ]),
                         ]
                        )
# ------------------------------------------------------------
# Comment Sentiment Analysis
    elif pathname == "/page-2":
        return html.Div([html.H3(children='Comment Sentiment Analysis by Category'),
                         html.Hr(),
                         # Container for second section
                         dbc.Row(children=[
                             # Container for left side of second section
                             dbc.Col(width='auto', children=[
                                 # Label for selections
                                 html.H5('Select metric to view:'),
                                 # Selections
                                 dcc.RadioItems(
                                     id='xaxis', options=[
                                         {'label': ' Comment Sentiment',
                                             'value': 'sentiment'},
                                     ],
                                     value='sentiment',
                                     labelStyle={'display': 'block'}
                                 ),
                                 # space
                                 html.H1(''),
                                 # Label for category selection
                                 html.H5('Select categories:'),
                                 # Category selection
                                 dcc.Checklist(id='checklist',
                                               options=category_options, value=categories, labelStyle={'display': 'block'}),
                             ]),
                             # Container for right side of second section
                             dbc.Col(width='auto', children=[
                                 # Graph
                                 dcc.Graph(
                                     id='box-plots',
                                     figure=fig2
                                 ),
                             ])
                         ])
                         ]),
# ------------------------------------------------------------
# Video Metrics by Category
    elif pathname == "/page-3":
        return html.Div([html.H3(children='Video Pubishing Time Metrics'),
                         html.Hr(),
                         # Container for third section
                         dbc.Row(children=[
                             # Container for left side of third section
                             # html.Div(className='col-2', children=[
                             #   html.H5(
                             #      'Information about the charts goes here'),
                             # ]),
                             # Container for right side of 4th section
                             dbc.Col(width='auto', children=[
                                 html.H5('Day of Week'),
                                 # Graph
                                 dcc.Graph(
                                     id='histogram',
                                     figure=fig4
                                 ),
                             ]),
                             # Container for right side of 4th section
                             dbc.Col(width='auto', children=[
                                 html.H5('Time of Day (CST)'),
                                 # Graph
                                 dcc.Graph(
                                     id='histogram2',
                                     figure=fig5
                                 ),
                             ])
                         ])
                         ]),
# ------------------------------------------------------------
# Machine Learning
    elif pathname == "/page-4":
        return html.Div([html.H3(children='Machine Learning Analysis'),
                         html.Hr(),
                         # Container for fourth section
                         dbc.Row(children=[
                             # Container for left side of fourth section
                             dcc.Markdown('''
# Machine Learning Model
We are using machine learning to see if we can predict whether or not a YouTube video can reach 1 million views based on its subscriber count, channel view count, channel video count, amount of comments on the video, amount of likes on the video, the topic of the video, and the day of week the video was published. We are using 1 million as our numeric value of whether the video has the potential to be 'viral' or not. Below is the code we used to add the viral or not column from our dataset we created using Youtube's API.

![code_for_viral_column](https://user-images.githubusercontent.com/105755095/201196386-c460bdf2-3feb-4ae8-824c-d409fd4be99e.png)

![code_for_viral_col_2](https://user-images.githubusercontent.com/105755095/201196399-abcbed6b-ef87-45e9-9e08-0f5fac5feae8.png)

# Preprocessing Data
In order to begin the Machine Learning portion, we must preprocess the feature set of the data. First we encoded the categorical data. We did this for the topic category column and the day of week published column. This turned the categorical values into numerical values. However, for the day of week published column, we decided to go with custom encoding so that the days of week were not assigned random numbers, but instead 1 started with Sunday and 7 was Saturday. You can see the code we used below to encode the columns and then add custom encoding to the last column.

![encoding](https://user-images.githubusercontent.com/105755095/201197005-4c819df7-2ba3-4332-9a6a-a1cda5c92744.png)

![custom_encoding](https://user-images.githubusercontent.com/105755095/201197039-dfad346b-38bf-4505-9b05-22d1e5e77de9.png)

![final_custom_encoding](https://user-images.githubusercontent.com/105755095/201197053-f6656825-f06e-40af-9297-fc0e43d008ca.png)

# Scaling the Data
Because our columns had some very large numbers, we thought it would be best to scale each column so that every column was on the same playing field. We did this with Standard Scaler from the sklearn package. This standardizes a feature by subtracting the mean and then scaling to unit variance. Unit variance means dividing all the values by the standard deviation.

![Screen Shot 2022-11-09 at 5 43 19 PM](https://user-images.githubusercontent.com/105755095/201197525-6971f879-26dd-468c-8fb8-8028bbeb0dc8.png)

![scaled_for_ml](https://user-images.githubusercontent.com/105755095/201197546-0f755aef-017f-43a7-9682-0d0374f87dff.png)

# Feature Selection
We selected the features for our machine learning by deciding what data points would effect how much a video is viewed. The first thing we thought of was the channel that posted the video. If the channel has many subscribers than the potential for the video being viewed increases. This is the same thought process we had for the total views the channel has ever had. The more views a channel has had can give a good idea that they are going to continue getting many views. But this can be affected by the amount of videos on their channel. We assumed that the more videos a channel posts, there is a potential that they one of those videos will get many views.

We also thought categorical data was important to include in our feature selection process. We included the topic category of the channel because some topics may get more views than others. Same goes for the day of week the video was published. We wanted to see if there was a correlation between when a video was published to the amount of views that the video will get.

The video data itself also seemed like a legitiment feature to include as the amount of comments a video is getting and being talked about can affect the amount of views a video gets. And finally, we felt as though the like count on a video can be a predictor of whether or not the video will gain attraction.

![Correlation_Matrix](https://user-images.githubusercontent.com/105755095/201199625-ac2f5d9f-c37f-4db8-83ab-1cd9e040fe10.png)

Above shares how the numerical features correlate with one another.

# Splitting Data
We split the data using sklearn's train_test_split function. This split our data as the default 80% for training and 20% for testing.

![train_test_split](https://user-images.githubusercontent.com/105755095/201200037-0217adac-3078-45ac-88c5-94e5fff53e3d.png)

We used this split the first time around for our machine learning portion, before we remebered that our data might be imbalanced. So with the value count function, we checked how many of the rows were given the 1 for 'viral' and how many were given the 0 for 'not viral' and this is what was shown:

![y_value_count](https://user-images.githubusercontent.com/105755095/201200265-1825b3d8-815a-426a-ac93-cfa2c2e8b38a.png)

![percent_targets](https://user-images.githubusercontent.com/105755095/201201604-0a60e710-2e34-4bf0-b954-3306d3b43b92.png)

![graph_target](https://user-images.githubusercontent.com/105755095/201201658-e2d6abe6-268e-4700-8c79-ae75cc993bef.png)

Our data was very imbalanced and we needed to use a function that would balance this data. Our instructor suggested we use SMOTEENN as it does both undersampling and oversampling at the same time. After resampling our data, we rechecked the y values and the numbers we much more balanced than before.

![smoteenn_code](https://user-images.githubusercontent.com/105755095/201200693-6b314a72-9f8f-4cd7-b1aa-7cf092287b8d.png)

# Model Choice
Our group choice 3 different machine learning models for our dataset. We started off with the most obvious choice for binary classification which was the Logistic Regression Model. It is a simple model to use and gave a great accuracy score, however, the precision of the viral target was the lowest of the 3 at 87%. This may be die to the fact that that this model is prone to overfitting on the training data. The next model we chose was the Random Forest Model. It was a little slower than the Logistic Regression Model to train, but was the most effective with the best accuracy, presicion, and recall score. We used this model because it is known for both regression and classification, while also preventing overfitting. The last model we used was Adaboost. This was because we wanted to see if this model would be able to do a better job than the Random Forest Model. It did better than the Logistic Regression Model, however it took a longer time than any of the models to train and since our model has a lot of outliars, it was not the best fit for our dataset. We considered it beacause it is refressed to as the best classifier, but due to the outliars in our model, it was not for our dataset. Random Forest did a great job in processing our features and performing on our testing data.

# Changes in our Model
The biggest change we made to our model was when we resampled our data and redid the machine learning for all 3 models. This showed a great change in our Classification Reports, especially when it came to the precision of our models calculating if the video was viral. Below are the classification reports and the changes that occured due to the resampling.
# Logistic Regression
Before Resampling:

![ClassReport_LR](https://user-images.githubusercontent.com/105755095/201206248-13f8a908-6056-414e-b91d-a0e5bf9ac25b.png)


After Resampling:

![ClassReport_LR_RS](https://user-images.githubusercontent.com/105755095/201206278-5cf319b3-11e6-4bdd-b67a-0eb44465187c.png)


# Random Forest Model
Before Resampling:

![CLassReport_RF](https://user-images.githubusercontent.com/105755095/201206363-226ac289-1b57-4377-94ae-5356479712d4.png)


After Resampling:

![ClassReport_RF_RS](https://user-images.githubusercontent.com/105755095/201206387-41423988-3526-465e-86ca-08daf3aa6173.png)

# Easy Ensemble AdaBoost Model
Before Resample:

![ClassReport_EE](https://user-images.githubusercontent.com/105755095/201206215-6c0452b4-3393-4cc3-b3a8-9672e189db49.png)


After Resampling:

![CR_EE_RS](https://user-images.githubusercontent.com/105755095/201206472-db0b4660-9d28-4e48-881b-92bae96a77cc.png)


# Results from our Machine Learning Model
The RandomForest model did a great job in training and learning which features make for a viral video. Giving us an almost 98% accuracy score, the model is able to predict with the features which video will gain 1 million views. It was able to even categorize which features were the most important when making it's calculations:

![Feature_Importance](https://user-images.githubusercontent.com/105755095/201209337-1609cb8a-8209-46b5-8264-0f813bcbe025.png)

Below are the accuracy scores for all 3 models we used;

# Logistic Regression
Before Resampling:

![AccuracyScore_LR](https://user-images.githubusercontent.com/105755095/201204409-790dad59-f1ea-4fe1-824d-6353902b1a0a.png)


After Resampling:

![accuracyscore_LR_RS](https://user-images.githubusercontent.com/105755095/201204415-13f1e1ab-1617-44bf-b2ff-7f6f61cd9f35.png)


# Random Forest Model
Before Resampling:

![AccuracyScore_RF](https://user-images.githubusercontent.com/105755095/201204440-286a1556-99ff-490d-a411-3265f57eb218.png)


After Resampling:

![AccuracyScore_RF_RS](https://user-images.githubusercontent.com/105755095/201204461-dfc1b217-de1f-4c6b-b6d3-91a83f0132fb.png)


# Easy Ensemble AdaBoost Model
Before Resample:

![AccuracyScore_EE](https://user-images.githubusercontent.com/105755095/201204358-c2d05b99-23a8-434b-aaaa-ffcfee964a18.png)

After Resample:

![AccuracyScore_EE_RS](https://user-images.githubusercontent.com/105755095/201204399-585b0d69-bda0-4249-95a9-c5f89449df3d.png)''', style={'margin-right': '2%'}),
                         ]),
                         ]),
# ------------------------------------------------------------
# Top Channels
    elif pathname == "/page-5":
        return html.Div([html.H3(children='Top Channel Metrics'),
                         html.Hr(),
                         # Container for first section
                         dbc.Row(children=[
                             # Container for left side of first section
                             dbc.Col(width='auto', children=[
                                 # Label for selections
                                 html.H5('Select metric to view:'),
                                 # Selections
                                 dcc.RadioItems(
                                     id='yaxis', options=[
                                         {'label': ' Views',
                                          'value': 'view_count'},
                                         {'label': ' Subscribers',
                                          'value': 'subscriber_count'},
                                         {'label': ' Comments',
                                             'value': 'comment_count'},

                                     ],
                                     value='view_count',
                                     labelStyle={'display': 'block'}
                                 ),
                                 html.Hr(),
                                 html.H5('Select:'),
                                 dcc.RadioItems(
                                     id='tot-mean', options=[
                                         {'label': ' Average',
                                          'value': 'mean'},
                                         {'label': ' Total',
                                          'value': 'sum'},
                                     ],
                                     value='mean',
                                     labelStyle={'display': 'block'}
                                 ),

                             ]),
                             # Container for right side of first section
                             dbc.Col(width='auto', children=[
                                 # Graph
                                 dcc.Graph(
                                     id='top-channels',
                                     figure=fig6
                                 ),
                                 html.P(
                                     'Analysis commentary: Video Count is disabled due to bug')
                             ]),
                         ]),
                         ]
                        )
# ------------------------------------------------------------
# Tableau Dashboard
    elif pathname == "/page-6":
        # imbed tableau dashboard
        return html.Div([html.H3(children='Tableau Dashboard'),
                         html.Hr(),
                         # add link to visit tableau dashboard
                         dbc.Row(children=[

                             html.A('Click here to view in Tableau Public',
                                    href='https://public.tableau.com/app/profile/snehal.desavale/viz/YoutubeVideoAnalysis_16680643134020/Dashboard', target='_blank'),

                         ]),
                         # display tableau.html
                         html.Iframe(srcDoc=open(
                             'tableau.html', 'r').read(), width='100%', height='1000')
                         ])
# ------------------------------------------------------------
# ML Viz
    elif pathname == "/page-7":
        return html.Div([html.Div(className='top-container', children=[html.H3(children='Machine Learning Visualization')]),
                         html.Hr(),
                         # Container for first section
                         dbc.Row(children=[
                             html.H5('Select features:'),
                             # Container for left side of first section
                             dbc.Col(width='auto', children=[
                                 # Label for selections
                                 html.P('Feature 1 (X):'),
                                 # Selections
                                 dcc.RadioItems(
                                     id='ml-feature-1', options=ml_viz_options_num,
                                     value='view_count',
                                     labelStyle={'display': 'block'}
                                 ),
                                 html.Hr(),
                                 html.P('Feature 2 (Y):'),
                                 dcc.RadioItems(
                                     id='ml-feature-2', options=ml_viz_options_num,
                                     value='video_length_seconds',
                                     labelStyle={'display': 'block'}
                                 ),
                                 html.Hr(),
                                 html.P('Feature 3 (Z):'),
                                 dcc.RadioItems(
                                     id='ml-feature-3', options=ml_viz_options_num,
                                     value='comment_count',
                                     labelStyle={'display': 'block'}
                                 ),

                             ]),
                             dbc.Col(width=2, children=[
                                 html.P('Feature 4 (Color):'),
                                 dcc.RadioItems(
                                     id='ml-feature-4', options=ml_viz_options_color,
                                     value='topic_category',
                                     labelStyle={'display': 'block'}
                                 ),
                                 html.Hr(),
                                 html.P('Feature 5 (Shape):'),
                                 dcc.RadioItems(
                                     id='ml-feature-5', options=ml_viz_options_symbol,
                                     value='day_of_week_published',
                                     labelStyle={'display': 'block'}
                                 ),
                                 html.Hr(),
                                 html.H5('Filter by:'),
                                 html.P('Video Length (seconds):'),
                                 dcc.RangeSlider(
                                     id='ml-video-length',
                                     min=0,
                                     max=4.633,
                                     step=.001,
                                     value=[0, 4.633],
                                     marks={
                                        0: '0',
                                        4.633*.25: '15s',
                                        4.633*.5: '200s',
                                        4.633*.75: '3000s',
                                        4.633: 'Max'},
                                 ),
                                 html.Hr(),

                                 html.P('Video Views:'),
                                 dcc.RangeSlider(
                                     id='ml-video-views',
                                     min=0,
                                     max=9.317,
                                     step=.001,
                                     value=[0, 9.317],
                                     marks={
                                        0: '0',
                                        9.317*.25: '200',
                                        9.317*.5: '50k',
                                        9.317*.75: '10M',
                                        9.317: 'Max'}
                                 ),
                                 html.Hr(),

                             ]),
                             # Container for right side of first section
                             dbc.Col(width='auto', style={'height': '100%'},
                                     children=[
                                 # Graph
                                 dcc.Graph(
                                     id='ml-viz',
                                     figure=fig8,
                                     loading_state={'is_loading': True}

                                 ),
                             ]),
                         ]),
                         ]
                        )
# ------------------------------------------------------------
# Length Analysis
    elif pathname == "/page-8":
        return html.Div([html.H3(children='Video Length Analysis'),
                         html.Hr(),
                         dbc.Row(children=[
                             dbc.Col(width='auto', children=[
                                 html.H5('Select features to view:'),
                                 html.Hr(),
                                 html.P('Feature 1 (X):'),

                             ]),
                             dbc.Col(width='auto', children=[
                                 dcc.Graph(
                                     id='video-length-viz',
                                     figure=fig9
                                 ),
                             ]),
                         ]),
                         ]
                        )
# ------------------------------------------------------------
# Error404
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


@app.callback(
    Output('bar-chart', 'figure'),
    [Input('checklist', 'value'),
     Input('xaxis', 'value'),
     Input('logscale', 'value')],)
def update_graph(checklist, xaxis, logscale):
    filtered_df = category_data_new[category_data_new.topic_category.isin(
        checklist)]
    fig = px.bar(filtered_df.sort_values(xaxis, ascending=False), template=template,
                 x="topic_category", y=xaxis, title=f'Video Metrics by Category', height=600, width=1000,
                 labels={'topic_category': 'Category', 'channel_view_count': 'Total Views', 'subscriber_count': 'Subscribers', 'channel_video_count': 'Channel Video Count', 'avg_length': 'Average Video Length'})
    fig.update_traces(marker_color='red')
    if logscale == 'log':
        fig.update_yaxes(type='log')
    else:
        fig.update_yaxes(type='linear')
    return fig


@app.callback(
    Output('box-plots', 'figure'),
    [Input('checklist', 'value'),
     Input('xaxis', 'value')],)
def update_graph(checklist, xaxis):
    filtered_df = video_sentiment_data[video_sentiment_data.topic_category.isin(
        checklist)]
    fig = px.box(filtered_df, template=template, labels={'topic_category': 'Category', 'sentiment': 'Sentiment Score'},
                 x="topic_category", y=xaxis, title=f'Total {xaxis} by Category', height=800, width=1200)
    fig.update_traces(marker_color='red')
    return fig


@app.callback(
    Output('top-channels', 'figure'),
    [Input('yaxis', 'value'),
     Input('tot-mean', 'value')],)
def update_graph(yaxis, totmean):
    alt_df = mega_df2.groupby('channel_id_x').agg({'subscriber_count': totmean, 'view_count': totmean, 'comment_count': totmean,
                                                   'sentiment': totmean, 'video_length_seconds': totmean, 'topic_category': 'first', 'custom_url': 'first'}).reset_index()
    fig = px.bar(alt_df.sort_values(yaxis, ascending=False).head(20), orientation='h',
                 y="custom_url", x=yaxis, title='Top Channels', color='topic_category', template=template, height=600, width=1000)
    fig.update_layout(yaxis_categoryorder='total ascending')
    return fig


@app.callback(
    Output('ml-viz', 'figure'), [
        Input('ml-feature-1', 'value'),
        Input('ml-feature-2', 'value'),
        Input('ml-feature-3', 'value'),
        Input('ml-feature-4', 'value'),
        Input('ml-feature-5', 'value'),
        Input('ml-video-length', 'value'),
        Input('ml-video-views', 'value'),
    ],)
def update_graph(feature1, feature2, feature3, feature4, feature5, length, views):
    if feature5 == 'none':
        if feature4 == 'none':
            fig = px.scatter_3d(mega_df2[(mega_df2['video_length_seconds'] >= transform_value(length[0])) & (mega_df2['video_length_seconds'] <= transform_value(length[1])) & (mega_df2['view_count'] >= transform_value(views[0])) & (mega_df2['view_count'] <= transform_value(views[1]))], template=template,
                                x=feature1, y=feature2, z=feature3, height=800, width=1024, log_x=True, log_y=True, log_z=True,
                                labels={'video_length_seconds': 'Video Length (seconds)', 'view_count': 'Video Views', 'comment_count': "Number of Video Comments",
                                'topic_category': 'Category', 'channel_title': 'Channel', 'day_of_week_published': 'Day of Week Published'},
                                hover_data=['custom_url', 'topic_category', 'view_count', 'video_length_seconds'])
        else:
            fig = px.scatter_3d(mega_df2[(mega_df2['video_length_seconds'] >= transform_value(length[0])) & (mega_df2['video_length_seconds'] <= transform_value(length[1])) & (mega_df2['view_count'] >= transform_value(views[0])) & (mega_df2['view_count'] <= transform_value(views[1]))], template=template,
                                x=feature1, y=feature2, z=feature3, color=feature4, height=800, width=1024, log_x=True, log_y=True, log_z=True,
                                labels={'video_length_seconds': 'Video Length (seconds)', 'view_count': 'Video Views', 'comment_count': "Number of Video Comments",
                                'topic_category': 'Category', 'channel_title': 'Channel', 'day_of_week_published': 'Day of Week Published'},
                                hover_data=['custom_url', 'topic_category', 'view_count', 'video_length_seconds'])
    elif feature4 == 'none':
        fig = px.scatter_3d(mega_df2[(mega_df2['video_length_seconds'] >= transform_value(length[0])) & (mega_df2['video_length_seconds'] <= transform_value(length[1])) & (mega_df2['view_count'] >= transform_value(views[0])) & (mega_df2['view_count'] <= transform_value(views[1]))], template=template,
                            x=feature1, y=feature2, z=feature3, symbol=feature5, height=800, width=1024, log_x=True, log_y=True, log_z=True,
                            labels={'video_length_seconds': 'Video Length (seconds)', 'view_count': 'Video Views', 'comment_count': "Number of Video Comments",
                                    'topic_category': 'Category', 'channel_title': 'Channel', 'day_of_week_published': 'Day of Week Published'},
                            hover_data=['custom_url', 'topic_category', 'view_count', 'video_length_seconds'])
    else:
        fig = px.scatter_3d(mega_df2[(mega_df2['video_length_seconds'] >= transform_value(length[0])) & (mega_df2['video_length_seconds'] <= transform_value(length[1])) & (mega_df2['view_count'] >= transform_value(views[0])) & (mega_df2['view_count'] <= transform_value(views[1]))], template=template,
                            x=feature1, y=feature2, z=feature3, color=feature4, symbol=feature5, height=800, width=1024, log_x=True, log_y=True, log_z=True,
                            labels={'video_length_seconds': 'Video Length (seconds)', 'view_count': 'Video Views', 'comment_count': "Number of Video Comments",
                                    'topic_category': 'Category', 'channel_title': 'Channel', 'day_of_week_published': 'Day of Week Published'},
                            hover_data=['custom_url', 'topic_category', 'view_count', 'video_length_seconds'])

    fig.update_traces(marker=dict(size=3, line=dict(width=1, color='DarkSlateGrey')),
                      selector=dict(mode='markers'))
    # if feature1 is Sentiment Score, change log_x to False
    if feature1 == 'sentiment':
        fig.update_layout(scene=dict(xaxis=dict(type='linear')))
    # if feature2 is Sentiment Score, change log_y to False
    if feature2 == 'sentiment':
        fig.update_layout(scene=dict(yaxis=dict(type='linear')))
    # if feature3 is Sentiment Score, change log_z to False
    if feature3 == 'sentiment':
        fig.update_layout(scene=dict(zaxis=dict(type='linear')))
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor="Black"
    )
    # increase legend symbol size
    fig.update_layout(legend=dict(
        font=dict(
            size=12,
        )
    ))

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
