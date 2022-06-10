from taipy.gui import Gui, notify
import pandas as pd
import webbrowser
import datetime

section_1="""
<center>
<|navbar|lov={[("page1", "This Page"), ("https://docs.taipy.io/en/latest/manuals/about/", "Taipy Docs"), ("https://docs.taipy.io/en/latest/getting_started/", "Getting Started")]}|>
</center>

Data Dashboard with Taipy
=========================
<|layout|columns=1 3|
<|
###let's create a simple Data Dashboard!
<br/> 
<center>
<|file_selector|label=Upload Dataset|>
</center>
|>
<|
<center>
<|{logo}|image|height=250px|width=250px|on_action=image_action|>
</center>
|>
|>
"""

section_2 = """
##Data Visualization
<|{dataset}|chart|mode=lines|x=Date|y[1]=MinTemp|y[2]=MaxTemp|color[1]=blue|color[2]=red|>
"""

section_3 = """
<|layout|columns= 1 5|
<|
## Custom Parameters
**Starting Date**\n\n<|{start_date}|date|not with_time|on_change=start_date_onchange|>
<br/><br/>
**Ending Date**\n\n<|{end_date}|date|not with_time|on_change=end_date_onchange|>
<br/>
<br/>
<|button|label=GO|on_action=button_action|>
|>
<|
<center> <h2>Dataset</h2><|{download_data}|file_download|on_action=download|>
</center>
<center>
<|{dataset}|table|page_size=10|height=500px|width=65%|>
</center>
|>
|>
"""
def image_action(state):
    webbrowser.open("https://taipy.io")

def get_data(path: str):
    dataset = pd.read_csv(path)
    dataset["Date"] = pd.to_datetime(dataset["Date"]).dt.date
    return dataset

def start_date_onchange(state, var_name, value):
    state.start_date = value.date()

def end_date_onchange(state, var_name, value):
    state.end_date = value.date()

def filter_by_date_range(dataset, start_date, end_date):
    mask = (dataset['Date'] > start_date) & (dataset['Date'] <= end_date)
    return dataset.loc[mask]

def button_action(state):
    state.dataset = filter_by_date_range(dataset, state.start_date, state.end_date)
    notify(state, "info", "Updated date range from {} to {}.".format(state.start_date.strftime("%m/%d/%Y"), state.end_date.strftime("%m/%d/%Y")))

def download(state):
    state.dataset.to_csv('download.csv')
    state.download_data = 'download.csv'

logo = "images/taipy_logo.jpg"
dataset = get_data("datasets/weather.csv")
start_date = datetime.date(2008, 12, 1)
end_date = datetime.date(2017, 6, 25)

Gui(page=section_1+section_2+section_3).run(dark_mode=False)