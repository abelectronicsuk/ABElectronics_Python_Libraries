# Contributing to ABElectronics_Python_Libraries

Thank you for your interest in contributing! We welcome contributions of all kinds, whether it’s fixing bugs, adding new features, improving documentation, or writing tests. To ensure a smooth process, please follow these guidelines.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)  
2. [How to Contribute](#how-to-contribute)  
   1. [Reporting Issues](#reporting-issues)  
   2. [Suggesting Enhancements](#suggesting-enhancements)  
   3. [Your First Pull Request](#your-first-pull-request)  
   4. [Development Workflow](#development-workflow)  
3. [Coding Standards](#coding-standards)  
   1. [Python Version Support](#python-version-support)  
   2. [Code Style & Quality](#code-style--quality)  
   3. [Testing](#testing)  
4. [Documentation](#documentation)  
5. [Release Process](#release-process)  
6. [License](#license)  

---

## Code of Conduct

By participating in this project, you agree to abide by the **[Code of Conduct](CODE_OF_CONDUCT.md)**. Please read it to understand the expectations for behaviour and how to report unacceptable conduct.

---

## How to Contribute

### Reporting Issues

If you find a bug, or something doesn’t work as expected, please open an issue with:

- A descriptive title (e.g. “IOPi.get_pin_direction() fails when channel > 7”)  
- A clear description of the problem  
- Steps to reproduce  
- The version of the library  
- Environment details (Raspberry Pi version, OS version, Python version)  
- Any error messages, stack traces, or logs  

Before opening, please search existing issues to avoid duplicates.

### Suggesting Enhancements

If you have ideas for improvements or new features, open an issue labelled **enhancement**. Provide:

- The motivation for the change  
- A proposed design change or addition  
- Any potential backwards compatibility impact  

We welcome discussion before you start coding so we can ensure alignment.

### Your First Pull Request

We’d love to help you get started. Here’s how:

1. Fork the repository  
2. Clone your fork locally  
3. Create a feature branch (e.g. `feature/xyz` or `fix/abc`)  
4. Make your changes, ensuring adherence to style and existing patterns  
5. Add or update tests and documentation  
7. Push your branch to your fork  
8. Open a Pull Request (PR) against the `master` branch  
9. In the PR description, reference any relevant issue(s) and explain your change  

Your PR will be reviewed by maintainers; you may get feedback or requests for changes. Please be patient and responsive to feedback.

### Development Workflow

- **Branching**: Always branch off `master` for new work  
- **Rebase or merge?** Use rebase to keep your commit history clean (or merge, depending on project preference)  
- **Commit messages**: Use clear, imperative style (e.g. “Fix I2C read error when buffer full”)  
- **Pull Requests**: Should ideally contain only one logical change; avoid mixing unrelated changes  

---

## Coding Standards

### Python Version Support

This library supports **Python 3 only** (as stated in README).  
If support for additional Python versions is desired, it should be treated as a separate effort (or branch).

### Code Style & Quality

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) conventions  
- Use meaningful variable and function names  
- Avoid overly long functions — refactor where appropriate  
- Add inline comments for tricky logic  


We encourage use of linters (e.g. `flake8`, `pylint`) and formatters (e.g. `black`, `isort`) — maintainers may run these checks during CI.

### Testing

- Provide tests for new features or bug fixes  
- Use the existing test framework / structure  
- Ensure new tests pass locally before opening PR  
- Aim for good coverage, particularly for edge cases  

If your change cannot be tested automatically (e.g. hardware-specific behaviour), document how to test it manually.

---

## Documentation

- Update **README.md**, **CHANGELOG.md**, or module-level docstrings to reflect your changes  
- If you add a new class or module, include usage examples  
- Keep written style consistent with the existing docs  

Good documentation is as important as good code.

---

## Release Process

- Releases are made by maintainers (often via GitHub Releases)  
- Before a release:  
  - Bump version number in `setup.py` / `pyproject.toml`  
  - Update CHANGELOG with notable changes  
  - Ensure all tests pass  
- Tag the release and create a GitHub release entry  

If your PR merits inclusion in the next release, it's helpful to mention it in your PR.

---

## License

By contributing, you agree that your contributions will be licensed under the same licence as the project (GPL-2.0).  
(See the [LICENSE](LICENSE) file.)

---

Thank you for helping improve **ABElectronics_Python_Libraries**! Your efforts are appreciated.  
If in doubt, feel free to open an issue or ask maintainers for guidance before diving in.
