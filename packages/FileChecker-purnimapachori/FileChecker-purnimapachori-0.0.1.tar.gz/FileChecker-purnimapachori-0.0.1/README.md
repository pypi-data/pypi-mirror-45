# file_investigation
To identify files to cleanup a directory as per user's input

Input: a directory to be recursively searched
Output: a csv report of files for deletion (category, full path to file).

This will include: 
identifying duplicate files, 
files which have not been accessed in over X days, 
files which are over Y bytes in size,
directories containing large numbers of files, 
identifying uncompressed files.

usage: FileChecker.py [-h] [--dirname DIRNAME] [--days DAYS] [--size SIZE]
                      [--filelimit FILELIMIT]

optional arguments:
  -h, --help            show this help message and exit
  --dirname DIRNAME     Please enter directory name
  --days DAYS           Number of days last accessed
  --size SIZE           File size in kilobytes
  --filelimit FILELIMIT
                        specify number of files above which a directory is
                        bigDir
                        
Example: python3 FileChecker.py --dirname data --days 0 --size 450 --filelimit 4
