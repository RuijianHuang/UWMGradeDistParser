# UWM Grade Distribution Parser
Parse UW-Madison Grade Distribution files & Departmental Instructional Report from PDF to Excel
## Usage
### Prerequisites
+ python3+
+ tabula-py
+ openpyxl
+ a PC with fans
### From PDF to .csv files [tabula-py]
+ ```python3 batchTabulaConvertor.py -d (or --dir)``` convert instructional reports to tables listed by semesters in ./dir/
+ ```python3 batchTabulaConvertor.py -g (or --grade)``` convert grade distribution files to tables listed by semesters in ./grade/
### From .csv to *slightly organized* Excels
+ ```python3 dirParser.py <dir/csv/filepath>``` print converted results of one selected dir .csv for testing
+ ```python3 dirParser.py -b (or --batch)``` organize instructional reports into one aggregated excel in ./dir/dirParsed.xlsx
+ ```python3 gradeParser.py <grade/csv/filepath>``` print converted results of one selected grade .csv for testing
+ ```python3 gradeParser.py -b (or --batch)``` organize grade distribution data into one aggregated excel in ./grade/gradeParsed.xlsx
