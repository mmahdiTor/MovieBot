def simple_encode(data: str) -> str:
    data = str(data)

    return (
        data.replace("_", "z")
        .replace("-", "y")
        .replace("1", "a")
        .replace("2", "b")
        .replace("3", "c")
        .replace("4", "d")
        .replace("5", "e")
        .replace("6", "f")
        .replace("7", "g")
        .replace("8", "h")
        .replace("9", "i")
        .replace("0", "j")
    )


def simple_decode(encoded: str):

    try:

        decoded = (
            encoded.replace("z", "_")
            .replace("y", "-")
            .replace("a", "1")
            .replace("b", "2")
            .replace("c", "3")
            .replace("d", "4")
            .replace("e", "5")
            .replace("f", "6")
            .replace("g", "7")
            .replace("h", "8")
            .replace("i", "9")
            .replace("j", "0")
        )

        return [int(i) for i in decoded.split("-")]

    except:
        return []