#  import subprocess
import sys
from tabula import convert_into

def parseGrade():
    folder = "./grade/"
    for y in range(2014, 2019+1):
        for s in ['spring', 'fall']:
            fn_in = folder+"report-gradedistribution-"+str(y)+"-"+str(y+1)+s+".pdf"
            fn_out = ""
            if s == 'spring': fn_out = folder+str(y+1)+s+".csv"
            else: fn_out = folder+str(y)+s+".csv"
            convert_into(fn_in, fn_out, output_format="tsv", pages='all', stream=True, guess=False)

def parseDir():
    folder = "./dir/"
    year_dict = {1150: [2014, 2015],
                 1160: [2015, 2016],
                 1170: [2016, 2017],
                 1180: [2017, 2018],
                 1190: [2018, 2019],
                 1200: [2019, 2020]}
    term_offsets = {2:'fall', 4:'spring'}
    for y in year_dict.keys():
        for s in term_offsets.keys():
            term = y + s
            fn_in = folder + str(term) + '_Final_Dir_Report.pdf'
            fn_out = ""
            if term_offsets[s] == 'spring': 
                fn_out = folder + str(year_dict[y][1]) + str(term_offsets[s]) + '.csv'
            else:
                fn_out = folder + str(year_dict[y][0]) + str(term_offsets[s]) + '.csv'
            convert_into(fn_in, fn_out, output_format='tsv', pages='all', stream=True, guess=False)
    

available_options = ['-d', 'dir', '-g', 'grade']
if len(sys.argv) != 2 or sys.argv[1].strip() not in available_options:
    print("Usage: python3 batchTabulaConvertor.py <option: -d/--dir or -g/--grade>")
    exit(1)

option = sys.argv[1]
if option in available_options[:2]: parseDir()
else: parseGrade()


# NOTE: Deprecated code that uses tabular.jar through subprocess
#  tabula = "tabula.jar"
#  for y in range(2014, 2019+1):
#      for semester in ['spring', 'fall']:
#          fn = folder+"report-gradedistribution-"+str(y)+"-"+str(y+1)+semester+".pdf"
#          print("Converting", fn, "...")
#          proc = subprocess.run(['java', '-jar', tabula, fn, '-pages=all'],
#                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#          out = proc.stdout.decode()
#          err = proc.stderr.decode()
#          if err != "":
#              print("stderr: \n", err)
#              #  exit(1)              # FIXME

#          toWrite = ""
#          if semester == 'spring': toWrite = folder+str(y+1)+semester+".csv"
#          else: toWrite = folder+str(y)+semester+".csv"

#          f = open(toWrite, 'w')
#          f.write(out)
#          f.close()


