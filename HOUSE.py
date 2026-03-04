h = 5          # wall height
w = 7          # front house width
d = 4          # back room depth

door_h = 2
door_w = 2

# front window settings
win_row = 1
win_w = 2

# -------- ROOF --------
for i in range(h):
    # front triangle roof
    print(" " * (h - i - 1) + "*", end="")
    if i > 0:
        print(" " * (2 * i - 1) + "*", end="")

    # roof connection
    print("*", end="")

    # back slanted roof
    if i == 0:
        print("*" * (w + d))
    elif i == h - 1:
        print(" " * (w + d - 1) + "*")
    else:
        print(" " * (w + d) + "*")

# -------- ROOF BASE --------
print("*" * (2 * h) + "*" * (w + d))

# -------- WALLS (FRONT WINDOW + BACK DOOR) --------
for i in range(h):
    # -------- FRONT WALL --------
    if i == win_row:
        print("*" +
              " " * ((2 * h - 2 - win_w) // 2) +
              "*" * win_w +
              " " * ((2 * h - 2 - win_w) // 2) +
              "*", end="")
    else:
        print("*" + " " * (2 * h - 2) + "*", end="")

    # -------- BACK WALL --------
    if i >= h - door_h:
        # door (UNCHANGED)
        print("*" +
              " " * ((w + d - door_w) // 2) +
              "*" * door_w +
              " " * ((w + d - door_w) // 2 - 1) +
              "*")
    else:
        print("*" + " " * (w + d - 2) + "*")

# -------- BASE --------
print("*" * (2 * h) + "*" * (w + d))