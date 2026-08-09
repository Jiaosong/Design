# Offline structural specification. NOT executed inside Grasshopper.
# All values are exercise-only hypothetical parameters.

ZONES = 4
ITEMS_PER_ZONE = 6
DX = 2.4
DY = 3.6

# Grasshopper-like tree representation: path tuple -> ordered items.
tree = {
    (z,): [(z * DX, i * DY, 0.0) for i in range(ITEMS_PER_ZONE)]
    for z in range(ZONES)
}

def graft(src):
    return {(path[0], i): [item] for path, items in src.items() for i, item in enumerate(items)}

def flatten(src):
    ordered = [item for path in sorted(src) for item in src[path]]
    return {(0,): ordered}

def transpose_by_item(src):
    # Equivalent design intent to regrouping zone branches by item index.
    return {(i,): [src[(z,)][i] for z in range(ZONES)] for i in range(ITEMS_PER_ZONE)}

EXPECTED = {
    "base": {"branches": 4, "items_per_branch": [6, 6, 6, 6]},
    "graft": {"branches": 24, "items_per_branch": [1] * 24},
    "flatten": {"branches": 1, "items_per_branch": [24]},
    "transpose": {"branches": 6, "items_per_branch": [4] * 6},
}

if __name__ == "__main__":
    variants = {"base": tree, "graft": graft(tree), "flatten": flatten(tree), "transpose": transpose_by_item(tree)}
    for name, t in variants.items():
        counts = [len(t[p]) for p in sorted(t)]
        print(name, "branches=", len(t), "counts=", counts, "paths=", sorted(t))
