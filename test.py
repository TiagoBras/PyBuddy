a = {
        'a': {
            'A': ['x', 1],
            'B': ['y', 2]
        },
        'b': {
            'C': ['z', 3],
            'D': ['HOME', 4]
        }
}

for k, v in  a.items():
    for k1, v2 in v.items():
        print("%s: {%s: [%s, %d]}" % (k, k1, v2[0], v2[1]))

