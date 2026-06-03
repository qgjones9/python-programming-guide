# [text encoding](https://docs.python.org/3.14/glossary.html#term-text-encoding)

A string in Python is a sequence of Unicode code points (in range `U+0000`–`U+10FFFF`). To store or transfer a string, it needs to be serialized as a sequence of bytes.

Serializing a string into a sequence of bytes is known as “encoding”, and recreating the string from the sequence of bytes is known as “decoding”.

There are a variety of different text serialization [codecs](https://docs.python.org/3.14/library/codecs.html#standard-encodings), which are collectively referred to as “text encodings”.

