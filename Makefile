.PHONY: run
run:
	python3 -m src.main

.PHONY: dashboard
dashboard:
	streamlit run src/dashboard.py

.PHONY: install-local-mac
install-local-mac:
	@echo "Installing PortAudio using Homebrew..."
	brew install portaudio
	@echo "Installing Python dependencies from requirements.in..."
	pip install -r requirements.in

.PHONY: run-inference-pod-local
run-inference-pod-local:
	@echo "Running inference pod on local Docker"
	docker run -p 50051:50051 fydp-local-inference-service
