.PHONY: readme

readme:
	@echo "Updating README.md with latest results..."
	@# Extract everything up to and including "## Results" line
	@sed -n '1,/^## Results/p' README.md > README.tmp
	@# Add a blank line
	@echo "" >> README.tmp
	@# Add the results table
	@./report.py --format=markdown >> README.tmp
	@# Move the temp file over the original
	@mv README.tmp README.md
	@echo "README.md updated successfully!"