normal:
	@$(MAKE) -C src compile --no-print-directory
	@if [ $$? -eq 0 ]; then \
        echo "Success: generated executable src/main"; \
    fi


withrv:
	@$(MAKE) -C rv instrument --no-print-directory
	@if [ $$? -eq 0 ]; then \
        echo "Success: generated executable rv/main-instrumented"; \
    fi


clean:
	@$(MAKE) -C src clean --no-print-directory
	@$(MAKE) -C rv clean --no-print-directory
