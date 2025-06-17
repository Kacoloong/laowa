data = open("right_res2_29.out", "r").read().replace("ASSERT( ", "").replace(" );", "").replace("\nInvalid.", "").split(
    "\n")

xv = []
xd = []
x = []
for i in range(45):
    temp_v = []
    temp_d = []
    temp = []
    for j in range(64):
        temp_v.append(0)
        temp_d.append(0)
        temp.append(0)
    xv.append(temp_v)
    xd.append(temp_d)
    x.append(temp)
yv = []
yd = []
y = []
for i in range(45):
    temp_v = []
    temp_d = []
    temp = []
    for j in range(64):
        temp_v.append(0)
        temp_d.append(0)
        temp.append(0)
    yv.append(temp_v)
    yd.append(temp_d)
    y.append(temp)


def handle(s):
    temp = s.replace("0b", "").split(" = ")
    index = temp[0].split("_")
    return index, temp[1]


for i in data:
    if "xv" in i and "mm" not in i:
        index, value = handle(i)
        xv[int(index[1])][int(index[2])] = value
    elif "xd" in i and "mm" not in i:
        index, value = handle(i)
        xd[int(index[1])][int(index[2])] = value
for i in range(len(xv)):
    for j in range(64):
        if xv[i][j] == "1" and xd[i][j] == "1":
            x[i][j] = "u"
        elif xv[i][j] == "0" and xd[i][j] == "0":
            x[i][j] = "0"
        elif xv[i][j] != xd[i][j]:
            x[i][j] = "n"
print("x differential")
for i in range(len(x)):
    temp = "%s\""%i
    for j in range(63, -1, -1):
        if x[i][j] == "0":
            temp += "="
        elif x[i][j] == "u":
            temp += "u"
        elif x[i][j] == "n":
            temp += "n"
    temp += "\","
    print(temp)


xv = []
xd = []
x = []
for i in range(45):
    temp_v = []
    temp_d = []
    temp = []
    for j in range(64):
        temp_v.append(0)
        temp_d.append(0)
        temp.append(0)
    xv.append(temp_v)
    xd.append(temp_d)
    x.append(temp)
yv = []
yd = []
y = []
for i in range(45):
    temp_v = []
    temp_d = []
    temp = []
    for j in range(64):
        temp_v.append(0)
        temp_d.append(0)
        temp.append(0)
    yv.append(temp_v)
    yd.append(temp_d)
    y.append(temp)


def handle(s):
    temp = s.replace("0b", "").split(" = ")
    index = temp[0].split("_")
    return index, temp[1]


for i in data:
    if "yv" in i and "mm" not in i :
        index, value = handle(i)
        xv[int(index[1])][int(index[2])] = value
    elif "yd" in i and "mm" not in i :
        index, value = handle(i)
        xd[int(index[1])][int(index[2])] = value
for i in range(len(xv)):
    for j in range(64):
        if xv[i][j] == "1" and xd[i][j] == "1":
            x[i][j] = "u"
        elif xv[i][j] == "0" and xd[i][j] == "0":
            x[i][j] = "0"
        elif xv[i][j] != xd[i][j]:
            x[i][j] = "n"
print("x differential")
for i in range(len(x)):
    temp = "%s\""%i
    for j in range(63, -1, -1):
        if x[i][j] == "0":
            temp += "="
        elif x[i][j] == "u":
            temp += "u"
        elif x[i][j] == "n":
            temp += "n"
    temp += "\","
    print(temp)




yv = []
yd = []
y = []
for i in range(45):
    temp_v = []
    temp_d = []
    temp = []
    for j in range(64):
        temp_v.append(0)
        temp_d.append(0)
        temp.append(0)
    yv.append(temp_v)
    yd.append(temp_d)
    y.append(temp)


def handle(s):
    temp = s.replace("0b", "").split(" = ")
    index = temp[0].split("_")
    return index, temp[1]


for i in data:
    if "wv" in i :
        index, value = handle(i)
        xv[int(index[1])][int(index[2])] = value
    elif "wd" in i:
        index, value = handle(i)
        xd[int(index[1])][int(index[2])] = value
for i in range(len(xv)):
    for j in range(64):
        if xv[i][j] == "1" and xd[i][j] == "1":
            x[i][j] = "u"
        elif xv[i][j] == "0" and xd[i][j] == "0":
            x[i][j] = "0"
        elif xv[i][j] != xd[i][j]:
            x[i][j] = "n"
print("x differential")
for i in range(len(x)):
    temp = "%s\""%i
    for j in range(63, -1, -1):
        if x[i][j] == "0":
            temp += "="
        elif x[i][j] == "u":
            temp += "u"
        elif x[i][j] == "n":
            temp += "n"
    temp += "\","
    print(temp)
