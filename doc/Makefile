TARGETS = \
	post-meeting-motes-20160323.pdf \



all: ${TARGETS}

clean:
	rm -f ${TARGETS}

mrproper: clean
	rm -f *~



figs/ahu1_from_writeboard.pdf: figs/ahu1_from_writeboard.svg
	inkscape -z --file=figs/ahu1_from_writeboard.svg -D --export-pdf=figs/ahu1_from_writeboard.pdf

figs/aspects-graph-example.pdf: figs/aspects-graph-example.svg
	inkscape -z --file=figs/aspects-graph-example.svg -D --export-pdf=figs/aspects-graph-example.pdf



post-meeting-motes-20160323.pdf: post-meeting-motes-20160323.tex figs/ahu1_from_writeboard.pdf figs/aspects-graph-example.pdf
	pdflatex post-meeting-motes-20160323.tex
	pdflatex post-meeting-motes-20160323.tex

