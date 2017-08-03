##
# @file pytest-loglevels.py
# @author Sam Lea (samjl) <samjlea@gmail.com>
# @created 12/07/17
# @brief pytest plugin loglevels - functions to assign and print a log
# level to test log messages.
# Supports pytest-outputredirect plugin so all log messages (including
# standard print function) are assigned a log level and associated
# step.

import pytest

MIN_LEVEL = 0
MAX_LEVEL = 5


# Move this configuration to the end to ensure outputredirect (is
# installed) is configured first.
@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    redirect_plugin = config.pluginmanager.getplugin('outputredirect')
    if redirect_plugin:
        import sys
        if isinstance(sys.stdout, redirect_plugin.LogOutputRedirection):
            MultiLevelLogging.output_redirect_enabled = True


def pytest_namespace():
    # Add logging functions to the pytest namespace
    class LogLevel:
        """Class containing logging methods used to apply a log level
        to a message.
        Note: This class should not and does not need to be instantiated.
        """
        @staticmethod
        def high_level_step(msg):
            """Print a message at the highest log level."""
            set_log_parameters(msg, log_level=1)

        @staticmethod
        def detail_step(msg):
            """Print a message at the second highest log level."""
            set_log_parameters(msg, log_level=2)

        @staticmethod
        def step(msg, log_level=None):
            """Print a message at the specified or current log level.
            If optional argument log_level is not specified or None
            then the log level of the previous message is applied.
            """
            set_log_parameters(msg, log_level)

        @staticmethod
        def step_increment(msg, increment=1):
            """Increment the current log level and print message at the
            new level.
            """
            current_level = MultiLevelLogging.current_level
            set_log_parameters(msg, current_level + increment)

        # TODO add block printing for lists and strings containing linebreaks

    class Redirect:
        # These functions are not required to be in the public API but
        # are required by the output redirection plugin.
        @staticmethod
        def is_level_set():
            """Return True if current message being processed has a log
            level assigned. Used to differentiate between messages
            originating from this API and those from the standard print
            functions.
            Note: This function is used by the outputredirect plugin.
            """
            return MultiLevelLogging.log_level_set

        @staticmethod
        def get_current_level():
            """Return the current log level.
            Note: This function is used by the outputredirect plugin.
            """
            return MultiLevelLogging.current_level

        @staticmethod
        def get_current_step(log_level):
            """Given a log level return the CURRENT step and index for
            the message being processed.
            Note: This function is used by the outputredirect plugin
            when processing messages from this API.
            """
            return MultiLevelLogging.current_step[index_from_level(
                log_level)], MultiLevelLogging.current_index

        @staticmethod
        def get_step_for_level(log_level):
            """Given a log level return the NEXT step and index.
            Note: This function is used by the outputredirect plugin
            when processing standard print function messages.
            """
            return get_next_step(log_level)

        @staticmethod
        def increment_level(increment=1):
            """Increment the current log level."""
            log_level = MultiLevelLogging.current_level + increment
            return set_current_level(log_level)

        @staticmethod
        def set_level(log_level):
            """Set the current log level."""
            return set_current_level(log_level)

    name = {"log": LogLevel,
            "redirect": Redirect}
    return name


def set_current_level(log_level):
    if log_level <= MIN_LEVEL:
        MultiLevelLogging.current_level = MIN_LEVEL + 1
    elif log_level > MAX_LEVEL:
        MultiLevelLogging.current_level = MAX_LEVEL
    else:
        MultiLevelLogging.current_level = log_level
    return MultiLevelLogging.current_level


def set_log_parameters(msg, log_level):
    """Prepend the string to print with the log level and step before
    printing.
    """
    if log_level is None:
        log_level = MultiLevelLogging.current_level
    set_current_level(log_level)
    step, index = get_next_step(log_level)
    MultiLevelLogging.log_level_set = True
    if MultiLevelLogging.output_redirect_enabled:
        # if the outputredirect plugin is installed and enabled
        print msg
    else:
        # Don't print index as it doesn't mean much in this situation
        # (not every message is given an index)
        print "{}-{} {}".format(log_level, step, msg)
    MultiLevelLogging.log_level_set = False


class MultiLevelLogging:
    # Keep track of the current log level and the step for each log
    # level.
    current_index = 0
    current_level = 1
    current_step = [0] * (MAX_LEVEL - MIN_LEVEL)
    log_level_set = False
    output_redirect_enabled = False


def get_next_step(log_level):
    # Return the next step and index for the specified log level.
    MultiLevelLogging.current_step[index_from_level(log_level)] += 1
    step = MultiLevelLogging.current_step[index_from_level(log_level)]
    reset_higher_levels(log_level)
    MultiLevelLogging.current_level = log_level
    MultiLevelLogging.current_index += 1
    return step, MultiLevelLogging.current_index


def index_from_level(log_level):
    # Return the current_step list index for the log level specified.
    return log_level - MIN_LEVEL - 1


def reset_level_step(log_level):
    # Reset the step for a log level to 0. Next time this level is
    # logged the step will be set to 1.
    MultiLevelLogging.current_step[index_from_level(log_level)] = 0


def reset_higher_levels(log_level):
    # Reset step to 0 for all log levels higher than specified.
    for level in range(log_level+1, MAX_LEVEL+1):
        reset_level_step(level)
