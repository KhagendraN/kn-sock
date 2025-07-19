# Contributing to kn-sock

🎉 First off, thanks for considering contributing to **kn-sock**!

We welcome all types of contributions — bug reports, feature suggestions, documentation improvements, tests, or code changes.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#-how-to-contribute)
- [Development Setup](#-development-setup)
- [Code Style Guidelines](#-code-style-guidelines)
- [Testing Guidelines](#-testing-guidelines)
- [Documentation Guidelines](#-documentation-guidelines)
- [Issue Reporting](#-issue-reporting)
- [Pull Request Guidelines](#-pull-request-guidelines)
- [Release Process](#-release-process)
- [Need Help?](#-need-help)

---

## 🤝 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

**Be respectful and inclusive** - We welcome contributors from all backgrounds and experience levels.

---

## 📝 How to Contribute

### 1. Fork the Repository

Click the **Fork** button on the top-right corner of [this repo](https://github.com/KhagendraN/kn-sock) to create your own copy.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/kn-sock.git
cd kn-sock
```

### 3. Set Up Development Environment

```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-asyncio black flake8 mypy

# Install the package in development mode
pip install -e .
```

### 4. Create a New Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
# or
git checkout -b docs/your-documentation-update
```

### 5. Make Changes & Add Tests

- Stick to the existing code style (see [Code Style Guidelines](#-code-style-guidelines))
- Add unit tests for any new functionality
- Update or create documentation if needed
- Ensure all tests pass locally

### 6. Commit and Push

```bash
git add .
git commit -m "feat: add new TCP connection pooling feature"
git push origin feature/your-feature-name
```

**Commit Message Guidelines:**
- Use conventional commit format: `type(scope): description`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Keep descriptions clear and concise

### 7. Submit a Pull Request

Go to your forked repo on GitHub and click "Compare & pull request".

Describe your changes clearly so reviewers understand the context.

---

## 🛠️ Development Setup

### Prerequisites

- Python 3.6 or higher
- pip
- git

### Local Development

1. **Clone and setup:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/kn-sock.git
   cd kn-sock
   pip install -e .
   ```

2. **Install development tools:**
   ```bash
   pip install pytest pytest-asyncio black flake8 mypy
   ```

3. **Verify installation:**
   ```bash
   python -c "import kn_sock; print(kn_sock.__version__)"
   ```

---

### Docker-based Development & Testing

- The project provides a `Dockerfile` for building a minimal Python environment with all dependencies.
- The `docker-compose.yml` orchestrates two services:
    - `knsock`: for running CLI commands
    - `test`: for running the test suite

**Common Docker commands:**

```bash
# Build the Docker image (uses Dockerfile)
docker-compose build

# Run CLI help
docker-compose run knsock

# Run all tests
docker-compose run test

# Run a specific test file
docker-compose run test pytest test/test_tcp_udp_msg.py -v

# Interactive development shell
docker run -it --rm -v $(pwd):/app knsock:latest bash
```

---

## 🎨 Code Style Guidelines

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 88 characters (Black formatter default)
- Use meaningful variable and function names
- Add type hints to all public functions

### Code Formatting, Linting, and Type Checking

We use [Black](https://black.readthedocs.io/), [Flake8](https://flake8.pycqa.org/), and [mypy](http://mypy-lang.org/) for code quality. All are managed via [pre-commit](https://pre-commit.com/) hooks, configured in `.pre-commit-config.yaml`.

**To set up and use pre-commit hooks:**

```bash
pip install pre-commit
pre-commit install  # Set up git hooks
pre-commit run --all-files  # Run on all files
```

This will automatically check formatting, linting, and types before you commit. See `.pre-commit-config.yaml` for details.

### Code Formatting

We use [Black](https://black.readthedocs.io/) for code formatting:

```bash
# Format all Python files
black kn_sock/ test/ examples/

# Check formatting without making changes
black --check kn_sock/ test/ examples/
```

### Linting

We use [flake8](https://flake8.pycqa.org/) for linting:

```bash
# Run linter
flake8 kn_sock/ test/ examples/
```

### Type Checking

We use [mypy](http://mypy-lang.org/) for type checking:

```bash
# Run type checker
mypy kn_sock/
```

---

## 🧪 Testing Guidelines

### Running Tests

```bash
# Run all tests
pytest -s test/

# Run tests with coverage
pytest --cov=kn_sock test/

# Run specific test file
pytest test/test_tcp_udp_msg.py

# Run tests in parallel
pytest -n auto test/
```

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names
- Test both success and failure cases
- Use fixtures for common setup
- Mock external dependencies when appropriate

### Test Structure

```python
def test_function_name():
    """Test description of what is being tested."""
    # Arrange
    expected = "expected result"

    # Act
    result = function_under_test()

    # Assert
    assert result == expected
```

---

## 📚 Documentation Guidelines

### Docstrings

- Use Google-style docstrings
- Include type hints
- Provide usage examples
- Document all parameters and return values

Example:
```python
def send_tcp_message(host: str, port: int, message: str) -> None:
    """Send a message to a TCP server.

    Args:
        host: The target host address.
        port: The target port number.
        message: The message to send.

    Raises:
        ConnectionError: If connection fails.

    Example:
        >>> send_tcp_message("localhost", 8080, "Hello, World!")
    """
```

### README Updates

- Update README.md for new features
- Add usage examples
- Update installation instructions if needed

---

## 🐛 Issue Reporting

### Before Creating an Issue

1. Check if the issue has already been reported
2. Search existing issues and pull requests
3. Try to reproduce the issue with the latest version

### Issue Template

When creating an issue, please include:

```markdown
## Bug Description
Brief description of the bug

## Steps to Reproduce
1.
2.
3.

## Expected Behavior
What you expected to happen

## Actual Behavior
What actually happened

## Environment
- OS:
- Python version:
- kn-sock version:

## Additional Information
Any other context about the problem
```

### Feature Requests

For feature requests, include:

```markdown
## Feature Description
Brief description of the feature

## Use Case
Why this feature would be useful

## Proposed Implementation
How you think this could be implemented

## Additional Information
Any other context about the feature request
```

---

## 🔄 Pull Request Guidelines

### Before Submitting

- [ ] All tests pass
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] Commit messages follow conventional format
- [ ] PR description is clear and complete

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Test addition/update
- [ ] Other (please describe)

## Testing
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or breaking changes documented)
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs tests and linting
2. **Code Review**: At least one maintainer reviews the PR
3. **Approval**: PR is approved and merged

---

## 💬 Need Help?

### Getting Started

- Check out our [good first issues](https://github.com/KhagendraN/kn-sock/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
- Read the [documentation](https://kn-sock.khagendraneupane.com.np)
- Look at existing examples in the `examples/` directory

### Communication

- **Issues**: Use GitHub issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for questions and general chat
- **Email**: Contact maintainers directly if needed

### Resources

- [Python Socket Programming](https://docs.python.org/3/library/socket.html)
- [asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)

---

## 🙏 Recognition

Contributors will be recognized in:

- [Contributors list](https://github.com/KhagendraN/kn-sock/graphs/contributors)
- Release notes
- Project documentation

---

Thanks again for contributing to **kn-sock**! 💙

Your contributions help make this project better for everyone in the community.
