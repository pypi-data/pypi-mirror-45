from __future__ import unicode_literals

import json
import logging.config
import datetime

# from logging import config
import sys


class GrayLogJSONFormatter(logging.Formatter):
    """
    Default keys:
    name            Name of the logger (logging channel)
    levelno         Numeric logging level for the message (DEBUG, INFO,
                        WARNING, ERROR, CRITICAL)
    levelname       Text logging level for the message ("DEBUG", "INFO",
                        "WARNING", "ERROR", "CRITICAL")
    pathname        Full pathname of the source file where the logging
                        call was issued (if available)
    filename        Filename portion of pathname
    module          Module (name portion of filename)
    lineno          Source line number where the logging call was issued
                        (if available)
    funcName        Function name
    created         Time when the LogRecord was created (time.time()
                        return value)
    asctime         Textual time when the LogRecord was created
    msecs           Millisecond portion of the creation time
    relativeCreated Time in milliseconds when the LogRecord was created,
                        relative to the time the logging module was loaded
                        (typically at application startup time)
    thread          Thread ID (if available)
    threadName      Thread name (if available)
    process         Process ID (if available)
    message         The result of record.getMessage(), computed just as
                        the record is emitted
    args            Passed arguments
    exc_text        Formatted traceback exception
    stack_info
    """
    default_keys = {
        'name', 'levelno', 'levelname',
        'pathname', 'filename', 'module', 'lineno', 'funcName',
        'created', 'asctime', 'msecs', 'relativeCreated',
        'thread', 'threadName', 'process',
        'message',
        'exc_text', 'stack_info',
    }

    def __init__(self, fmt=None, datefmt=None, style='%',
                 source=None, keys=None, encoder=None):
        assert source, 'Empty source. You must specify the source.'

        kwargs = {'fmt': fmt, 'datefmt': datefmt}
        if sys.version_info > (3, 2, 6):
            kwargs.update(style=style)

        super(GrayLogJSONFormatter, self).__init__(**kwargs)

        self.source = source
        self.keys = keys
        if encoder:
            self.encoder = logging.config._resolve(encoder)
        else:
            self.encoder = json.JSONEncoder

    def get_keys(self):
        return self.keys or self.default_keys

    def format(self, record):
        graylog_data = None
        if 'data' in record.__dict__:
            graylog_data = record.__dict__['data']

        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        if sys.version_info > (3, 2, 6):
            message = self.formatMessage(record)
        else:
            try:
                message = self._fmt % record.__dict__
            except UnicodeDecodeError:
                # Issue 25664. The logger name may be Unicode. Try again ...
                try:
                    record.__dict__ = {
                        k: v.decode('utf-8') if isinstance(v, bytes) else v
                        for k, v in record.__dict__.items()
                    }
                    fmt = (
                        self._fmt.decode('utf-8')
                        if isinstance(self._fmt, bytes) else self._fmt
                    )
                    message = fmt % record.__dict__
                except UnicodeDecodeError as exc:
                    raise exc

        data = {key: value for key, value in record.__dict__.items()
                if key in self.get_keys()}
        asctime = datetime.datetime.fromtimestamp(record.created).isoformat()
        data.update({
            'source': self.source,
            'asctime': asctime,
            'message': message,
            'data': graylog_data,
        })

        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

            data['exc_text'] = record.exc_text

        return json.dumps(data, cls=self.encoder)
