import sys
import re
import openpyxl
from utils import *

# approximate page bounds for dir
def findPageBounds(p):
    start = None
    end = None
    for i in range(len(p)):
        if 'FACILITY_ID' in p[i] and 'COMB_ENRL' in p[i]: start = i+1
        if 'PAGE NUMBER' in p[i] and 'OF' in p[i]: 
            end = i
            break
    if start is None:
        print("Error: findPageBounds: upper bound not found:")
        for i in p: print(i)
        exit(1)
    if end is None: end = len(p)-1
    if start >  end:
        print("Error: findPageBounds: start={} > end={}".format(start, end))
        for i in p: print(i)
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
            identifications = re.findall(r'[0-9]{10}[ \t]*[A-Z \'\.-]+', l)
            if len(identifications) != 1: continue
            employeeID = re.findall('[0-9]{10}', identifications[0])[0]
            info.extend([employeeID, identifications[0][10:].strip()])

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
    unifyColumns(pages)
    addInfoFromHeader(pages)
    lines = finalTrim(pages)
    
    for l in lines: 
        if len(l) != 7: print(l)
    return lines


cur_file = None
dst_folder = './dir/'
src_folder = './dir/'
empty_course_name = 'empty'
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 dirParser.py <csv file>")
        exit(1)
    
    if sys.argv[1] == '-b' or sys.argv[1] == '--batch':
        wb = openpyxl.Workbook()
        for year in range(2014, 2020+1):
            for term in ['spring', 'fall']:
                if year == 2014 and term == 'spring': continue
                elif year == 2020 and term == 'fall': continue
                
                cur_file = src_folder + str(year) + term + '.csv'
                print("Processing", cur_file)
                #  writeExcel(processCsv(cur_file), str(year)+term)        # FIXME
                
        print('Saving')
        wb.save(dst_folder + 'grade_dist.xlsx')

    else: 
        cur_file = sys.argv[1]
        processCsv(cur_file)
