from rubiksCubeNext import RubiksCube
import numpy as np


def main():
    test4()

def test1():
    cube = RubiksCube()

    cube.display_cube()

    print(np.unique(np.array(cube.cube),return_counts=True))
    print('Rotate cube from bottom')
    # rotate(cube,2,2)
    cube.rotate(2,2)
    cube.display_cube()
    # display_cube(cube)
    # np.array(cube)
    print(np.unique(np.array(cube.cube),return_counts=True))

def test2():
    cube = RubiksCube()
    cube.rotate(2,2)
    cube.rotate(2,2)
    cube.rotate(2,2)
    cube.rotate(2,2)
    cube.display_cube()
    print(np.unique(np.array(cube.cube),return_counts=True))

def test3():
    cube = RubiksCube()
    for _ in range(105):
        cube.rotate(2,2)
        cube.rotate(0,2)
    # cube.rotate(0,2)
    # cube.rotate(0,2)
    # cube.rotate(0,2)
    # cube.rotate(0,2)
    expected = cube.create_cube()
    cube.compare(expected,display=True)


from termcolor import colored

def test4():
    cube = RubiksCube()
    cube2 = RubiksCube()
    i = 0
    while i == 0 or not cube.compare(cube2):
        if i % 2 == 0:
            cube.rotate(2,1)
        else:
            cube.rotate(0,2)
        i += 1
    print(i)
    pass

main()