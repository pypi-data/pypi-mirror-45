def dot3(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def norm3(a):
    return (a[0] ** 2 + a[1] ** 2 + a[2] ** 2) ** 0.5


def sign3(a, b):
    return 1 if dot3(a, b) > 0 else (-1 if dot3(a, b) < 0 else 0)


def ptOnPlane(pt, origin, normal):
    t = dot3([pt[i] - origin[i] for i in range(3)], normal)
    return [pt[i] - t * normal[i] for i in range(3)]


def vtOnPlane(vt, normal):
    n2 = dot3(normal, normal)
    n2 = n2 if n2 != 0 else 1
    t = dot3(vt, normal)
    return [vt[i] - t * normal[i] / n2 for i in range(3)]


def vtOnVector(vt, vector):
    dot = dot3(vector, vector)
    if dot == 0:
        return [0, 0, 0]

    dot = dot3(vt, vector) / dot
    return [dot * vector[i] for i in range(3)]


def vtNormalized(vt):
    return [_ / (vt[0] ** 2 + vt[1] ** 2 + vt[2] ** 2) ** 0.5 for _ in vt]
