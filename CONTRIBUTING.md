# Contributing to Network Port Scanner

First off, thank you for considering contributing to the Network Port Scanner project! We welcome contributions in the form of bug reports, feature requests, code improvements, and documentation enhancements. This guide will help you get started.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Submitting Pull Requests](#submitting-pull-requests)
- [Development Workflow](#development-workflow)
- [Coding Guidelines](#coding-guidelines)
- [License](#license)

## Code of Conduct

This project adheres to the Contributor Covenant Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [Suraj Kumar](https://dsa.pythonanywhere.com/contact).

## How Can I Contribute?

### Reporting Bugs

If you find a bug in the project, please create an issue on GitHub. When reporting a bug, please include:

- A clear and descriptive title.
- The steps to reproduce the bug.
- Any error messages or screenshots.
- Your environment (e.g., operating system, Python version).

### Suggesting Enhancements

We welcome suggestions for new features or improvements. To suggest an enhancement, please create an issue on GitHub and include:

- A clear and descriptive title.
- A detailed description of the proposed enhancement.
- Any relevant examples or mockups.

### Submitting Pull Requests

If you'd like to contribute code to the project, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix (`git checkout -b feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add feature'`).
5. Push to your branch (`git push origin feature-name`).
6. Create a pull request on GitHub.

When submitting a pull request, please ensure that your code adheres to the project's coding guidelines.

## Development Workflow

Since the project currently does not have specific dependencies or tests, follow these general guidelines:

1. Clone the repository:
    ```bash
    git clone https://github.com/Surajkumarsaw1/port-scanner.git
    cd port-scanner
    ```

2. (Optional) Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Make your changes in a new branch:
    ```bash
    git checkout -b feature-name
    ```

4. Test your changes locally (if applicable):
    - If testing is required for your changes, please include appropriate test cases in your pull request description.

5. Commit and push your changes:
    ```bash
    git add .
    git commit -m "Describe your changes"
    git push origin feature-name
    ```

6. Create a pull request on GitHub and provide a detailed description of your changes.

## Coding Guidelines

- Follow PEP 8 for Python code style.
- Use descriptive variable and function names.
- Write docstrings for all public functions and classes.
- Keep commits small and focused on a single change.

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing!
