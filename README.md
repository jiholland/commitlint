# commitlint
Python module that will lint commit messages according to [conventional commit scheme](https://www.conventionalcommits.org).

## usage
Intended to be used in a Git CI/CD pipeline.

```yaml
Run without arguments.
$ python3 commitlint.py

Pass the Git root directory as an argument.
$ python3 commitlint.py "$(realpath git_example_root_dir)"

Pass the GitLab project directory as an argument.
$ python3 commitlint.py $CI_PROJECT_DIR
```

## license
BSD-3-Clause
