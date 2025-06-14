# The purpose of this script is to activate the Python extension in
# VS Code. Open this file, and review the "Python" tab in the bottom
# left corner. You should see the currently selected Python interpreter.
# It should be version 3.12.8 (or the version the instructor says). If it
# is not, the click the tab and select the correct Python interpreter.

# Review the code below. Do you see the "-> None" and the "name: str". The
# types listed are called type hints. They are used to help you and other
# developers understand the expected types of the function arguments and
# return values. They are not required, but they are helpful. We will be
# using them in this course. The linter if configured to check the types
# of the variables and function arguments. If you pass the wrong type, you
# will see a warning.

# Finally, we are using Ruff as the code linter and formatter. The formatter
# will run on "Save".

# To view the settings for the VS Code editing environment, review the
# `settings.json` file in the `.vscode` directory at the root of this code
# repository.


def main(name: str) -> None:
    print(f"Hello, {name}!")


if __name__ == "__main__":
    main("World!")
