.PHONY: plot svg clean

F=presentation

all: $F.pdf

texfiles:=$(wildcard *.tex)

$F.pdf: $F.dvi
	dvipdfmx $<

$F.dvi: plot $(texfiles)
	platex -shell-escape --kanji=utf8 $F

plot:
	$(MAKE) -C plot

svg:
	$(MAKE) -C svg

clean:
	-$(MAKE) -C plot clean
	#$(MAKE) -C svg clean
	-rm -f *~ *.dvi *.aux *.log *.pdf *.blg *.bbl

