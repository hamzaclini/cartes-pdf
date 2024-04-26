# Sequential FlashCard generator

This project allows for the generation of a formatted pdf file
containing a set of flashcards with questions and answers in the
ANKI style. The aim of this pdf is to be printed recto-verso with
questions on one side and answer on the other side.

This app can be accessed on streamlit [here](https://cartes-pdf.streamlit.app/)

## Use of FPDF package

PDF formatting is defined in a .csv file using the template.py class from
[FDPF](https://github.com/reingart/pyfpdf/tree/master/fpdf) project.
Properties are as followed :

* name: placeholder identification
* type: 'T': texts, 'L': lines, 'I': images, 'B': boxes, 'BC': barcodes 
* x1, y1, x2, y2: top-left, bottom-right coordinates (in mm)
* font: e.g. "Arial"
* size: text size in points, e.g. 10 
* bold, italic, underline: text style (non-empty to enable)
* foreground, background: text and fill colors, e.g. 0xFFFFFF
* align: text alignment, 'L': left, 'R': right, 'C': center
* text: default string, can be replaced at runtime
* priority: Z-order
* multiline: None for single line (default), True to for multicells (multiple lines), False trims to exactly fit the space defined
> Important for multiline: you should set coordinates for the cell containing the first line. It will then be repeated as 
> many times as required to fit the whole text

## Improvement

* Find a way to input lists (with return to the line):
  * Streamlit side : st.textarea
  * FPDF side : 
* See if it is possible to add an option to change the csv template : to modify size, alignment