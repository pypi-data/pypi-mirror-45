##################
Logging Extensions
##################

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

.. image:: https://img.shields.io/github/license/open-things/loggingex.svg
    :target: https://github.com/open-things/loggingex/blob/master/LICENSE

.. image:: https://travis-ci.com/open-things/loggingex.svg?branch=master
    :target: https://travis-ci.com/open-things/loggingex

.. image:: https://img.shields.io/pypi/v/loggingex.svg?color=green
    :target: https://pypi.org/project/loggingex/

.. image:: https://img.shields.io/pypi/pyversions/loggingex.svg
    :target: https://pypi.org/project/loggingex/

.. image:: https://img.shields.io/pypi/dm/loggingex.svg
    :target: https://pypi.org/project/loggingex/

Implements a few extensions for the standard python logging library.

Currently, this project lacks documentation. Sorry about that.


Logging Context Filter
======================

Logging Context Filter injects context variables into LogRecord objects as extra
fields.

Here's a usage example:

.. code-block:: python

    import logging
    import sys

    from loggingex.context import LoggingContextFilter, context

    log = logging.getLogger()


    def process_lines(lines):
        for index, line in enumerate(lines):
            line = line.strip()
            with context(current_line=index + 1):
                log.debug("processing line: %s", line)
                if not line:
                    log.error("empty line!")
                    continue
                log.info("processed line: %s", line)


    def process_files(filenames):
        log.debug("starting...")
        for filename in filenames:
            with context(current_file=filename):
                log.info("processing file: %s", filename)
                with open(filename, "r") as f:
                    process_lines(f)
                log.info("processed file: %s", filename)
        log.debug("work is complete!")


    if __name__ == "__main__":
        formatter = logging.Formatter(
            "%(current_file)s:%(current_line)s:%(levelname)s: %(message)s"
        )
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)
        handler.addFilter(LoggingContextFilter())  # it's that simple
        logging.basicConfig(handlers=[handler], level=logging.DEBUG)

        with context(current_file="-", current_line="-"):
            # The context above sets default value, so that the formatter does
            # not crash, when they are not defined.
            process_files(sys.argv[1:])
