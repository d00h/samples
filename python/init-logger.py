
import logging
import sys

# some module

log1 = logging.getLogger("api.managers.payture.charge")


def method1():
    log1.info("start method1")
    log1.debug("debug method1")

# some module other module


log2 = logging.getLogger("api.managers.payture.refund")


def method2():
    log2.info("start method2")
    log2.debug("debug method2")

# some module other module


log3 = logging.getLogger("api.database")


def method3():
    log3.info("start database")
    log3.debug("debug database")


# main application

def configure_logging():
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(levelname)-8s: %(message)s"))

    file_handler = logging.FileHandler("file.log")
    file_handler.setFormatter(logging.Formatter("%(levelname)-8s: %(message)s"))

    logger = logging.getLogger("api.managers.payture")
    logger.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    logger = logging.getLogger("api.database")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def process():
    method1()
    method2()
    method3()


def main():
    configure_logging()
    process()


if __name__ == '__main__':
    main()
