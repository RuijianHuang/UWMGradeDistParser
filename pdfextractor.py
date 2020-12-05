import sys
import re

def removeIrrelevantLines(lines):
    removeIndex = []
    irrelevantKeys = ['Please note', 'S/SD and U/UD', 'Dept. Total', 'Section Total']       # ***?
    for i in range(len(lines)):
        for k in irrelevantKeys: 
            if k in lines[i]:
                removeIndex.append(i)
                break
    for index in reversed(removeIndex):
        lines.pop(index)

def getCsvByLines(fn):
    try: 
        f = open(sys.argv[1])
        lines = [l.strip() for l in f.readlines()]
        f.close()
        removeIrrelevantLines(lines)
        return lines
    except OSError:
        print("Error: cannot open file:", fn)
        exit(1)

# split raw pdf to pages by pageHeader
def paginate(lines):
    pageHeader = 'Percentage Distribution of Grades'
    pageNum = []
    pages = []
    for i in range(len(lines)):
        if pageHeader in lines[i]:
            pageNum.append(i)
    
    for i in range(len(pageNum)):
        if i < len(pageNum)-1:
            pages.append(lines[pageNum[i]:pageNum[i+1]])
        else:
            pages.append(lines[pageNum[i]:len(lines)-1])
    return pages
        
# find bounds of grade distribution data based on keywords
def findPageBounds(p):
    start = None
    end = None
    for i in range(len(p)):
        if 'Grades' in p[i] and 'GPA' in p[i]: start = i+1
        if 'Summary by Level' in p[i] or ('Page' in p[i] and 'of' in p[i]): 
            end = i
            break
        if 'Summary by College/School' in p[i] or 'Grand Total' in p[i]:        # discard Summary page
            return (1, 0)

    if start is None:
        print("Error: findPageBounds: upper bound not found:")
        for i in p: print(i)
        exit(1)

    if end is None: end = len(p)-1
    if end < start:
        print("Error: findPageBounds: start={} > end={}\n".format(start, end))
        for i in p: print(i)
        exit(1)
    return (start, end)

def unifyColumns(pages):
    for i in range(len(pages)-2):                       # NOTE: last page is a summary of the term, formatted differently
        start, end = findPageBounds(pages[i])           # find grade_dist data in a page
        removeIndex = []       # deal with special case biotech&phmacogenomics in 2014 fall and 2017 fall
        for j in range(start, end):
            l = pages[i][j].split()
            
            replacementIndex = {}   # replace [.]+ with ( null )+, and extend elements to one list of strings
            additionIndex = {}      # replace [.]+ attched to float by inserting
            for k in range(len(l)):
                element = l[k].strip()
                if "."*len(element) == element:             # check if one element is full of . and note them down
                    replacementIndex[k] = len(element)
                if re.match(r'\.+[0-9]+\.[0-9]+', element):  # check if . attached to floats
                    digits = re.findall(r'[^\.]', element)
                    additionIndex[k] = element.index(digits[0])
                    l[k] = element[additionIndex[k]:]

            # replace . with " null " for now
            for k in reversed(replacementIndex.keys()):
                l = l[:k] + (" null "*replacementIndex[k]).split() + l[k+1:]
            for k in reversed(additionIndex.keys()):
                l = l[:k] + (" null "*additionIndex[k]).split() + l[k:]

            # find course_name based on patterns in stop_signs
            l_joined = " ".join(l)
            stop_signs = ['(Course Total)+',                        # Order matters
                            '^[0-9]{3} [0-9]{3} [0-9]+ ',           # no course_name scenarios
                            '^[0-9]{2} [0-9]{3} [0-9]+ ',
                            '^[0-9]{1} [0-9]{3} [0-9]+ ',
                            '^[0-9]{3} 0{2}[ABCD]{1} [0-9]+ ',
                            '[^0-9]{1}[0-9]{3} [0-9]{3} [0-9]+ ',   # with course_name scenarios [avoid course_name=something:1839-1989]
                            '[^0-9]{1}[0-9]{2} [0-9]{3} [0-9]+ ',
                            '[^0-9]{1}[0-9]{1} [0-9]{3} [0-9]+ ',
                            '[^0-9]{1}[0-9]{3} 0{2}[ABC]{1} [0-9]+ ']
            findings = []
            sign_i = None        # to discern w/ or w/o course_name
            for sign_i in range(len(stop_signs)):
                if findings != []: break
                findings = re.findall(stop_signs[sign_i], l_joined)
            if findings == []:
                if l_joined == 'Biotech&Phmacogenomics':    # Special case: 2-line course_name
                    pages[i][j-1][0] += (" "+l_joined)
                    removeIndex.append(j)
                    continue
                else:
                    print("Error: cannot find identify course_name by existing "\
                            "stop_signs in {} page {} line \n{}".format(sys.argv[1], i, l_joined))
                    exit(1)

            course_name_tail = l_joined.index(findings[0])
            if sign_i > 4: course_name_tail += 1
            course_name = l_joined[:course_name_tail].strip()

            l_joined = l_joined[len(course_name):].strip()
            l = l_joined.split()
            l.insert(0, course_name if course_name !='' else empty_course_name)
            
            # special cases
            if l[0] == 'Russ Honor Tutorial-Slav' and (l[1]=='101' or l[1]=='102'):
                l[0] += l[1]
                l.pop(1)
            
            # l[4] should be float (GPA) after course_name extraction
            if re.match(r'[0-9]+\.{1}[0-9]+',l[4]) is None:
                l.insert(4, " null ")

            # DEBUG
            if len(l) != 21 and "***" not in "".join(l):                # FIXME: get rid of *** lines
                print("Warning: #col mismatch at:\n", sys.argv[1], len(l), "p", i, l)

            pages[i][j] = l
        for index in reversed(removeIndex): pages[i].pop(index)

# find course_name by looking downward
def findCourseName(pages, pageNum, curLine, endLine):
    for k in range(curLine, endLine):
        if pages[pageNum][k][1] == 'Course' and pages[pageNum][k][2] == 'Total':
            return pages[pageNum][k][0]
    return empty_course_name

# find course_name for those with only course_code/section_code
def fillEmptyCourseName(pages):
    for i in range(len(pages)-2):
        start, end = findPageBounds(pages[i])           # find grade_dist data in a page TODO: optimization can wait
        startN, endN = findPageBounds(pages[i+1])       # find grade_dist data in a page TODO: optimization can wait
        for j in range(start, end):                     # find at this page and the next
            if pages[i][j][0] == empty_course_name:
                pages[i][j][0] = findCourseName(pages, i, j, end)
            if pages[i][j][0] == empty_course_name:
                pages[i][j][0] = findCourseName(pages, i+1, startN, endN)
            if pages[i][j][0] == empty_course_name:
                print("Error: fillEmptyCourseName: cannot find course_name for")
                print(pages[i][j][0], 'in page', i, ":")
                for i, l in enumerate(pages[i]): print(i, l)
                print("\n\nand page", i+1, ':')
                for i, l in enumerate(pages[i+1]): print(i, l)
                exit(1)

# remove lines containing 'Course Total' or '***' (i.e.: no GPA)
def removeMoreIrrelevantLines(pages):
    for i in range(len(pages)):
        removeIndex = []
        for j in range(len(pages[i])):
            l = " ".join(pages[i][j])
            if 'Course Total' in l or '***' in l: removeIndex.append(j)
        for index in reversed(removeIndex): pages[i].pop(index)

# add dept_code, dept_abbr, dept_name, school to each line, s.t. headers can be removed
def addInfoFromHeader(pages):
    for i in range(len(pages)):
        p = pages[i]
        start, end = findPageBounds(p)
        if start > end: continue            # discarding irrelevant pages

        sub = p[start-1][:p[start-1].index('Grades')].strip()
        dept_code = int(sub[:3].strip())
        dept_abbr = sub[3:].strip()
        dept_name = p[start-2][:p[start-2].index('Section')].strip()
        school = p[start-3].strip()
        
        for j in range(start, end):
            pages[i][j].extend([school, dept_code, dept_abbr, dept_name])

def finalTrim(pages):
    lines = []
    for i in range(len(pages)):
        start, end = findPageBounds(pages[i])
        lines.extend(pages[i][start:end])
    return lines

empty_course_name = 'empty'
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 ??extractor.py <csv file>")
        exit(1)
        
    lines = getCsvByLines(sys.argv[1])
    pages = paginate(lines)
    unifyColumns(pages)
    fillEmptyCourseName(pages)
    removeMoreIrrelevantLines(pages)
    addInfoFromHeader(pages)
    lines = finalTrim(pages)
    
    # DEBUG print
    #  for p in pages:
    #      start, end = findPageBounds(p)
    #      for j in range(start, end):
    #          print(p[j])
    #  for l in lines:
    #      if len(l) != 25:
    #          print(sys.argv[1], len(l), l)
