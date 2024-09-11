import logging


def setup_custom_logger(name: str) -> logging.Logger:
    """
    This function creates a custom logger which makes multiprocess debugging much easier.

    Args:
        name (str): the name of the logger.

    Returns:
        custom_logger (logging.Logger): the custom logger to monitor the system.
    """

    # Set a descriptive logger message.
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - Process:%(process)d - Thread:%(thread)d - %(message)s'
    )

    # Set the file handler with the logging format.
    handler = logging.FileHandler('./src/name_components.log')
    handler.setFormatter(formatter)

    # Generate the custom logger.
    custom_logger = logging.getLogger(name)
    custom_logger.setLevel(logging.DEBUG)
    custom_logger.addHandler(handler)

    return custom_logger


# Initialize logger.
logger = setup_custom_logger('my_script')
