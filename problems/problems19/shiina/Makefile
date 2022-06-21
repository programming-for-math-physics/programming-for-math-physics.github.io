FILENAME=kadaian

docker: $(FILENAME).tex
	docker run --rm -v ${PWD}:/workdir gitlab-registry.eidos.ic.i.u-tokyo.ac.jp/shiina/docker-latex/fonts bash -c "make pdf"
	evince $(FILENAME).pdf &

pdf: $(FILENAME).tex
	sed -e 's/。/. /g' $(FILENAME).tex | sed -e 's/、/, /g' > $(FILENAME).mid.tex
	latexmk -lualatex $(FILENAME).mid.tex
	cp -f $(FILENAME).mid.pdf $(FILENAME).pdf

clean:
	rm -f $(FILENAME).mid*

distclean: clean
	rm -f $(FILENAME).pdf
