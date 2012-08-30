GAE-webdiff
============

Google App Engine | small experimental app to display the diff between two pasted files or two gists, also provides a download of the resulting .diff. Currently the App is live at http://sharpnoises.appspot.com/webdiff/  

- allows you to paste two files
- compare will display the diff
- once the diff is performed a download button will appear
- you can download and set the filename to download as
- in addition you can compare two gists by feeding the app their gist ids.

#### doing a gist compare, example usage  

- `/webdiff/gist_id1-gist_id2`, for example `/webdiff/3482451-3487958`, will download the gists into the respective text areas and allow you to compare and download the diff. (no progress indicator connected yet, to show you it is downloading, usually this happens quite fast but depends on GAE load). The regex is `GIST_ID_RE = '(\d{3,}-\d{3,})'`  

- Some gists contain several files, in this case you can `/webdiff/3527642>file_00_file_01.py&3527642>file_0001_file_02.py`. The regex will match `r'(\d{3,}>.*?&\d{3,}>.*?$)'` this might be temporary untill a nicer solution comes up. Github will add the prefix `file` to a the permalink if you are copying the link directly from the gist browser.







