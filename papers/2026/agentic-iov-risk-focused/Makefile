PAPER ?= manuscript
BUILD := build
SUBMISSION := submission
ARXIV_STAGE := $(BUILD)/arxiv-stage
ARXIV_TARBALL := $(SUBMISSION)/arxiv-bundle.tar.gz

.PHONY: pdf clean watch arxiv arxiv-verify

pdf:
	mkdir -p $(BUILD)
	latexmk -pdf -outdir=$(BUILD) $(PAPER).tex

watch:
	mkdir -p $(BUILD)
	latexmk -pdf -outdir=$(BUILD) -pvc $(PAPER).tex

clean:
	latexmk -C -outdir=$(BUILD) $(PAPER).tex
	rm -rf $(BUILD)

# arXiv submission bundle (per https://info.arxiv.org/help/submit_tex.html).
# Ships the .bbl rather than the .bib so arXiv autotex never needs to chase a
# symlink resolution, and excludes every build artefact / hidden file / macOS
# metadata scrap. The staging dir is cleaned and rebuilt each call.
arxiv: pdf
	@mkdir -p $(SUBMISSION)
	@rm -rf $(ARXIV_STAGE)
	@mkdir -p $(ARXIV_STAGE)/figures
	@cp $(PAPER).tex $(ARXIV_STAGE)/$(PAPER).tex
	@cp $(BUILD)/$(PAPER).bbl $(ARXIV_STAGE)/$(PAPER).bbl
	@cp figures/*.png figures/*.pdf $(ARXIV_STAGE)/figures/ 2>/dev/null || true
	@find $(ARXIV_STAGE) -name '.DS_Store' -delete
	@find $(ARXIV_STAGE) -name '._*' -delete
	@rm -f $(ARXIV_TARBALL)
	@cd $(ARXIV_STAGE) && tar -czf ../../$(ARXIV_TARBALL) .
	@echo ""
	@echo "==> arXiv bundle ready: $(ARXIV_TARBALL)"
	@du -h $(ARXIV_TARBALL) | awk '{print "    size: " $$1}'
	@echo "    contents:"
	@tar -tzf $(ARXIV_TARBALL) | sed 's/^/      /'

# Verify the tarball compiles cleanly in a fresh tmpdir.
arxiv-verify: $(ARXIV_TARBALL)
	@TMPDIR_VERIFY=$$(mktemp -d -t arxiv-verify) && \
	  tar -xzf $(ARXIV_TARBALL) -C $$TMPDIR_VERIFY && \
	  cd $$TMPDIR_VERIFY && \
	  latexmk -pdf -interaction=nonstopmode $(PAPER).tex >/tmp/arxiv-verify.log 2>&1 && \
	  PAGES=$$(grep "Output written" /tmp/arxiv-verify.log | sed -E 's/.*\(([0-9]+) pages.*/\1/') && \
	  echo "==> arxiv-verify OK: $$PAGES pages" && \
	  echo "    fresh tmpdir: $$TMPDIR_VERIFY"
