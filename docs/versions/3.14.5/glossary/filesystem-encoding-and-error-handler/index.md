# [filesystem encoding and error handler](https://docs.python.org/3.14/glossary.html#term-filesystem-encoding-and-error-handler)

Encoding and error handler used by Python to decode bytes from the
operating system and encode Unicode to the operating system.

The filesystem encoding must guarantee to successfully decode all bytes
below 128. If the file system encoding fails to provide this guarantee,
API functions can raise [UnicodeError](https://docs.python.org/3.14/library/exceptions.html#UnicodeError).

The [sys.getfilesystemencoding()](https://docs.python.org/3.14/library/sys.html#sys.getfilesystemencoding) and
[sys.getfilesystemencodeerrors()](https://docs.python.org/3.14/library/sys.html#sys.getfilesystemencodeerrors) functions can be used to get the
filesystem encoding and error handler.

The [filesystem encoding and error handler](../filesystem-encoding-and-error-handler/index.md) are configured at
Python startup by the [PyConfig_Read()](https://docs.python.org/3.14/c-api/init_config.html#c.PyConfig_Read) function: see
[filesystem_encoding](https://docs.python.org/3.14/c-api/init_config.html#c.PyConfig.filesystem_encoding) and
[filesystem_errors](https://docs.python.org/3.14/c-api/init_config.html#c.PyConfig.filesystem_errors) members of [PyConfig](https://docs.python.org/3.14/c-api/init_config.html#c.PyConfig).

See also the [locale encoding](../locale-encoding/index.md).
