def fix_quotes(text: str) -> str:
    """
    将文本中的全角引号左右互换的问题修正.
    e.g.
        ”...“ -> “...”
    """
    lst = 0
    out = []

    while True:
        lq = min(text.find("“", lst), text.find("”", lst))
        if lq == -1:
            break
        rq = min(text.find("“", lq + 1), text.find("”", lq + 1))
        if rq == -1:
            break

        out.append(text[lst:lq])
        out.append("“")
        out.append(text[lq + 1:rq])
        out.append("”")

        lst = rq + 1

    out.append(text[lst:])

    return "".join(out)


def fix_quotes_file_inplace(filename: str):
    """
    在文件中就地进行 `fix_quotes`.
    """
    with open(filename) as f:
        text = f.read()
    text = fix_quotes(text)
    with open(filename, "w") as f:
        f.write(text)
