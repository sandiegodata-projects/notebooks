IPython Notebooks
=========================

IPython Notebooks for data analysis projects. These notebooks all use the Ambry data packaging system to get data, and primarily use Pandas and Matplotlib for visualization


Building HTML
-------------

The `pre-commit` script will search for .ipynb files that are newer than their 
corresponding HTML file and re-generate them. Each .ipynb file is converyted to two 
HTML files, one with the default IPython template, and one that hides the code. 

