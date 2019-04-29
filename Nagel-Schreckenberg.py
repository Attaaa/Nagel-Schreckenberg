import numpy.random as random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from copy import copy, deepcopy
from operator import itemgetter

# initialize algorithm parameter
M = 100
p = 0.3
init_v = 0
N = 10
t_max = 100
v_max = 5

# initialize cars
random.seed(4)
roads = np.array( [ [[0,M+0.5], [3,3]], [[0,M+0.5], [7,7]] ] )
cars = np.array([[random.randint(1,M), 5] for i in range(1,N+1)])
cars = np.array(sorted(cars, key=itemgetter(0)))

# main program
v = init_v
all_car_movement = []
cars_order = [i for i in range(N)]
new_cars_order = []
print(cars_order)
for t in range(t_max):
    x_row = []
    for i in cars_order:
        car = cars[i]
        next_car = cars[i+1 if i+1 < N else 0]
        
        # v pertama
        v = np.min([v+1, v_max])
        
        # v kedua
        if (next_car[0] < car[0]):
            d = M - next_car[0]
        else: 
            d = (next_car[0]-car[0])
        v = np.min([v, d-1])

        # v ketiga
        prob = random.rand()
        if (prob < p):
            v = np.max([0, v-1])
        
        # update nilai x
        x = copy(car[0])
        x = x + v
        if (x >= M):
            temp = []
            for i in range(N):
                order = cars_order[i] + N-1
                if (order + N-1 > N):
                    order = order - N
                temp.append(order)
            cars_order = deepcopy(temp)
            x = x - M
        x_row.append(copy([x,car[1]]))

    cars = deepcopy(x_row)
    all_car_movement.append(deepcopy(x_row))

# animating
fig = plt.figure()
ax = plt.axes(ylim=(0,10), xlim=(0,M+0.5))
for road in roads:
    plt.plot(road[0], road[1], c="black")
car_marker = ax.scatter([], [], s=75, marker="s")

def animate(i):
    cars_position = all_car_movement[i]
    car_marker.set_offsets(cars_position)
    return car_marker

anim = animation.FuncAnimation(fig, animate, frames=len(all_car_movement), interval=50)
plt.show()