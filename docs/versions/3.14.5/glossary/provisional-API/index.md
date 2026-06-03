# [provisional API](https://docs.python.org/3.14/glossary.html#term-provisional-API)

A provisional API is one which has been deliberately excluded from the standard library’s backwards compatibility guarantees.  While major changes to such interfaces are not expected, as long as they are marked provisional, backwards incompatible changes (up to and including removal of the interface) may occur if deemed necessary by core developers.  Such changes will not be made gratuitously – they will occur only if serious fundamental flaws are uncovered that were missed prior to the inclusion of the API.

Even for provisional APIs, backwards incompatible changes are seen as a “solution of last resort” - every attempt will still be made to find a backwards compatible resolution to any identified problems.

This process allows the standard library to continue to evolve over time, without locking in problematic design errors for extended periods of time.  See [PEP 411](https://peps.python.org/pep-0411/) for more details.

