#!/usr/bin/env python
import subprocess
import sys
from extractor import Extractor

COLUMNS = ','.join(map(str, [
  200,215,235,280,300,330,360,385,410,435,
  460,480,510,540,560,580,610,630,660,690
]))

REPORT_PAGE = 'https://registrar.wisc.edu/grade-reports/'

class GpaExtractor(Extractor):
  def __init__(self):
    super(GpaExtractor, self).__init__(REPORT_PAGE)

  def get_columns(self, context):
    return COLUMNS

  def is_data_set(self, url):
    return 'report-gradedistribution' in url

  def download_name(self, url):
    # get the file name, it contains the term code
    file = url.split("/")[-1]

    return file

  def extract_data(self, context, contents):
    sections = []

    school = None
    dept_name = None
    dept_num = None
    last_was_dept_name = False

    # set of all school names
    schools = set()

    # department id -> name
    departments = {}

    for row in contents.split("\r\n"):
      cols = row.split("\t")
      joined = ''.join(cols)

      if len(cols) != 21:
        continue

      course_name = None

      if len(cols[0]) > 2 or 'CourseTotal' in joined:
        course_name = cols[0]

      # schools are 3 chars
      if len(joined) == 3:
        school = joined
        schools.add(joined)
        continue

      # departments
      if 'Section"#"' in joined:
        dept_name = cols[0]
        last_was_dept_name = True
        continue
      elif last_was_dept_name:
        # extract the deptartment number
        dept_info = cols[0].split(" ")
        # dept_id is usually an int, however
        # Study Abroad for example is "SAB"
        dept_id = dept_info[0]
        departments[dept_num] = dept_name
        last_was_dept_name = False
        continue

      # valid rows should have a course number
      # if it does not parse, we skip this row
      try:
        int(cols[1])
      except ValueError:
        continue

      course_num = cols[1] 
      section_num = cols[2]
      gpa_count = int(cols[3])
      gpa_avg = None
      try:
        gpa_avg = float(cols[4])
      except ValueError:
        gpa_avg = None

      distribution = []
      for i in range(0, 15):
        percent_str = cols[i + 5]
        try:
          percent = float(percent_str)
          distribution.append(percent)
        except ValueError:
          distribution.append(None)
          if len(percent_str) > 0 and percent_str != '.':
            print("Unable to parse course %s, encountered percentage: %s" % (course_num, percent_str))
            print("Poorly formatted PDF? Fix precision of column dividers?")
            continue

      sections.append({
        "dept_num": dept_num,
        "course_num": course_num,
        "section_num": section_num,
        "gpa_count": gpa_count,
        "gpa_avg": gpa_avg,
        "distribution": distribution
      })

    return (schools, departments, sections)

GpaExtractor().execute()