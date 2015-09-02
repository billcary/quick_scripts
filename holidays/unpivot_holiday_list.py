# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 2015

@author: billcary

Script Name: unpivot_holiday_list

Purpose:
Take a "pivoted" list of US holidays and corresponding dates and "unpivot" it
to get a row for each holiday and date.  Save resulting data frame as a csv
file for use by other systems/tools.

Approach:
Utilize pandas to read in a pivoted list of holidays, unpivot the list, clean up
inconsistent date formats, then save result in .csv format.

Author: Bill Cary

Copyright 2015 Bill Cary

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

The data file 'Holidays.xls' was released by Don McMunn (2007) and is licensed
under the Creative Commons Attribution 3.0 License, available here:
http://creativecommons.org/licenses/by/3.0/.  The data file is available at the
following location: http://www.ipcdesigns.com/dim_date/Holidays.xls.

History:

Date            Author          Purpose
-----           -------         -----------
08/31/2015      Bill Cary       Initial development/release

"""
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import necessary libraries
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pandas as pd
from dateutil import parser

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Read holiday list into a pandas dataframe
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
holidayTable = pd.read_excel('Holidays.xls')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Drop the "year" column - not needed
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
holidayTable = holidayTable.drop('Year', 1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Unpivot the dataframe
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
stackedHolidays = pd.melt(holidayTable, id_vars=['#'], var_name='holiday', 
                          value_name = 'date')
                          
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Drop the now-meaningless '#' column
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
stackedHolidays = stackedHolidays.drop('#', 1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Clean up inconsistent date formatting in the input file
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
strDates = stackedHolidays['date'].astype(str)
strDates = strDates.tolist()
strDates = [parser.parse(element) for element in strDates]
strDates = [element.strftime("%m/%d/%Y") for element in strDates]
stackedHolidays['newDate'] = strDates
stackedHolidays = stackedHolidays.drop('date', 1)         
stackedHolidays = stackedHolidays.rename(columns={'newDate': 'date'})            

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Write results to .csv file
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
stackedHolidays.to_csv('stackedHolidays.csv')            
            