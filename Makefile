# ──────────────────────────────────────────────────────────────────────────────
# Makefile — jolarca-observability
# ──────────────────────────────────────────────────────────────────────────────
# Compliance: SOC 2 Type II · GDPR · ISO 27001:2022 · PCI-DSS 4.0
# ──────────────────────────────────────────────────────────────────────────────

.PHONY: help setup lint test verify-all verify-retention verify-integrity verify-completeness clean

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup:  ## Install dependencies into .venv
	python3 -m venv .venv
	.venv/bin/pip install -r requirements-dev.txt

lint:  ## Run ruff, mypy, yamllint
	.venv/bin/ruff check scripts/ tests/
	.venv/bin/mypy --strict scripts/ tests/
	.venv/bin/yamllint -c .yamllint logging/ alerting/ audit-trail/ schemas/ compliance/

test:  ## Run pytest
	.venv/bin/pytest tests/ -v --tb=short

verify-retention:  ## Verify retention policy compliance (PCI-DSS 10.5.1)
	.venv/bin/python scripts/verify_retention.py

verify-integrity:  ## Verify hash-chain integrity config (PCI-DSS 10.5.5)
	.venv/bin/python scripts/verify_integrity.py

verify-completeness:  ## Verify log schema completeness (PCI-DSS 10.2)
	.venv/bin/python scripts/verify_completeness.py

verify-all: verify-retention verify-integrity verify-completeness  ## Run all verification scripts

clean:  ## Remove build artifacts
	rm -rf .venv __pycache__ .mypy_cache .ruff_cache .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
