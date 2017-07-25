# pytest-loglevels Plugin

Prototyping a pytest plugin to apply log levels to messages

Current limitation: cannot apply log levels to messages using standard print function or pytest generated messages

## Install

Download and build the package:

    python setup.py bdist_wheel
(wheel python plugin is required for build step)

Copy dist/pytest_loglevels-... .whl to a local python plugin server

    pip install pytest-loglevels

## Import

Import the API into test script using:
    
    from pytest import log
    
## Using the API
### Highest level (1)
Print a message at the highest log level (1)

    log.high_level_step("Very important test step 1")
which is then printed in the log output as

    1-1 High level step: Very important, first test step
The first 1 is the log level and the second 1 is the step of this log level.

Note: The "High level step" printing above is just for debug use and will be removed before release.    
   
A subsequent high level message is then printed as:
    
    1-2 High level step: Second test step
where the 2 indicates it is the second step at level 1.

### Detail Level (2)
Print a message at log level 2

    log.detail_step("More detailed test step information")
output:

    2-1 Detail level step: More detailed test step information
    
### Other log levels
The step function prints at the current log level if the log_level parameter is not defined
    
    log.step("This will be the next step at the current log level")
output:    

    2-2 Detail level step: This will be the next step at the current log level
    
Specifying a log level using the step function:
    log.step("Specify the log level", log_level=3)
output:

    3-1 Step: Specify the log level

Increment the current log level and print the message (default increment is 1 but can be specified using the increment parameter):
    
    log.step_increment("Increment the log level")
    log.step("Another step at this incremented level")
output:

    4-1 Step inc: Increment the log level
    4-2 Step: Another step at this incremented level
    