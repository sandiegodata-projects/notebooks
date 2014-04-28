#! /usr/bin/env python 
# Convert an IPython notebook to HTML
import IPython.nbconvert
from IPython.config import Config
from IPython.nbconvert import HTMLExporter
from IPython.nbformat import current as nbformat
from IPython.nbconvert.preprocessors.base import Preprocessor
from IPython.nbconvert.preprocessors import CSSHTMLHeaderPreprocessor
import argparse, sys, os, datetime

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

parser = argparse.ArgumentParser(description='Convert an ipython notebook to  HTML')
parser.add_argument('files', metavar='files', nargs='+',  type=str,  help='The file to convert')

args = parser.parse_args()

root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

force = True

        
def convert(exporter, nb_file, suffix=''):

    nb_md = modification_date(nb_file)

    out_file = nb_file.replace('.ipynb', suffix+'.html').replace(' ','_')

    if os.path.exists(out_file):
        out_md = modification_date(out_file)

        if out_md > nb_md and not force:
            return None


    #print "NBConvert: {}".format(nb_file)

    with open(nb_file) as f:
        notebook = nbformat.reads_json(f.read())

    ## I use basic here to have less boilerplate and headers in the HTML.
    ## we'll see later how to pass config to exporters.

    (body,resources) = exporter.from_notebook_node(notebook)

    with open(out_file,'w') as f:
        f.write(body.encode('utf8'))

    return out_file

config=Config({
    'HTMLExporter':{
        'template_file':'local',
        'template_path': [os.path.join(root_dir,'_scripts')]
    },
})

exportHtmlA = HTMLExporter()
exportHtmlB = HTMLExporter(config=config)


out_files = set()

for file in args.files:
    
    if file.startswith('_'):
        continue
    
    for exporter, suffix in ( (exportHtmlA,'-code'), (exportHtmlB,'')):
        
        out_file = convert(exporter, file, suffix)
    
        if out_file:
            out_files.add(out_file)
    
    
print '\n'.join(out_files)

#
# The preprocessor isn't used, but may need it later. 
#

class LocalPreprocessor(Preprocessor):
    
    js = []
    css = []
    
    def __init__(self, root_dir, config=None, **kw):

        super(LocalPreprocessor, self).__init__(config=config, **kw)

        self.root_dir = root_dir
        
        self.get_inlines()

    def get_inlines(self):
        
        self.js = []
        js_file = os.path.join(self.root_dir, 'assets','js','ipython.js')
        
        #Load style CSS file.
        with open(js_file) as file:
            self.js.append(file.read())

        self.css = []
        css_file = os.path.join(self.root_dir, 'assets','css','ipython.css')
        
        #Load style CSS file.
        with open(css_file) as file:
            self.css.append(file.read())


    def preprocess(self, nb, resources):
        resources['ambry'] = {}
        resources['ambry']['js'] = self.js
        resources['ambry']['css'] = self.css
       
        return nb, resources
        
#exportHtmlB.register_preprocessor(LocalPreprocessor(root_dir), enabled=True)
    