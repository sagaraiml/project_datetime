# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 19:05:04 2019

@author: sagar_paithankar
"""

#from datetime import *
#import calendar
# =============================================================================
# def add_months(date):
#     datetime
#     month = date.month
#     year = date.year + month // 12
#     month = month % 12 + 1
#     day = min(date.day, calendar.monthrange(year,month)[1])
#     return datetime.date(year, month, day)
# 
# date = datetime.strptime('2015-01-01', '%Y-%m-%d')
# 
# i = add_months(date)
# =============================================================================


from datetime import datetime
from dateutil.relativedelta import relativedelta

date = datetime.strptime('2015-01-31', '%Y-%m-%d')

date_after_month = date + relativedelta(months=1)
print('Input: ',date.strftime('%Y-%m-%d'))
print('After Month:', date_after_month.strftime('%Y-%m-%d'))
