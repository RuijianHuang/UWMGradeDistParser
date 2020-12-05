
SEASON_IDS = {
  4: 'Spring',
  6: 'Summer',
  2: 'Fall'
}

def term_code_to_english(term_code):
  """Convert SIS term code into English.
  
  Convert a SIS term code into a English tuple containing
  a season string and the calendar year.

  Examples: ('Spring', 2017) or ('Fall', '2009')

  See http://www.bussvc.wisc.edu/bursar/termcode.html
  
  Arguments:
    term_code {int} -- the SIS term code

  Returns:
    Tuple containing two elements: a season string and the calendar year.
  """

  # get the season
  season_id = term_code % 10

  # chop off the season
  term_year = term_code // 10

  # term codes start at: 101
  offset = term_year - 101

  # account for fall season being 1 greater than other seasons
  if season_id == 2:
    offset -= 1

  # term codes start at calendar year: 2001
  calendar_year = 2001 + offset
  season = term_code_season_to_english(season_id)

  return (
    season,
    calendar_year
  )

def term_code_season_to_english(season_id):
  """Convert season id into English string.
  
  Arguments:
    season_id {int} -- The season id, either 2, 4, or 6.

  Returns:
    The appropriate season name in English.
  """
  return SEASON_IDS[season_id]