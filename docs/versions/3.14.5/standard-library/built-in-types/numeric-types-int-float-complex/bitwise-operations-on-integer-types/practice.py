"""
Bitwise operations practice — fill in the TODOs and run:

    python practice.py

Each function maps to a pattern from index.md. All tests run when you execute
this file directly.
"""

READ, WRITE, EXECUTE = 4, 2, 1


def grant(flags: int, mask: int) -> int:
    """Turn on every bit set in mask."""
    return flags | mask 


def revoke(flags: int, mask: int) -> int:
    """Turn off every bit set in mask."""
    return flags & ~mask 


def has(flags: int, mask: int) -> bool:
    """True when all bits in mask are set in flags."""
    # TODO: test whether mask bits are present
    raise NotImplementedError


def toggle(flags: int, mask: int) -> int:
    """Flip every bit that is set in mask."""
    # TODO: XOR mask into flags
    raise NotImplementedError


def one_hot(bit: int) -> int:
    """Return an int with only bit `bit` set (0-based)."""
    # TODO: build a one-hot mask
    raise NotImplementedError


def pack_rgb(red: int, green: int, blue: int) -> int:
    """Pack three 0–255 byte values into 0xRRGGBB."""
    # TODO: shift and OR the three bytes
    raise NotImplementedError


def high_byte(word: int) -> int:
    """Return the high byte of a 16-bit value."""
    # TODO: shift right by one byte
    raise NotImplementedError


def low_byte(word: int) -> int:
    """Return the low byte of a 16-bit value."""
    # TODO: mask the bottom 8 bits
    raise NotImplementedError


def _run_checks() -> None:
    flags = READ
    flags = grant(flags, WRITE)
    assert flags == (READ | WRITE)

    flags = READ | WRITE | EXECUTE
    flags = revoke(flags, WRITE)
    assert flags == (READ | EXECUTE)
    assert not has(flags, WRITE)
    assert has(flags, READ)

    flags = READ | EXECUTE
    flags = toggle(flags, WRITE)
    assert flags == (READ | WRITE | EXECUTE)

    assert one_hot(5) == 32
    assert one_hot(0) == 1

    color = pack_rgb(0x3A, 0x7F, 0x2C)
    assert color == 0x3A7F2C

    word = 0x12_34
    assert high_byte(word) == 0x12
    assert low_byte(word) == 0x34


if __name__ == "__main__":
    _run_checks()
    print("All practice checks passed.")
