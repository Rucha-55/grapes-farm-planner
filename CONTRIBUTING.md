# Contributing to Grape and Apple Disease Detection System

Thank you for your interest in contributing to the Grape and Apple Disease Detection System! We welcome contributions from the community to help improve this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style](#code-style)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)
- [License](#license)

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/grapes-farm-planner.git
   cd grapes-farm-planner
   ```
3. **Set up the development environment**:
   ```bash
   # Create and activate a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate

   # Install development dependencies
   pip install -r requirements-dev.txt
   ```

## Development Workflow

1. **Create a new branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/issue-number-description
   ```

2. **Make your changes** following the code style guidelines.

3. **Run tests** to ensure nothing is broken:
   ```bash
   pytest
   ```

4. **Commit your changes** with a descriptive commit message:
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

5. **Push your changes** to your fork:
   ```bash
   git push origin your-branch-name
   ```

6. **Open a pull request** against the `main` branch.

## Code Style

We use several tools to maintain code quality and style:

- **Black** for code formatting
- **Flake8** for linting
- **isort** for import sorting
- **mypy** for static type checking

Before committing, run:

```bash
black .
isort .
flake8 .
mypy .
```

## Testing

We use `pytest` for testing. To run the test suite:

```bash
pytest
```

To run tests with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

## Pull Request Process

1. Ensure your code passes all tests and linting checks.
2. Update the README.md with details of changes if needed.
3. Include relevant tests for new features or bug fixes.
4. Ensure your branch is up to date with the latest changes from `main`.
5. Open a pull request with a clear title and description.

## Reporting Issues

When reporting issues, please include:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected vs. actual behavior
- Any relevant error messages or screenshots
- Your environment details (OS, Python version, etc.)

## Feature Requests

We welcome feature requests! Please open an issue with:

- A clear description of the feature
- The problem it solves
- Any alternative solutions you've considered

## License

By contributing, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
