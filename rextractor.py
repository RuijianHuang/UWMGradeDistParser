import sys

def getCsvByLines(fn):
    try: 
        f = open(sys.argv[1])
        lines = [l.strip() for l in f.readlines()]
        f.close()
        return lines
    except OSError:
        print("Error: cannot open file:", fn)
        exit(1)

def remove

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
        
def parseCommaSplit(pages):
    for i in range(len(pages)):
        for j in range(len(pages[i])):
            pages[i][j] = pages[i][j].split(',')
    return pages

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 ??extractor.py <csv file>")
        exit(1)
        
    lines = getCsvByLines(sys.argv[1])
    pages = paginate(lines)
    pages = parseCommaSplit(pages)
    
    # FIXME
    #  print(pages[0][0])
    #  for l in pages[0]:
    #      print(len(l), l)
    
    for p in pages:
        for l in p:
            print(len(l), l[0])
