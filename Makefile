WORKDIR=build
ANTLR_VERSION=4.10
ANTLR_JAR=antlr-$(ANTLR_VERSION)-complete.jar

PROJECT=grammars-v4
GITHUB_URL=git@github.com:facetoe/$(PROJECT).git
GRAMMAR_COMMIT=4a9bb0a5dc9cedbfafac688791ad0245a8d9d539

$(WORKDIR)/$(ANTLR_JAR):
	mkdir -p $(WORKDIR)
	curl https://www.antlr.org/download/$(ANTLR_JAR) -o $(WORKDIR)/$(ANTLR_JAR)

$(WORKDIR)/$(PROJECT):
	git clone $(GITHUB_URL) $(WORKDIR)/$(PROJECT)

generate-parser: $(WORKDIR)/$(ANTLR_JAR) $(WORKDIR)/$(PROJECT)
	git -C $(WORKDIR)/$(PROJECT) reset --hard "$(GRAMMAR_COMMIT)"
	(cd $(WORKDIR)/$(PROJECT)/promql && java -jar $(CURDIR)/$(WORKDIR)/$(ANTLR_JAR) -Dlanguage=Python3 PromQLLexer.g4 -visitor -o $(CURDIR)/promval/parser)
	(cd $(WORKDIR)/$(PROJECT)/promql && java -jar $(CURDIR)/$(WORKDIR)/$(ANTLR_JAR) -Dlanguage=Python3 PromQLParser.g4 -visitor -o $(CURDIR)/promval/parser)

clean:
	rm -rf $(WORKDIR)

test:
	PYTHONPATH=. pytest-3 tests/

reformat:
	black --exclude promval/parser promval/ tests/

flake8:
	flake8 --exclude  promval/parser/ promval/ tests/
