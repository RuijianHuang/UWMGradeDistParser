#!/usr/bin/env python
from extractor import Extractor
from utils import tabula

REPORT_PAGE = 'https://registrar.wisc.edu/grade-reports/'

COLUMNS = ','.join(map(str, [
  55,80,95,130,150,210,295,360,420,480,550
]))

class DirExtractor(Extractor):
  def __init__(self):
    super(DirExtractor, self).__init__(REPORT_PAGE)

  def get_columns(self, context):
    return COLUMNS

  def is_data_set(self, url):
    upper = url.upper()
    if 'MEMO' in upper or 'CALL' in upper:
      return False
    return 'DIR' in upper

  def download_name(self, url):
    # get the file name, it contains the term code
    file = url.split("/")[-1]

    # extract the term code, the only digits in the file name
    sis_term_code = int(filter(str.isdigit, str(file)))

    return 'dir_%s.pdf' % sis_term_code

  def extract_data(self, context, contents):
    # TODO:
    # 1124 is literally the only term which has a PDF which
    # differs from the others. Different fonts, colors, and
    # table format... *sigh*
    if '1124' in context['file_path']:
      return []

    dept_num = None
    start_time = None
    end_time = None
    sections = []

    for row in contents.split("\r\n"):
      cols = row.split("\t")
      joined = ''.join(cols)

      if 'SUBJECT' in joined:
        dept_num = int(joined[-4:-1])

      if 'TERM:' in joined:
        term = int(joined.split(':')[-1])

      # valid rows have 12 columns
      if len(cols) != 12:
        continue

      # valid rows should have a course number
      # if it does not parse, we skip this row
      try:
        int(cols[1])
      except ValueError:
        continue
      
      # unknown values: cols[0], cols[4]

      course_num = int(cols[1])
      section_type = cols[2]
      section_num = cols[3]
      time = cols[5]
      days = cols[6]
      facility = cols[7]
      combined_enrollment = cols[8]
      total_enrollment = cols[9]
      instructor_id = cols[10]
      instructor_name = cols[11]

      # if combined enrollment is not defined, that means
      # it is not cross listed
      if combined_enrollment == '':
        combined_enrollment = None

      if time == '-':
        start_time = None
        end_time = None
      elif ' - ' in time:
        split_time = time.split(' - ')
        start_time = split_time[0]
        end_time = split_time[1]

      if len(days) == 0:
        days_array = []
      else:
        days_array = days.split(' ')

      if facility in ('ONLINE', 'OFF CAMPUS'):
        building = facility
        room = None
      elif facility == '':
        building = None
        room = None
      elif ' ' in facility:
        parts = facility.split(' ')
        building = parts[0]
        room = parts[1]
      elif len(facility) > 8:
        building = facility[0:5]
        room = facility[5:]
      else:
        print('Unable to parse facility: "%s"' % facility)
        building = None
        room = None

      sections.append({
        "dept_num": dept_num,
        "course_num": course_num,
        "section_num": section_num,
        "start_time": start_time,
        "end_time": end_time,
        "days": days_array,
        "building": building,
        "room": room,
        "combined_enrollment": combined_enrollment,
        "total_enrollment": total_enrollment,
        "instructor_id": instructor_id,
        "instructor_name": instructor_name
      })
    return sections