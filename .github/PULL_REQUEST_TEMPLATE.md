# Description

Please include a summary of the change and which issue is fixed. Please also include relevant motivation and context. List any dependencies that are required for this change.

Fixes # (issue)

## Type of change

Please add a line in the relevant section of [CHANGELOG.md](https://github.com/pybamm-team/PyBaMM/blob/develop/CHANGELOG.md) to document the change (include PR #) - note reverse order of PR #s. If necessary, also add to the list of breaking changes.

- [ ] New feature (non-breaking change which adds functionality)
- [ ] Optimization (back-end change that speeds up the code)
- [ ] Bug fix (non-breaking change which fixes an issue)

# Key checklist:

- [ ] No style issues: `$ pre-commit run` (or `$ nox -s pre-commit`) (see [CONTRIBUTING.md](https://github.com/pybamm-team/PyBaMM/blob/develop/CONTRIBUTING.md#installing-and-using-pre-commit) for how to set this up to run automatically when committing locally, in just two lines of code)
- [ ] All tests pass: `$ python run-tests.py --all` (or `$ nox -s tests`)
- [ ] The documentation builds: `$ python run-tests.py --doctest` (or `$ nox -s doctests`)

You can run integration tests, unit tests, and doctests together at once, using `$ python run-tests.py --quick` (or `$ nox -s quick`).

## Further checks:

- [ ] Code is commented, particularly in hard-to-understand areas
- [ ] Tests added that prove fix is effective or that feature works
