def parse_inline_text(text):
    blocks = text.split(", ")
    balance = []
    for block in blocks:
        parts = list(map(str.strip, block.split(" ")))
        if len(parts) == 2:
            balance.append((parts[0], float(parts[1])))
    return balance
