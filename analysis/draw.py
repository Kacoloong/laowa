import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 定义每个小立方体的顶点
def cuboid_data(o, size=(1,1,1)):
    X = [[0, 0, 1, 1, 0, 0, 1, 1],
         [0, 1, 1, 0, 0, 1, 1, 0],
         [0, 1, 1, 0, 0, 1, 1, 0]]
    X = np.array(X)
    for i in range(3):
        X[i] = X[i] * size[i] + o[i]
    return X

def plot_cube(positions, size=(1,1,1), ax=None):
    for p in positions:
        X = cuboid_data(p, size)
        ax.plot_wireframe(X[0], X[1], X[2], color="black")
        r = [-0.5,0.5]
        for s, e in combinations(np.array(list(product(r,r,r))), 2):
            if np.sum(np.abs(s-e)) == r[1]-r[0]:
                s = s*size/2 + p
                e = e*size/2 + p
                ax.plot3D(*zip(s,e), color="black")

# 生成4x4x8立方体的所有小正方体的位置
positions = [(x,y,z) for x in range(4) for y in range(4) for z in range(8)]

# 绘制小正方体
plot_cube(positions, size=(1,1,1), ax=ax)

# 在每个小正方体上标注数字
for idx, pos in enumerate(positions):
    ax.text(pos[0]+0.5, pos[1]+0.5, pos[2]+0.5, str(idx), color="red")

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
