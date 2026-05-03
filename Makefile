.PHONY: help new publish list

help:
	@echo "OmniRisk papers — academic publication repo"
	@echo
	@echo "Commands:"
	@echo "  make new SLUG=<slug>           — scaffold a new paper under papers/<year>/<slug>/"
	@echo "  make publish PAPER=<dir>       — build + replicate to s3://omnirisk-insights-bucket/papers/..."
	@echo "  make list                      — list all papers + their status"
	@echo
	@echo "Per-paper (cd into the paper dir first):"
	@echo "  make pdf                       — compile manuscript.tex via latexmk"
	@echo "  make watch                     — recompile on save"
	@echo "  make clean                     — remove build artefacts"

new:
	@test -n "$(SLUG)" || (echo "usage: make new SLUG=my-slug" && exit 2)
	@bin/new $(SLUG)

publish:
	@test -n "$(PAPER)" || (echo "usage: make publish PAPER=papers/2026/my-slug" && exit 2)
	@bin/publish $(PAPER)

list:
	@find papers -mindepth 2 -maxdepth 2 -type d | sort | while read d; do \
	  status=$$(grep '^status:' "$$d/meta.yaml" 2>/dev/null | sed 's/status: *//; s/"//g' || echo "—"); \
	  title=$$(grep '^title:' "$$d/meta.yaml" 2>/dev/null | sed 's/title: *//; s/"//g' || echo "—"); \
	  printf "  %-12s  %-40s  %s\n" "[$$status]" "$$d" "$$title"; \
	done
