#!/usr/bin/env python
import dir_parser
import gpa_parser
import dir_fetcher
import numpy as np
import csv
import pandas as pd
# all sections
# dirs = dir_parser.parse_dir_pdf('../data/1194-Final-DIR-Report.pdf')

# i=2019
# while i >= 2014:

#     # gpa = gpa_parser.parse_gpa_pdf('../data/report-gradedistribution-%s-%sfall.pdf' % (i, i+1))
#     # print('Lines:')
#     # print(len(gpa))
#     # with open('%s-%sfallgpa.txt' % (i, i+1), 'w') as file:
#     #     for line in gpa:
#     #         file.writelines('%s\n' % line)
#     # i=i-1

#     gpa = gpa_parser.parse_gpa_pdf('../data/report-gradedistribution-%s-%sfall.pdf' % (i, i+1))
#     print('Lines:')
#     print(len(gpa))
#     with open('%s-%sfallgpa1.csv' % (i, i+1), 'w') as file:
#         for line in gpa:
#             file.writelines('%s\n' % line)

#     df = pd.DataFrame.from_dict(gpa)
#     print (df)
#     df.to_csv('%s-%sfallgpa2.csv' % (i, i+1))
#     i=i-1
# i=2019
# while i >= 2014:

#     gpa = gpa_parser.parse_gpa_pdf('../data/report-gradedistribution-%s-%sspring.pdf' % (i, i+1))
#     print('Lines:')
#     print(len(gpa))
#     with open('%s-%sspringgpa1.csv' % (i, i+1), 'w') as file:
#         for line in gpa:
#             file.writelines('%s\n' % line)

#     df = pd.DataFrame.from_dict(gpa)
#     print (df)
#     df.to_csv('%s-%sspringgpa2.csv' % (i, i+1))

#     i=i-1

# i=2015


# gpa = gpa_parser.parse_gpa_pdf('../data/report-gradedistribution-%s-%sspring.pdf' % (i, i+1))
# print('Lines:')
# print(len(gpa))
# with open('%s-%sspringgpa1.csv' % (i, i+1), 'w') as file:
#     for line in gpa:
#         file.writelines('%s\n' % line)

# df = pd.DataFrame.from_dict(gpa)
# print (df)
# df.to_csv('%s-%sspringgpa2.csv' % (i, i+1))


# with open('%s-%sspringgpa.csv' % (i, i+1), 'w') as output:
#     writer = csv.writer(output)
#     for key, value in gpa.iteritems():
#         writer.writerow([key, value])
    
# with open('2018-2019springdir.txt', 'w') as file:
#     for line in dirs:
#         file.writelines('%s\n' % line)
# print('hello')

# seems to list:
# * most lecture sections (not AAE 652 - 0 enrolled)
# * independent study sometimes
# 
# just random in general?
# gpas = gpa_parser.parse_gpa_pdf('gpa_1174.pdf')
# i=2019
# while i >= 2014:
#     j=i-2000+101
#     print('../data/%s2_Final_DIR_Report.pdf' % j)
#     dirs = dir_parser.parse_dir_pdf('../data/%s2_Final_DIR_Report.pdf' % j) 
#     print('Lines:')
#     print(len(dirs))
#     with open('DIR%s-%sfall1.csv' % (i, i+1), 'w') as file:
#         for line in dirs:
#             file.writelines('%s\n' % line)

#     # df = pd.DataFrame.from_dict(dir)
#     # print (df)
#     # df.to_csv('DIR%s-%sfall1.csv' % (i, i+1))

#     i=i-1

i=2016

while i >= 2016:
    j=i-2000+101
    print('../data/%s4_Final_DIR_Report.pdf' % j)
    dirs = dir_parser.parse_dir_pdf('../data/%s4_Final_DIR_Report.pdf' % j)
    print('Lines:')
    print(len(dirs))
    with open('DIR%s-%sspring1.csv' % (i, i+1), 'w') as file:
        for line in dirs:
            file.writelines('%s\n' % line)

    # df = pd.DataFrame.from_dict(gpa)
    # print (df)
    # df.to_csv('DIR%s-%sspring1.csv' % (i, i+1))

    i=i-1