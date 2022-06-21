.PHONY: clean

mdfiles:=$(wildcard *.md)
texfiles:=$(mdfiles:.md=.tex)

all: $(texfiles)

%.tex: %.md
	pandoc -o $(<:.md=.tex) $<

clean:
	rm -f *.tex

