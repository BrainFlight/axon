

.PHONY: install-local-mac
install-local-mac:
	@echo "Installing PortAudio using Homebrew..."
	brew install portaudio
	@echo "Installing Python dependencies from requirements.in..."
	pip install -r requirements.in
