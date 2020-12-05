import urllib
import subprocess

TABULA_URL = "https://github.com/tabulapdf/tabula-java/releases/download/v1.0.1/tabula-1.0.1-jar-with-dependencies.jar"
TABULA_JAR = "tabula.jar"

def download_tabula():
  urllib.request.urlretrieve(TABULA_URL, TABULA_JAR)

def execute(pdf, columns, pages='all'):
  test_process = subprocess.Popen([
    'java',
    '-jar',
    TABULA_JAR
  ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

  test_out, test_err = test_process.communicate()

  if 'Error: Need exactly one filename' not in str(test_err):
    print('Tabula missing, downloading...')
    download_tabula()
    print('Tabula downloaded')

  print("-----------PDF filename:", pdf)       # FIXME
  process = subprocess.Popen([
    'java', 
    '-jar', 
    TABULA_JAR,
    pdf,
    '--columns=' + columns,
    '--format=TSV',
    '--pages=%s' % pages
  ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

  out, err = process.communicate()

  if len(err) > 0:
    print('Error executing tabula: "%s"' % err.rstrip())

  return out
