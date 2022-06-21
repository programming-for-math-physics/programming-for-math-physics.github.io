.PHONY: clean

pltfiles:=$(wildcard *.plt)
pdffiles:=$(pltfiles:.plt=.pdf)

all: $(pdffiles)

%.pdf: %.plt
	gnuplot $< || { if ! [ -s $(<:.plt=.pdf) ]; then rm $(<:.plt=.pdf); fi; exit 1; }

clean:
	rm -f *.pdf *.xbb

