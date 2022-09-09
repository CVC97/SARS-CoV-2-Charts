import pandas as pd
import matplotlib.pyplot as plt


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


#data
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


#######

fig, ax = plt.subplots()
fig.subplots_adjust(right=0.75)
#fig = plt.figure(figsize=(12, 6))

twin1 = ax.twinx()
twin2 = ax.twinx()

# Offset the right spine of twin2.  The ticks and label have already been
# placed on the right by twinx above.
twin2.spines.right.set_position(("axes", 1.075))


#cases
p1, = ax.plot_date(
    cases_spec_data['date'], 
    cases_spec_data['newCasesBySpecimenDate'] / GB_pop, 
    color=(50/255, 150/255, 250/255), 
    linestyle='solid', 
    linewidth=1, 
    markersize = 0, 
    alpha= 0.2
    )

p1, = ax.plot_date(
    time_cases_spec[0], 
    cases_spec_7Dma[0], 
    color=(50/255, 150/255, 250/255), 
    linestyle='solid', 
    linewidth=1, 
    markersize = 0, 
    alpha=1,
    label='cases (specimen date)'
    )

p1, = ax.plot_date(
    cases_rep_data['date'], 
    cases_rep_data['newCasesByPublishDate'] / GB_pop, 
    color='blue', 
    linestyle='solid', 
    linewidth=1, 
    markersize = 0, 
    alpha= 0.2)

p1, = ax.plot_date(
    time_cases_rep[0], 
    cases_rep_7Dma[0], 
    color='blue', 
    linestyle='solid', 
    linewidth=1, 
    markersize = 0, 
    alpha=1,
    label='cases (report date)')

#hosps
p2, = twin1.plot_date(
    time_hosp_adm[0], 
    hosp_adm_data['newAdmissions'] / GB_pop, 
    color='red', 
    linestyle='solid', 
    linewidth=1, 
    markersize = 0, 
    alpha= 0.2)

p2, = twin1.plot_date(
    time_hosp_adm[0], 
    hosp_adm_7Dma[0], 
    color='red', 
    linestyle='solid', 
    linewidth=1, 
    markersize = 0, 
    alpha=1,
    label='hospital admissions')

#deaths
p3, = twin2.plot_date(
    deaths_dd_data['date'], 
    deaths_dd_data['newDeaths28DaysByDeathDate'] / GB_pop, 
    color=(150/256, 50/256, 250/256), 
    linestyle='solid', 
    linewidth=1, 
    markersize = 0, 
    alpha= 0.2)

p3, = twin2.plot_date(
    time_deaths_dd[0], 
    deaths_dd_7Dma[0], 
    color=(150/256, 50/256, 250/256), 
    linestyle='solid', 
    linewidth=1, 
    markersize = 0, 
    alpha=1,
    label='deaths (date of death)')


p3, = twin2.plot_date(
    deaths_rep_data['date'], 
    deaths_rep_data['newDeaths28DaysByPublishDate'] / GB_pop, 
    color='black', 
    linestyle='solid', 
    linewidth=1, 
    markersize = 0, 
    alpha= 0.2)

p3, = twin2.plot_date(
    time_deaths_rep[0], 
    deaths_rep_7Dma[0], 
    color='black', 
    linestyle='solid', 
    linewidth=1, 
    markersize = 0, 
    alpha=1,
    label='deaths (report date)')



#ax.set_xlabel("Distance")
ax.set_ylabel('number of cases per capita')
twin1.set_ylabel('number of hospital admissions per capita')
twin2.set_ylabel('number of deaths (within 28 days of positive test) per capita')


#LHS y-axis
case_start=-0.05 * max(cases_spec_data['newCasesBySpecimenDate']) / GB_pop 
case_end=1.05 * max(cases_spec_data['newCasesBySpecimenDate']) / GB_pop

#RHS y-axis hosps
rfactor = max(cases_spec_data['newCasesBySpecimenDate'])* max(data_to_7D(hosp_adm_data['newAdmissions'])) / max(data_to_7D(cases_spec_data['newCasesBySpecimenDate']))

hosp_start=-0.05 * rfactor / GB_pop
hosp_end=1.05 * rfactor / GB_pop

#RHS y-axis deaths
rfactor2 = max(cases_spec_data['newCasesBySpecimenDate'])* max(data_to_7D(deaths_dd_data['newDeaths28DaysByDeathDate'])) / max(data_to_7D(cases_spec_data['newCasesBySpecimenDate']))

death_start=-0.05 * rfactor2 / GB_pop 
death_end=1.05 * rfactor2 / GB_pop


#ax limits
ax.set_ylim(case_start, case_end)
twin1.set_ylim(hosp_start, hosp_end)
twin2.set_ylim(death_start, death_end)

#timestamp
diggawhat = cases_rep_data['date'].loc[0]
print(diggawhat)


ax.grid(True)
fig.set_size_inches(16, 8)
fig.legend(loc="upper right")
plt.title(f'SARS-CoV-2: United Kingdom ({diggawhat})',  loc='left', weight='bold')
plt.show()