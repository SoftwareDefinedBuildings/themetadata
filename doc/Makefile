TARGETS = \
	post-meeting-motes-20160323.pdf \


all: ${TARGETS}

clean:
	rm -f ${TARGETS}

mrproper: clean
	rm -f *~


post-meeting-motes-20160323.pdf: post-meeting-motes-20160323.tex
	pdflatex post-meeting-motes-20160323.tex
	pdflatex post-meeting-motes-20160323.tex

