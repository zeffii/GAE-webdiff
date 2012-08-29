"""
Milestones
[x] display a diff of two files
[x] color code the diff
[x] populate output area after 'compare button' is pressed
[x] accept pasted data
[x] track download button event
[x] make diff downloadable
[x] autofill from gist combo ( webdiff/gist_id1-gist_id2 )
[ ] accept dragged data
[ ] permalink, for sharing
[ ] implement additional origins beside gists
[ ] deal with multifile gists somehow ( must gather examples )
"""

import re

import webapp2
import difflib

import json
import urllib
from utils import PageHandler
from utils import logger


def get_raw_url_from_gist_id(gist_id):
    gist_id = str(gist_id)
    url = 'https://api.github.com/gists/' + gist_id
    
    found_json = urllib.urlopen(url).read()
    wfile = json.JSONDecoder()
    wjson = wfile.decode(found_json)

    # 'files' may contain several - this will mess up gist name.
    files_flag = 'files'
    file_names = wjson[files_flag].keys()
    file_name = file_names[0]
    return wjson[files_flag][file_name]['raw_url']

def get_file(gist_id):
    url = get_raw_url_from_gist_id(gist_id)
    conn = urllib.urlopen(url)
    return conn.read()

# -----------------------

def make_diffstring(content_ab, separator):
    raw_text_input_a, raw_text_input_b = content_ab
    text_input_a = raw_text_input_a.split(separator)
    text_input_b = raw_text_input_b.split(separator)
    
    # http://docs.python.org/library/difflib.html     
    diff_object = difflib.HtmlDiff(wrapcolumn=87)
    diff_string = diff_object.make_table( text_input_a, text_input_b)

    if not type(diff_string) == unicode:
        logger('make_table failed')
        return

    return ''.join(diff_string)

def make_unified_diff(content_ab, separator):
    a, b = content_ab
    diff_generator = difflib.unified_diff(  a=a.split(separator), 
                                            b=b.split(separator))
    return '\n'.join(diff_generator)

# -----------------------

def perform_compare_or_download(self):
    passed_args = self.request.arguments()

    a = self.request.get('from').strip()
    b = self.request.get('to').strip()
    content_ab = a, b

    if ('comparer_button' in passed_args) and not (r'' in content_ab):
        diff_string = make_diffstring(content_ab, '\r\n')

        # if make_diffstring can't resolve the content
        if diff_string == None:
            # perhaps pass an error message.. not needed for now
            self.render('webdiff.html')
            return

        self.render('diff_into_base.html',  diff=diff_string, 
                                            content_a=a, 
                                            content_b=b)
        return

    elif 'download_button' in passed_args:
        file_name = self.request.get('filename')
        CD_MESSAGE = "attachment; filename={}".format(file_name)
        self.response.headers['Content-Disposition'] = CD_MESSAGE
        self.response.headers['Content-Type'] = 'text/diff'

        diff_wad = make_unified_diff(content_ab, '\r\n')
        self.response.out.write(diff_wad)
        return 

    self.render('webdiff.html', content_a=a, content_b=b)

# -----------------------

class Welcome(PageHandler):

    def get(self):
        self.render('webdiff.html')

    def post(self):
        perform_compare_or_download(self)
       

class DiffGist(PageHandler):
    """Handles the matched regex of two numbers separated by a dash.

    /webdiff/gistid1-gistid2   
    where both gistids are valid gist id values.
    """
    def get(self, gist_ids):
        gist_id_a, gist_id_b = gist_ids.split('-')

        a = get_file(gist_id_a)
        b = get_file(gist_id_b)
        self.render('webdiff.html', content_a=a, 
                                    content_b=b)
    def post(self, gist_ids):
        perform_compare_or_download(self)


class _404(PageHandler):
    def get(self):
        self.redirect('/webdiff/')        



GIST_ID_RE = '(\d{3,}-\d{3,})'

app = webapp2.WSGIApplication([ ('/webdiff/' + GIST_ID_RE, DiffGist),
                                ('/webdiff/?', Welcome),
                                ('/?', _404)],  debug=True)

