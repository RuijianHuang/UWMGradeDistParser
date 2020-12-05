def removeIrrelevantLines(lines):
    removeIndex = []
    irrelevantKeys = ['Please note', 'S/SD and U/UD', 'Dept. Total', 'Section Total']
    for i in range(len(lines)):
        for k in irrelevantKeys: 
            if k in lines[i]:
                removeIndex.append(i)
                break
    for index in reversed(removeIndex):
        lines.pop(index)

def getCsvByLines(fn):
    try: 
        f = open(fn)
        lines = [l.strip() for l in f.readlines()]
        f.close()
        removeIrrelevantLines(lines)
        return lines
    except OSError:
        print("Error: cannot open file:", fn)
        exit(1)

# split raw pdf to pages by pageHeader
def paginate(lines, pageHeader):
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
        
def getLetter(n):
    return chr(ord('@')+n)

