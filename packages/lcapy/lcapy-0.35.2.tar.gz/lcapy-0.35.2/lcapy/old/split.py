def split(s):  
    """Split a string by , except if in braces"""
    parts = []
    bracket_level = 0
    current = []
    for c in (s + ','):
        if c == ',' and bracket_level == 0:
            parts.append(''.join(current))
            current = []
        else:
            if c == '{':
                bracket_level += 1
            elif c == '}':
                bracket_level -= 1
            current.append(c)
    if bracket_level != 0:
        raise ValueError('Mismatched braces for ' + s)
    return parts
