.PHONY: plot svg markdown clean

F=report

all: $F.pdf

texfiles:=$(wildcard *.tex)

$F.pdf: $F.dvi
	dvipdfmx $<

$F.dvi: plot svg markdown $(texfiles)
	platex --shell-escape --kanji=utf8 $F
	-pbibtex -kanji=utf8 $F
	platex --shell-escape --kanji=utf8 $F

plot:
	$(MAKE) -C plot

svg:
	$(MAKE) -C svg

markdown:
	$(MAKE) -C markdown

clean:
	$(MAKE) -C plot clean
	$(MAKE) -C svg clean
	$(MAKE) -C markdown clean
	rm -f *~ *.dvi *.aux *.log *.pdf *.blg *.bbl

