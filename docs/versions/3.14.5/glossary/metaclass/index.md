# [metaclass](https://docs.python.org/3.14/glossary.html#term-metaclass)

The class of a class.  Class definitions create a class name, a class
dictionary, and a list of base classes.  The metaclass is responsible for
taking those three arguments and creating the class.  Most object oriented
programming languages provide a default implementation.  What makes Python
special is that it is possible to create custom metaclasses.  Most users
never need this tool, but when the need arises, metaclasses can provide
powerful, elegant solutions.  They have been used for logging attribute
access, adding thread-safety, tracking object creation, implementing
singletons, and many other tasks.

More information can be found in [Metaclasses](https://docs.python.org/3.14/reference/datamodel.html#metaclasses).
