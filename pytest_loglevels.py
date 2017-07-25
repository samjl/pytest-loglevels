##
# @file pytest-loglevels.py
# @author Sam Lea (samjl) <samjlea@gmail.com>
# @created 12/07/17
# @brief pytest plugin loglevels - functions to assign and print a log
# level to test log messages.
# Current limitations: log level cannot be applied to standard print
# function.

MIN_LEVEL = 0
MAX_LEVEL = 5


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

    name = {"log": LogLevel}
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
    step = get_next_step(log_level)
    print "{}-{} {}".format(log_level, step, msg)


class MultiLevelLogging:
    # Keep track of the current log level and the step for each log
    # level.
    current_level = 1
    current_step = [0] * (MAX_LEVEL - MIN_LEVEL)


def get_next_step(log_level):
    # Return the next step for the specified log level.
    MultiLevelLogging.current_step[index_from_level(log_level)] += 1
    step = MultiLevelLogging.current_step[index_from_level(log_level)]
    reset_higher_levels(log_level)
    MultiLevelLogging.current_level = log_level
    return step


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
