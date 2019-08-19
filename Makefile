default:
	@echo "make clean"


.PHONY: clean
clean:
	rm -rf generated_tests
	rm -rf logs
	rm -rf reports
