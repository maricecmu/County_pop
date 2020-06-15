import pandas as pd
import datetime as dt

#current and previous weeks
from datetime import date, timedelta
def weeks(year):
   current = date(year, 2, 7)
   while current.year == year:
      yield current
      current += timedelta(days = 7)    

for current in weeks(2020):
   print(current)
   previous = current - timedelta(days = 7)
   print(previous)
    
#import csv files from github
   state_pop= 'https://raw.githubusercontent.com/maricecmu/State_pop/master/State_Population_Data.csv'
   base_url = 'https://raw.githubusercontent.com/stccenter/COVID-19-Data/master/US/State_level_daily/US_State_'+'2020-01-31'+'.csv'
   case_death_current = base_url.replace('2020-01-31', str(current))
   case_death_previous = base_url.replace('2020-01-31', str(previous))

#data into dataframes, selecting columns, sort and new index, combining frames
   sf = pd.read_csv(state_pop, usecols=[0,2])
   sf = sf.rename(columns={'population':'population_per_100000_people'})
   cdcf = pd.read_csv(case_death_current, usecols=[0,1,2,3,4])
   cdcf = cdcf.rename(columns={'confirmed':'current_total_cases','death':'current_total_deaths', 'recovered':'current_total_recovered'})
   cdcf = cdcf.sort_values('State')
   cdcf = cdcf.reset_index(drop=True)
   cdpf = pd.read_csv(case_death_previous, usecols=[0,2,3])
   cdpf = cdpf.rename(columns={'confirmed':'previous_total_cases','death':'previous_total_deaths'})
   cdpf = cdpf.sort_values('State')
   cdpf = cdpf.reset_index(drop=True)
   combined = pd.concat((cdcf[['State','hasc','current_total_cases','current_total_deaths','current_total_recovered']], cdpf[['previous_total_cases','previous_total_deaths']], sf[['population_per_100000_people']]), axis=1)

#adding in inc, prev, death rate formulas
   combined['new_cases'] = cdcf.current_total_cases - cdpf.previous_total_cases
   combined['new_deaths'] = cdcf.current_total_deaths - cdpf.previous_total_deaths
   combined['incidence'] = (combined.new_cases)/(sf.population_per_100000_people)
   combined['prevalence'] = (cdcf.current_total_cases)/(sf.population_per_100000_people)
   combined['death_rate_per_pop'] = (combined.new_deaths)/(sf.population_per_100000_people)
#getting rid of values with 0 in denominator
   combined.loc[combined.new_deaths/cdcf.current_total_cases > 0]
   combined['death_rate_per_case'] = 0
   combined.loc[combined.new_deaths/cdcf.current_total_cases > 0, 'death_rate_per_case'] = combined.new_deaths/cdcf.current_total_cases

#resorting and printing
   pd.set_option("display.max_rows", None, "display.max_columns", None)
   combined = combined.sort_values('current_total_cases', ascending=False)
   print(combined)

   