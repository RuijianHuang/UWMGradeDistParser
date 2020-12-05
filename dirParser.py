import sys
import re
import openpyxl
from utils import *

# approximate page bounds for dir
def findPageBounds(p):
    start = None
    end = None
    for i in range(len(p)):
        if 'EMPLID' in p[i] and 'instructor role' in p[i].lower():
            start = i+1
        elif 'PAGE NUMBER' in p[i] and 'OF' in p[i]: 
            end = i
            break
    if start is None:
        print("Error: findPageBounds: upper bound not found:")
        for i in p: print(i)
        exit(1)
    if end is None: end = len(p)-1
    if start-1 >  end:
        print("Error: findPageBounds: start={} > end={}".format(start, end))
        for i in range(len(p)): print(i, p[i])
        exit(1)
    return (start, end)

# find 5 pieces of info for each section
def unifyColumns(pages):
    for i in range(len(pages)):
        start, end = findPageBounds(pages[i])
        for j in range(start, end):
            l = pages[i][j].strip()

            # find course_code course_mode section_code
            codes = re.findall(r'[0-9]{1,3}[ \t]+[A-Z]{3}[ \t]+[0-9]{2}[0-9ABCD]{1} ', l)
            if len(codes) != 1:
                #  print("Warning: no codes found, possible header:", len(codes), codes, l)
                continue
            info = codes[0].split()
            if len(info) != 3:
                print('Error: cannot split course_code, course_mode, section_code in ', codes)
                exit(1)

            # find employeeID and name
            identifications = re.findall(r'[0-9]{10}', l)
            if len(identifications) != 1: continue
            employeeID = identifications[0].strip()
            name = l[l.index(identifications[0])+len(identifications[0]):].strip()
            if '/' in name: name = name[name.index('/')+1:]
            info.extend([employeeID, name]) 

            info = [piece.strip() for piece in info]
            pages[i][j] = info

def addInfoFromHeader(pages):
    scode = None
    for i in range(len(pages)):
        start, end = findPageBounds(pages[i])
        subject = "SUBJECT:"
        for j in range(end):
            l = pages[i][j]
            if isinstance(l, str) and subject in l:
                subject = l[l.rfind(subject)+len(subject)+1:]
                scode = re.findall(r'\([0-9]{0,3}\)',l)[0]
                subject = subject[:subject.index(scode)].strip()
                scode = int(scode[scode.index('(')+1:scode.index(')')])
                subject = [subject, scode]
                break

        for j in range(start, end):
            if isinstance(pages[i][j], str): continue
            pages[i][j].extend(subject)

def finalTrim(pages):
    lines = []
    for p in pages:
        start, end = findPageBounds(p)
        for j in range(start, end):
            if isinstance(p[j], list): lines.append(p[j])
    return lines

def processCsv(fn):
    lines = getCsvByLines(fn)
    pages = paginate(lines, 'DEPARTMENT INSTRUCTIONAL REPORT-FINAL')
    if pages == []: pages = paginate(lines, 'SUBJECT:')
    unifyColumns(pages)
    addInfoFromHeader(pages)
    lines = finalTrim(pages)
    for l in lines: 
        if len(l) != 7: print(l)
    return lines

#  def writeExcel(lines, sname):
#      wb.create_sheet(title=sname)
#      st = wb[sname]
#      for r, l in enumerate(lines):
#          for i in range(len(l)):
#              st[getLetter(i+1)+str(r+1)] = l[i]

cur_file = None
dst_folder = './dir/'
src_folder = './dir/'
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 dirParser.py <csv file>")
        exit(1)
    
    if sys.argv[1] == '-b' or sys.argv[1] == '--batch':
        #  wb = openpyxl.Workbook()
        for year in range(2014, 2020+1):
            for term in ['spring', 'fall']:
                if year == 2014 and term == 'spring': continue
                elif year == 2020 and term == 'fall': continue
                
                cur_file = src_folder + str(year) + term + '.csv'
                print("Processing", cur_file)
                processCsv(cur_file)
                #  writeExcel(processCsv(cur_file), str(year)+term)        # FIXME
                
        #  print('Saving')
        #  wb.save(dst_folder + 'dirParsed.xlsx')
    else: 
        cur_file = sys.argv[1]
        processCsv(cur_file)
