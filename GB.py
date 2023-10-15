import pandas as pd
import holoviews as hv
hv.extension('bokeh')
from bokeh.plotting import figure, show, output_file
from bokeh.models import Range1d, LinearAxis, ColumnDataSource
from bokeh.models.tools import HoverTool


#downloading and reading data using pandas
url_cases_spec = 'https://coronavirus.data.gov.uk/api/v1/data?filters=areaType=overview&structure=%7B%22areaType%22:%22areaType%22,%22areaName%22:%22areaName%22,%22areaCode%22:%22areaCode%22,%22date%22:%22date%22,%22newCasesBySpecimenDate%22:%22newCasesBySpecimenDate%22,%22cumCasesBySpecimenDate%22:%22cumCasesBySpecimenDate%22%7D&format=csv'
url_cases_rep = 'https://coronavirus.data.gov.uk/api/v1/data?filters=areaType=overview&structure=%7B%22areaType%22:%22areaType%22,%22areaName%22:%22areaName%22,%22areaCode%22:%22areaCode%22,%22date%22:%22date%22,%22newCasesByPublishDate%22:%22newCasesByPublishDate%22,%22cumCasesByPublishDate%22:%22cumCasesByPublishDate%22%7D&format=csv'
url_hosp_adm = 'https://coronavirus.data.gov.uk/api/v1/data?filters=areaType=overview&structure=%7B%22areaType%22:%22areaType%22,%22areaName%22:%22areaName%22,%22areaCode%22:%22areaCode%22,%22date%22:%22date%22,%22newAdmissions%22:%22newAdmissions%22,%22cumAdmissions%22:%22cumAdmissions%22%7D&format=csv'
url_deaths_dd = 'https://coronavirus.data.gov.uk/api/v1/data?filters=areaType=overview&structure=%7B%22areaType%22:%22areaType%22,%22areaName%22:%22areaName%22,%22areaCode%22:%22areaCode%22,%22date%22:%22date%22,%22newDeaths28DaysByDeathDate%22:%22newDeaths28DaysByDeathDate%22,%22cumDeaths28DaysByDeathDate%22:%22cumDeaths28DaysByDeathDate%22%7D&format=csv'
url_deaths_rep = 'https://coronavirus.data.gov.uk/api/v1/data?filters=areaType=overview&structure=%7B%22areaType%22:%22areaType%22,%22areaName%22:%22areaName%22,%22areaCode%22:%22areaCode%22,%22date%22:%22date%22,%22newDeaths28DaysByPublishDate%22:%22newDeaths28DaysByPublishDate%22,%22cumDeaths28DaysByPublishDate%22:%22cumDeaths28DaysByPublishDate%22%7D&format=csv'


#initializing columns
cases_spec_data_pre = pd.read_csv(url_cases_spec, sep=',', header=0, skipinitialspace=True, usecols=[3,4], parse_dates=['date'])
cases_rep_data_pre = pd.read_csv(url_cases_rep, sep=',', header=0, skipinitialspace=True, usecols=[3,4], parse_dates=['date'])
hosp_adm_data_pre = pd.read_csv(url_hosp_adm, sep=',', header=0, skipinitialspace=True, usecols=[3,4], parse_dates=['date'])
deaths_dd_data_pre = pd.read_csv(url_deaths_dd, sep=',', header=0, skipinitialspace=True, usecols=[3,4], parse_dates=['date'])
deaths_rep_data_pre = pd.read_csv(url_deaths_rep, sep=',', header=0, skipinitialspace=True, usecols=[3,4], parse_dates=['date'])


#cleaning the NaNs
cases_spec_data = cases_spec_data_pre.fillna(0)
cases_rep_data = cases_rep_data_pre.fillna(0)
hosp_adm_data = hosp_adm_data_pre.fillna(0)
deaths_dd_data = deaths_dd_data_pre.fillna(0)
deaths_rep_data = deaths_rep_data_pre.fillna(0)

GB_pop = 66.65 #Millionen


#7-Day avg. for dataframe
def data_to_7D(dataframe):
    moving_average = []
    for i1 in range(len(dataframe)-7):
        moving_average_temp = 0
        for i2 in range(i1,i1+7):
            moving_average_temp += dataframe.loc[i2]
        moving_average.append(moving_average_temp)
    SD_moving_average = [moving_average[i]/7/GB_pop for i in range(len(moving_average))]
    return SD_moving_average


#column data source
COV_data_source = ColumnDataSource(data=dict(
    cases_spec_7Dma = data_to_7D(cases_spec_data['newCasesBySpecimenDate']),
    cases_rep_7Dma = data_to_7D(cases_rep_data['newCasesByPublishDate']),
    hosp_adm_7Dma = data_to_7D(hosp_adm_data['newAdmissions']),
    deaths_dd_7Dma = data_to_7D(deaths_dd_data['newDeaths28DaysByDeathDate']),
    deaths_rep_7Dma = data_to_7D(deaths_rep_data['newDeaths28DaysByPublishDate']),
    time_cases_rep = cases_rep_data['date'],
    time_cases_spec = cases_spec_data['date'],
    time_hosp_adm = hosp_adm_data['date'],
    time_deaths_dd = deaths_dd_data['date'],
    time_deaths_rep = deaths_rep_data['date'],
))


#Hovertools
hover_cases_spec = HoverTool(name = 'cases by specimen date: 7-Day moving average',
    tooltips = [
        ('cases (specimen date)', '@cases_spec_7Dma{0,000}'),
        ('date (7-Day moving average)', '@time_cases_spec{%F}')
    ], formatters={'@time_cases_spec': 'datetime'}
)

hover_cases_rep = HoverTool(name = 'cases by report date: 7-Day moving average',
    tooltips = [
        ('cases (report date)', '@cases_rep_7Dma{0,000}'),
        ('date (7-Day moving average)', '@time_cases_rep{%F}')
    ], formatters={'@time_cases_rep': 'datetime'}
)

hover_hosp_adm = HoverTool(name = 'hospital admissions: 7-Day moving average',
    tooltips = [
        ('hospital admissions', '@hosp_adm_7Dma{0.0}'),
        ('date (7-Day moving average)', '@time_hosp_adm{%F}')
    ], formatters={'@time_hosp_adm': 'datetime'}
)

hover_deaths_dd = HoverTool(name = 'deaths by date of death: 7-Day moving average',
    tooltips = [
        ('deaths (date of death)', '@deaths_dd_7Dma{0.00}'),
        ('date (7-Day moving average)', '@time_deaths_dd{%F}')
    ], formatters={'@time_deaths_dd': 'datetime'}
)

hover_deaths_rep = HoverTool(name = 'deaths by report date: 7-Day moving average',
    tooltips = [
        ('deaths (report date)', '@deaths_rep_7Dma{0.00}'),
        ('date (7-Day moving average)', '@time_deaths_rep{%F}')
    ], formatters={'@time_deaths_rep': 'datetime'}
)


#timestamp
timestamp = cases_rep_data['date'].loc[0]
print(timestamp)


#figure
p = figure(
    title = f'SARS-CoV-2: United Kingdom ({timestamp})', 
    width = 1200, 
    height = 600, 
    x_axis_type='datetime',
)


#LHS y-axis cases
p.yaxis.axis_label = 'number of cases per capita'
case_start = -0.05 * max(cases_spec_data['newCasesBySpecimenDate']) / GB_pop
case_end = 1.05 * max(cases_spec_data['newCasesBySpecimenDate']) / GB_pop
p.y_range = Range1d(start = case_start, end = case_end)

#RHS y-axis hosps
rfactor = max(cases_spec_data['newCasesBySpecimenDate'])* max(data_to_7D(hosp_adm_data['newAdmissions'])) / 918.3924552566713
hosp_start = -0.05 * rfactor / GB_pop
hosp_end = 1.05 * rfactor / GB_pop
p.extra_y_ranges['rhosp'] = Range1d(start = hosp_start, end = hosp_end)
p.add_layout(LinearAxis(y_range_name='rhosp', axis_label='number of hospital admissions per capita'), 'right')

#RHS y-axis 2 deaths
rfactor2 = max(cases_spec_data['newCasesBySpecimenDate'])* max(data_to_7D(deaths_dd_data['newDeaths28DaysByDeathDate'])) / 918.3924552566713
death_start = -0.05 * rfactor2 / GB_pop
death_end = 1.05 * rfactor2 / GB_pop
p.extra_y_ranges['rdeath'] = Range1d(start = death_start, end = death_end)
p.add_layout(LinearAxis(y_range_name='rdeath', axis_label='number of deaths (within 28 days of positive test) per capita'), 'right')


#cases by specimen date
p.line(
    x = cases_spec_data['date'], y = cases_spec_data['newCasesBySpecimenDate'] / GB_pop,
    line_color = (50, 150, 250), 
    line_width = 1.5,
    line_alpha = 0.2,
)

p.line(
    x = 'time_cases_spec', y = 'cases_spec_7Dma', source = COV_data_source,
    line_color = (50, 150, 250),
    legend_label = 'cases (specimen date)',
    line_width = 1.5,
    line_alpha = 1,
    name = 'cases by specimen date: 7-Day moving average',
)


#cases by report date
p.line(
    x = cases_rep_data['date'], y = cases_rep_data['newCasesByPublishDate'] / GB_pop,
    line_color = 'blue',
    line_width = 1.5,
    line_alpha = 0.2,
)

p.line(
    x = 'time_cases_rep', y = 'cases_rep_7Dma', source = COV_data_source,
    line_color = 'blue',
    legend_label = 'cases (report date)',
    line_width = 1.5,
    line_alpha = 0.75,
    name = 'cases by report date: 7-Day moving average',
)


#hospital admissions
p.line(
    x = hosp_adm_data['date'], y = hosp_adm_data['newAdmissions'] / GB_pop,
    line_color = 'red',
    line_width = 1.5,
    line_alpha = 0.2,
    y_range_name = 'rhosp',
)

p.line(
    x = 'time_hosp_adm', y = 'hosp_adm_7Dma', source = COV_data_source,
    line_color = 'red',
    legend_label = 'hospital admissions',
    line_width = 1.5,
    line_alpha = 1,
    y_range_name = 'rhosp',
    name = 'hospital admissions: 7-Day moving average',
)


#deaths by date of death
p.line(
    x = deaths_dd_data['date'], y = deaths_dd_data['newDeaths28DaysByDeathDate'] / GB_pop,
    line_color = (150, 50, 250), 
    line_width = 1.5,
    line_alpha = 0.2,
    y_range_name = 'rdeath',
)

p.line(
    x = 'time_deaths_dd', y = 'deaths_dd_7Dma', source = COV_data_source,
    line_color = (150, 50, 250),
    legend_label = 'deaths (date of death)',
    line_width = 1.5,
    line_alpha = 1,
    y_range_name = 'rdeath',
    name = 'deaths by date of death: 7-Day moving average',
)


#deaths by report date
p.line(
    x = deaths_rep_data['date'], y = deaths_rep_data['newDeaths28DaysByPublishDate'] / GB_pop,
    line_color = 'black',
    line_width = 1.5,
    line_alpha = 0.2,
    y_range_name = 'rdeath',
)

p.line(
    x = 'time_deaths_rep', y = 'deaths_rep_7Dma', source = COV_data_source,
    line_color = 'black',
    legend_label = 'deaths (report date)',
    line_width = 1.5,
    line_alpha = 0.75,
    y_range_name = 'rdeath',
    name = 'deaths by report date: 7-Day moving average',
)


#axis formatting
##p.title.text_font = 'Computer Modern Roman'
#p.axis.axis_label_text_font = 'Computer Modern Roman'
#p.axis.axis_label_text_font_size = '16px'
#p.axis.axis_label_text_font_style = 'normal'
#p.axis.major_label_text_font = 'Computer Modern Roman'


#adding hovertools
p.add_tools(hover_cases_spec)
p.add_tools(hover_cases_rep)
p.add_tools(hover_hosp_adm)
p.add_tools(hover_deaths_dd)
p.add_tools(hover_deaths_rep)

#minorticks
p.ygrid.minor_grid_line_color = 'navy'
p.ygrid.minor_grid_line_alpha = 0.05

#p.xgrid.minor_grid_line_color = 'navy'
#p.xgrid.minor_grid_line_alpha = 0.05

p.legend.location = 'top_left'
output_file(filename = "index.html")  
show(p)