.PHONY: test lint check demo run-all clean docker-build docker-run help scenario-504 scenario-confirmed scenario-refused scenario-tcp-reset

help:
	@echo "Available targets:"
	@echo "  test           - Run pytest test suite"
	@echo "  lint           - Run syntax checks"
	@echo "  check          - Run lint and tests"
	@echo "  demo           - Run the demo launcher"
	@echo "  run-all        - Run all scenarios in interactive mode"
	@echo "  scenario-*     - Run specific scenarios (504, confirmed, refused, tcp-reset)"
	@echo "  clean          - Remove generated audit artifacts"
	@echo "  docker-build   - Build the container image"
	@echo "  docker-run     - Run the containerized harness locally"

test:
	python3 -m pytest tests/ -v

lint:
	python3 -m py_compile run.py demo_launcher.py

check: lint test

demo:
	python3 demo_launcher.py

run-all:
	python3 run.py --all-scenarios --export-dir ./audit_out

scenario-504:
	python3 run.py --scenario 504_timeout --export-dir ./audit_out/504_timeout

scenario-confirmed:
	python3 run.py --scenario confirmed --export-dir ./audit_out/confirmed

scenario-refused:
	python3 run.py --scenario refused --export-dir ./audit_out/refused

scenario-tcp-reset:
	python3 run.py --scenario tcp_reset --export-dir ./audit_out/tcp_reset

clean:
	rm -rf audit_out/
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +

docker-build:
	docker build -t smaos-demo:0.1.0 .

docker-run:
	docker run --rm -p 127.0.0.1:8765:8765 smaos-demo:0.1.0
