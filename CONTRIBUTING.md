# Contributing to Financial Risk Assessment System 🤝

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## 🚀 Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

### We Use [Github Flow](https://guides.github.com/introduction/flow/index.html)

Pull requests are the best way to propose changes to the codebase:

1. 🍴 Fork the repo and create your branch from `main`
2. 🔧 If you've added code that should be tested, add tests
3. 📖 If you've changed APIs, update the documentation
4. 🧪 Ensure the test suite passes
5. 🎨 Make sure your code lints (follows our style guide)
6. 🚀 Issue that pull request!

## 🐛 Report Bugs Using GitHub Issues

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/ViktorFu/Financial-Risk-Assessment-System/issues/new).

### Great Bug Reports Include:

- **Summary**: Quick summary and/or background
- **Steps to reproduce**: Be specific! Include sample code if you can
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happens
- **Environment**: Your OS, Python version, etc.
- **Additional context**: Screenshots, logs, etc.

## 🎯 Suggest Features Using GitHub Issues

We welcome feature suggestions! When suggesting a feature:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested feature
- **Explain why this feature would be useful** to most users
- **List some other applications where this feature exists** (if applicable)

## 💻 Development Setup

### Prerequisites

```bash
# Required
Python 3.8+
Git
pip

# Recommended
Virtual environment tool (venv, conda, etc.)
IDE with Python support (VS Code, PyCharm, etc.)
```

### Setup Instructions

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Financial-Risk-Assessment-System.git
   cd Financial-Risk-Assessment-System
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   # Development dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If exists
   
   # Or install in development mode
   pip install -e .
   ```

4. **Set Up Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

5. **Run Tests**
   ```bash
   pytest tests/ -v
   ```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=project code/Client/

# Run specific test file
pytest tests/test_specific_module.py

# Run tests with verbose output
pytest -v

# Run performance tests
pytest tests/performance/ --benchmark-only
```

### Writing Tests

- Write tests for all new functionality
- Maintain test coverage above 80%
- Use descriptive test names
- Follow the AAA pattern (Arrange, Act, Assert)

**Example Test Structure:**
```python
def test_risk_assessment_calculation():
    # Arrange
    applicant_data = {
        'credit_score': 600,
        'debt_ratio': 0.3
    }
    
    # Act
    result = risk_controller.evaluate_loan_application(applicant_data)
    
    # Assert
    assert result['approved'] == True
    assert result['score'] >= 60
```

## 🎨 Code Style

### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:

- **Line length**: 88 characters (Black default)
- **Quotes**: Double quotes for strings
- **Imports**: Grouped and sorted with `isort`
- **Type hints**: Required for all public functions

### Code Formatting

We use the following tools:

```bash
# Format code
black project code/

# Sort imports
isort project code/

# Type checking
mypy project code/

# Linting
flake8 project code/
```

### Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only changes
- `style`: Changes that don't affect code meaning (formatting, etc.)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to build process or auxiliary tools

**Examples:**
```
feat(risk-engine): add credit score validation
fix(database): resolve connection pool timeout issue
docs(readme): update installation instructions
```

## 📁 Project Structure Guidelines

```
Financial-Risk-Assessment-System/
├── project code/
│   ├── Client/
│   │   ├── controllers/     # Business logic only
│   │   ├── models/         # Data access and models
│   │   ├── views/          # UI components
│   │   └── utils/          # Utility functions
│   ├── config/             # Configuration management
│   ├── tests/              # Test files
│   └── docs/               # Documentation
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
└── setup.py               # Package configuration
```

### File Naming Conventions

- **Python files**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions/variables**: `snake_case`
- **Constants**: `UPPER_CASE`
- **Test files**: `test_*.py`

## 🔐 Security Guidelines

### Reporting Security Vulnerabilities

**DO NOT** create a public GitHub issue for security vulnerabilities.

Instead, email us at: `security@financial-risk-system.com`

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Security Best Practices

- Never commit secrets, passwords, or API keys
- Use environment variables for sensitive configuration
- Validate all user inputs
- Follow OWASP guidelines for web security
- Keep dependencies updated

## 📋 Pull Request Checklist

Before submitting a pull request, ensure:

- [ ] 🧪 All tests pass (`pytest`)
- [ ] 📊 Code coverage doesn't decrease
- [ ] 🎨 Code follows style guidelines (`black`, `flake8`, `isort`)
- [ ] 📝 Documentation is updated (if needed)
- [ ] 🔍 Self-review completed
- [ ] 📋 PR description explains the changes
- [ ] 🏷️ Appropriate labels are added
- [ ] 🔗 Related issues are linked

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Screenshots (if applicable)
Include screenshots for UI changes

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
```

## 🌟 Recognition

Contributors will be recognized in:
- README.md acknowledgments
- CONTRIBUTORS.md file
- Release notes for significant contributions
- Annual contributor awards

## 📞 Getting Help

- 💬 **Discord**: [Join our community](https://discord.gg/financial-risk-system)
- 📧 **Email**: `developers@financial-risk-system.com`
- 📖 **Documentation**: Check the [docs](docs/) folder
- 🐛 **Issues**: Browse existing [GitHub issues](https://github.com/ViktorFu/Financial-Risk-Assessment-System/issues)

## 📜 License

By contributing, you agree that your contributions will be licensed under the same [MIT License](LICENSE) that covers the project.

---

**Thank you for contributing to Financial Risk Assessment System! 🎉** 