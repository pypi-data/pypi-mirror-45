# Kontr Test Development Kit

Kontr Test Development Kit was designed to write custom test scenarios for multiple programming languages.
Configuration is done by python script with predefined structure.

## Getting stated
`KTDK` is a library, to use it, you have to install it, or add it to your's `Pipenv` or `requirements.txt` file.

### Prerequisites
- Python 3.6 or later
- (Optional) [pipenv](https://github.com/pypa/pipenv)

### Install the released version

You can install ktdk using the `pip`:
```bash
$ pip install ktdk
```

Or you can add it as a development dependency using the ``pipenv``

```bash
$ pipenv install ktdk
```

### Install the development version

You can either use the `Pipenv` command.

```shell
pipenv install git+https://gitlab.fi.muni.cz/grp-kontr2/ktdk.git
```

or the `pip` command:

```shell
pip install git+https://gitlab.fi.muni.cz/grp-kontr2/ktdk.git
```


### Available Env variables

- `KTDK_WORKSPACE` - Workspace dir
- `KTDK_TEST_FILES` - Test files dir
- `KTDK_SUBMISSION` - Student's submission dir
- `KTDK_RESULTS` - Results directory submission dir
- `KTDK_ENTRY_POINT` - Entry point - main script (default: `instructions.py`)
- `KTDK_TEST_TIMEOUT` - Test timeout
- `KTDK_WEBHOOK_URL` - Webhook url
- `KTDK_WEBHOOK_TOKEN` - Webhook token
- `KTDK_TEST_TIMEOUT` - Test timeout
- `KTDK_SUITE_TIMEOUT` - Suite timeout
- `KTDK_SUITE_ID` - Suite ID

## Run the cli tool
Ktdk also provides a simple cli tool, to run your tests

```bash
# Show the help
$ ktdk --help

# List all the static tests
$ ktdk tests list

# Run your tests using the ktdk
$ ktdk execute --help

# Example:
$ ktdk execute --submission="<SUBMISSION_DIR>" --test-files="<TEST_FILES_DIR>" --devel
```


## Examples
 TBD - python examples of the KTDK tests

## Development

Take a look at the [contribution guide]( 
https://gitlab.fi.muni.cz/grp-kontr2/kontr-documentation/blob/master/contributing/GeneralContributionGuide.adoc)



