import pandas as pd
import matplotlib.pyplot as plt
#from matplotlib.pyplot import figure
#import matplotlib.dates as mdates
#from mpl_toolkits.axes_grid1 import host_subplot



#downloading and reading data using pandas
url_cases_spec = 'https://coronavirus.data.gov.uk/api/v1/data?filters=areaType=overview&structure=%7B%22areaType%22:%22areaType%22,%22areaName%22:%22areaName%22,%22areaCode%22:%22areaCode%22,%22date%22:%22date%22,%22newCasesBySpecimenDate%22:%22newCasesBySpecimenDate%22,%22cumCasesBySpecimenDate%22:%22cumCasesBySpecimenDate%22%7D&format=csv'
url_cases_rep = 'https://coronavirus.data.gov.uk/api/v1/data?filters=areaType=overview&structure=%7B%22areaType%22:%22areaType%22,%22areaName%22:%22areaName%22,%22areaCode%22:%22areaCode%22,%22date%22:%22date%22,%22newCasesByPublishDate%22:%22newCasesByPublishDate%22,%22cumCasesByPublishDate%22:%22cumCasesByPublishDate%22%7D&format=csv'
url_hosp_adm = 'https://coronavirus.data.gov.uk/api/v1/data?filters=areaType=overview&structure=%7B%22areaType%22:%22areaType%22,%22areaName%22:%22areaName%22,%22areaCode%22:%22areaCode%22,%22date%22:%22date%22,%22newAdmissions%22:%22newAdmissions%22,%22cumAdmissions%22:%22cumAdmissions%22%7D&format=csv'
url_deaths_dd = 'https://coronavirus.data.gov.uk/api/v1/data?filters=areaType=overview&structure=%7B%22areaType%22:%22areaType%22,%22areaName%22:%22areaName%22,%22areaCode%22:%22areaCode%22,%22date%22:%22date%22,%22newDeaths28DaysByDeathDate%22:%22newDeaths28DaysByDeathDate%22,%22cumDeaths28DaysByDeathDate%22:%22cumDeaths28DaysByDeathDate%22%7D&format=csv'
url_deaths_rep = 'https://coronavirus.data.gov.uk/api/v1/data?filters=areaType=overview&structure=%7B%22areaType%22:%22areaType%22,%22areaName%22:%22areaName%22,%22areaCode%22:%22areaCode%22,%22date%22:%22date%22,%22newDeaths28DaysByPublishDate%22:%22newDeaths28DaysByPublishDate%22,%22cumDeaths28DaysByPublishDate%22:%22cumDeaths28DaysByPublishDate%22%7D&format=csv'

cases_spec_data = pd.read_csv(url_cases_spec, sep=',', header=0, skipinitialspace=True, usecols=[3,4], parse_dates=['date'])
cases_rep_data = pd.read_csv(url_cases_rep, sep=',', header=0, skipinitialspace=True, usecols=[3,4], parse_dates=['date'])
hosp_adm_data = pd.read_csv(url_hosp_adm, sep=',', header=0, skipinitialspace=True, usecols=[3,4], parse_dates=['date'])
deaths_dd_data = pd.read_csv(url_deaths_dd, sep=',', header=0, skipinitialspace=True, usecols=[3,4], parse_dates=['date'])
deaths_rep_data = pd.read_csv(url_deaths_rep, sep=',', header=0, skipinitialspace=True, usecols=[3,4], parse_dates=['date'])

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
    for i3 in range(len(dataframe)-7, len(dataframe)):
        SD_moving_average.append(dataframe[i3]/GB_pop)
    return SD_moving_average


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


diggawhat = cases_rep_data['date'].loc[0]
#diggawhat2 = diggawhat[:diggawhat.find(' ')]
print(diggawhat)

#figure
# p = figure(
#     title = f'SARS-CoV-2: United Kingdom ({diggawhat})', 
#     plot_width = 1200, 
#     plot_height = 600, 
#     x_axis_type='datetime',
# )


#LHS y-axis
#p.yaxis.axis_label = 'number of cases per capita'
#p.y_range = Range1d(start=-0.05 * max(cases_spec_data['newCasesBySpecimenDate']) / GB_pop, end=1.05 * max(cases_spec_data['newCasesBySpecimenDate']) / GB_pop)

#RHS y-axis hosps
rfactor = max(cases_spec_data['newCasesBySpecimenDate'])* max(data_to_7D(hosp_adm_data['newAdmissions'])) / max(data_to_7D(cases_spec_data['newCasesBySpecimenDate']))

#p.extra_y_ranges['rhosp'] = Range1d(start=-0.05 * rfactor / GB_pop, end=1.05 * rfactor / GB_pop)
#p.add_layout(LinearAxis(y_range_name='rhosp', axis_label='number of hospital admissions per capita'), 'right')

#deaths
rfactor2 = max(cases_spec_data['newCasesBySpecimenDate'])* max(data_to_7D(deaths_dd_data['newDeaths28DaysByDeathDate'])) / max(data_to_7D(cases_spec_data['newCasesBySpecimenDate']))

#p.extra_y_ranges['rdeath'] = Range1d(start=-0.05 * rfactor2 / GB_pop, end=1.05 * rfactor2 / GB_pop)
#p.add_layout(LinearAxis(y_range_name='rdeath', axis_label='number of deaths (within 28 days of positive test) per capita'), 'right')

#fig, ax1 = plt.subplots()
fig = plt.figure(figsize=(12, 6))

plt.xlabel('date')
plt.ylabel('number of cases per capita')
#plt.set_xlabel('date')
#plt.set_ylabel('number of cases per capita')
#ax1.xticks(rotation=45)
#plt.tick_params(axis='y')

ax2 = plt.twinx()
ax2.set_ylabel('number of hospital admissions per capita') 

ax3 = plt.twinx()  
ax3.set_ylabel('number of deaths (within 28 days of positive test) per capita') 

#ax2.spines["right"].set_position(("axes", 1.2))
#ax2.spines["right"].set_visible(True)

plt.plot_date(
    cases_spec_data['date'], 
    cases_spec_data['newCasesBySpecimenDate'] / GB_pop, 
    color=(50/255, 150/255, 250/255), 
    linestyle='solid', 
    linewidth=1, 
    markersize = 0, 
    alpha= 0.2)

plt.plot_date(
    time_cases_spec[0], 
    cases_spec_7Dma[0], 
    color=(50/255, 150/255, 250/255), 
    linestyle='solid', 
    linewidth=1, 
    markersize = 0, 
    alpha=1,
    label='cases (specimen date)')


plt.plot_date(
    cases_rep_data['date'], 
    cases_rep_data['newCasesByPublishDate'] / GB_pop, 
    color='blue', 
    linestyle='solid', 
    linewidth=1, 
    markersize = 0, 
    alpha= 0.2)

plt.plot_date(
    time_cases_rep[0], 
    cases_rep_7Dma[0], 
    color='blue', 
    linestyle='solid', 
    linewidth=1, 
    markersize = 0, 
    alpha=1,
    label='cases (report date)')



ax2.plot_date(
    time_hosp_adm[0], 
    hosp_adm_data['newAdmissions'] / GB_pop, 
    color='red', 
    linestyle='solid', 
    linewidth=1, 
    markersize = 0, 
    alpha= 0.2)

ax2.plot_date(
    time_hosp_adm[0], 
    hosp_adm_7Dma[0], 
    color='red', 
    linestyle='solid', 
    linewidth=1, 
    markersize = 0, 
    alpha=1,
    label='hospital admissions')


ax3.plot_date(
    deaths_dd_data['date'], 
    deaths_dd_data['newDeaths28DaysByDeathDate'] / GB_pop, 
    color=(150/256, 50/256, 250/256), 
    linestyle='solid', 
    linewidth=1, 
    markersize = 0, 
    alpha= 0.2)

ax3.plot_date(
    time_deaths_dd[0], 
    deaths_dd_7Dma[0], 
    color=(150/256, 50/256, 250/256), 
    linestyle='solid', 
    linewidth=1, 
    markersize = 0, 
    alpha=1,
    label='deaths (date of death)')


ax3.plot_date(
    deaths_rep_data['date'], 
    deaths_rep_data['newDeaths28DaysByPublishDate'] / GB_pop, 
    color='black', 
    linestyle='solid', 
    linewidth=1, 
    markersize = 0, 
    alpha= 0.2)

ax3.plot_date(
    time_deaths_rep[0], 
    deaths_rep_7Dma[0], 
    color='black', 
    linestyle='solid', 
    linewidth=1, 
    markersize = 0, 
    alpha=1,
    label='deaths (report date)')



#plt.xticks(rotation=45)
#plt.xlabel('date', fontsize=12)
#plt.ylabel('number of cases per capita', fontsize=12)

#months = MonthLocator()
#monthsFmt = DateFormatter("%b '%y")
#ax.xaxis.set_major_locator(months)
#ax.xaxis.set_major_formatter(monthsFmt)
plt.grid(True)


plt.legend(loc="upper right")
plt.show()
