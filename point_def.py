import numpy as np


# 点A(ax, ay)から点B(bx, by)と点C(cx, cy)を比べて点Bの方が近くの時1を返す。その他0
def comp_point(ax, ay, bx, by, cx, cy):
    a = np.array((ax, ay))
    b = np.array((bx, by))
    c = np.array((cx, cy))
    if np.linalg.norm(a-b) < np.linalg.norm(a-c):
        return 1
    else:
        return 0
