.PHONY: clean

svgfiles:=$(wildcard *.svg)
pdffiles:=$(svgfiles:.svg=.pdf_tex)

all: $(pdffiles)

%.pdf_tex: %.svg
	inkscape -D -z --file=$< --export-pdf=$(<:.svg=.pdf) --export-latex

clean:
	rm -f *.pdf *.pdf_tex *.aux *.xbb

