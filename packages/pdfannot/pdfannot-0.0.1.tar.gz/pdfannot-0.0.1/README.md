
# pdfannot

This package aims to create a two-way link between annotated pdf and excel data frame.

It allows you to :

   - create an excel file containing each string annotated of the pdf in a column 'annot_text', along with its 
   annotation in a column 'content'.
    
   - annotate a pdf given an excel file of the form described above.
   
It can be really useful for generating automatically annotated pdf documents with NLP models capable to
infer annotations from raw texts in a data frame.


### Prerequisites

fitz

### Installing

pip install pymupdf
(pipenv install pymupdf)

import fitz

### Authors

Arthur Renaud, Antoine Marullaz


