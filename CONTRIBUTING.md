# Contributing to ProxmoxMCP

Thank you for considering contributing to ProxmoxMCP! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and welcoming community.

## How Can I Contribute?

### Reporting Bugs

If you find a bug, please create an issue on GitHub with the following information:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Any relevant logs or screenshots
- Your environment (OS, Python version, Proxmox version, etc.)

### Suggesting Enhancements

If you have an idea for an enhancement, please create an issue on GitHub with the following information:

- A clear, descriptive title
- A detailed description of the enhancement
- Any relevant examples or mockups
- Why this enhancement would be useful

### Pull Requests

1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Make your changes
4. Add or update tests as necessary
5. Update documentation as necessary
6. Submit a pull request

## Development Setup

1. Clone your fork of the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```
3. Set up a virtual environment:
   ```bash
   # Linux/macOS
   ./scripts/setup-venv.sh
   
   # Windows
   .\scripts\setup-venv.ps1
   ```
4. Create a test configuration:
   ```bash
   cp ProxmoxMCP/proxmox-config/config.template.json ProxmoxMCP/proxmox-config/config.json
   ```
   Edit the config.json file with your test Proxmox credentials.

## Coding Guidelines

- Follow PEP 8 style guidelines
- Write docstrings for all functions, classes, and modules
- Use type hints where appropriate
- Write tests for new functionality
- Keep functions and methods small and focused

## Testing

- Run tests before submitting a pull request:
  ```bash
  pytest
  ```
- Add tests for new functionality
- Ensure all tests pass

## Documentation

- Update documentation for any changes to functionality
- Use clear, concise language
- Include examples where appropriate

## Commit Messages

- Use clear, descriptive commit messages
- Reference issue numbers in commit messages when applicable
- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")

## Versioning

We use [Semantic Versioning](https://semver.org/) for this project.

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.
