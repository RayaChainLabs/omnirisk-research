PAPER ?= manuscript
BUILD := build

.PHONY: pdf clean watch

pdf:
	mkdir -p $(BUILD)
	latexmk -pdf -outdir=$(BUILD) $(PAPER).tex

watch:
	mkdir -p $(BUILD)
	latexmk -pdf -outdir=$(BUILD) -pvc $(PAPER).tex

clean:
	latexmk -C -outdir=$(BUILD) $(PAPER).tex
	rm -rf $(BUILD)
