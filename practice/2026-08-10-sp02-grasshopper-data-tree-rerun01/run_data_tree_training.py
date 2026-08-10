"""
OLEANDER SP02 — Grasshopper-like Data Tree offline reproduction.
Run status: OFFLINE STRUCTURE ONLY. This is not a Rhino/Grasshopper .gh execution.
All geometry parameters are SIMULATED / EXERCISE ASSUMPTION.
"""

ZONES = 4
ITEMS = 6
DX = 2.4
DY = 3.6


def path(*idx):
    return "{" + ";".join(map(str, idx)) + "}"


def base():
    return {
        path(z): [
            {"zone": z, "item": i, "x": i * DX, "y": z * DY, "z": 0.0}
            for i in range(ITEMS)
        ]
        for z in range(ZONES)
    }


def graft(tree):
    return {
        path(int(p.strip("{}")), i): [item]
        for p, items in tree.items()
        for i, item in enumerate(items)
    }


def flatten(tree):
    return {path(0): [item for p in sorted(tree) for item in tree[p]]}


def transpose_by_item(tree):
    return {
        path(i): [tree[p][i] for p in sorted(tree) if i < len(tree[p])]
        for i in range(ITEMS)
    }


def summary(tree):
    return len(tree), sum(len(v) for v in tree.values()), {p: len(v) for p, v in tree.items()}


if __name__ == "__main__":
    b = base()
    g = graft(b)
    f = flatten(b)
    t = transpose_by_item(b)

    assert summary(b)[:2] == (4, 24)
    assert summary(g)[:2] == (24, 24)
    assert summary(f)[:2] == (1, 24)
    assert summary(t)[:2] == (6, 24)

    print("BASE", summary(b))
    print("GRAFT", summary(g))
    print("FLATTEN", summary(f))
    print("TRANSPOSE", summary(t))
