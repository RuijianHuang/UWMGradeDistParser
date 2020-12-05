import subprocess
from tabula import convert_into

folder = "./grade/"
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

for y in range(2014, 2019+1):
    for semester in ['spring', 'fall']:
        fn_in = folder+"report-gradedistribution-"+str(y)+"-"+str(y+1)+semester+".pdf"
        fn_out = ""
        if semester == 'spring': fn_out = folder+str(y+1)+semester+".csv"
        else: fn_out = folder+str(y)+semester+".csv"
        convert_into(fn_in, fn_out, output_format="tsv", pages='all', stream=True, guess=False)
