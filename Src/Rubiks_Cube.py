import copy
import numpy as np

DEBUG = 2



class RubiksCube:
    def __init__(self):
        # self.cube

        self.cube = self.create_cube()

    def rotate(self,axis,pos,numRotations=1,clockwise=True):
        '''
        Rotate a section, axis determines which axis the face
        will be turned about, pos determines which layer
        pf the cube is turned that is perpendicular to 
        axis. 0 axis = up/down, 1 axis = forward/back,
        2 axis = left/right
        Ex.
        self.rotate(0,2) will rotate around the up/down axis
        and will rotate the top layer.
        
        Currently only rotates in a clockwise manner
            looking from up, front, or right depending
            on axis. 
        '''

        # fix numRotations to be how everything should change to
        numRotations %= 4
        if numRotations == 0:
            return
        if not clockwise:
            numRotations = 4 - numRotations

        # (a,b,c) is a position of a corner
        a = 0 if axis != 0 else pos
        b = 0 if axis != 1 else pos
        c = 0 if axis != 2 else pos

        # rotate all necessary corner pieces
        self._rotate(self.cube,a,b,c,axis,numRotations,clockwise)

        # (a,b,c) is a position of a middle edge
        a = pos if axis == 0 else 1
        b = 1 if axis == 0 else pos if axis == 1 else 0
        c = pos if axis == 2 else 0

        # rotate all necessary middle edge pieces
        self._rotate(self.cube,a,b,c,axis,numRotations,clockwise)

    @staticmethod
    def _swap(cube,pairings):
        '''
        Swap cells in cube, 
        value of key goes to value of value
        in otherwords: pairing = {from:to}
        '''
        deepcopies = {pair:copy.deepcopy(cube[pair[0]][pair[1]][pair[2]]) for pair in pairings.keys()}
        for frm,(toa,tob,toc) in pairings.items():
            cube[toa][tob][toc] = deepcopies[frm]

    def _rotate(self,cube,a,b,c,axis,numRotations=1,clockwise=True):
        '''
        Rotate all elements in cube, uses a,b,c to specify
        one specific cell to be rotated, others are generated
        from it
        '''
        A = (a,b,c)
        B = self.next_set(*A,axis)
        C = self.next_set(*B,axis)
        D = self.next_set(*C,axis)
        S = (A,B,C,D)

        pairings = {S[i]:S[(i+numRotations)%4] for i in range(4)}

        self._swap(self.cube,pairings)
        for i,j,k in S:
            self.cube[i][j][k] = self.rotate_face(self.cube[i][j][k],axis,numRotations)
        return


    def display_cube(self):
        '''
        Textually display cube, displays each layer,
        first layer printed is bottom layer of cube
        first line in printed layer is on face closest
        to user. First characters in line are leftern 
        cells in cube.
        '''
        for layer in self.cube:
            print('\n\n',end='')
            for slice in layer:
                print('\n',end='')
                for cell in slice:
                    print(cell,end=' ')
        print()

    def compare(self,other,return_dict=False,display=False):
        '''
        Compare 2 cubes, other is other cube.
        other can be a cube like self.cube or it can
        be of class RubiksCube 
        '''
        if type(other) is RubiksCube:
            return compare(other.cube,self.cube,return_dict,display)
        else:
            return compare(other,self.cube,return_dict,display)

    @staticmethod
    def create_cube():
        '''
        Creates a cube, already solved, and returns it
        '''
        cube = np.zeros((3,3,3),int).tolist()

        cube[0][1][1]  = (0,-1,-1)
        cube[1][0][1]  = (-1,1,-1)
        cube[1][1][0]  = (-1,-1,2)
        cube[1][1][2]  = (-1,-1,3)
        cube[1][2][1]  = (-1,4,-1)
        cube[2][1][1]  = (5,-1,-1)

        cube[0][0][1]  = (0,1,-1)
        cube[0][1][0]  = (0,-1,2)
        cube[0][1][2]  = (0,-1,3)
        cube[0][2][1]  = (0,4,-1)

        cube[1][0][0]  = (-1,1,2)
        cube[1][0][2]  = (-1,1,3)
        cube[1][2][0]  = (-1,4,2)
        cube[1][2][2]  = (-1,4,3)

        cube[2][0][1]  = (5,1,-1)
        cube[2][1][0]  = (5,-1,2)
        cube[2][1][2]  = (5,-1,3)
        cube[2][2][1]  = (5,4,-1)


        cube[0][0][0] = (0,1,2)
        cube[0][0][2] = (0,1,3)
        cube[0][2][0] = (0,4,2)
        cube[0][2][2] = (0,4,3)

        cube[2][0][0] = (5,1,2)
        cube[2][0][2] = (5,1,3)
        cube[2][2][0] = (5,4,2)
        cube[2][2][2] = (5,4,3)

        cube[1][1][1] = (-1,-1,-1)
        return cube

    @staticmethod
    def next_set(a,b,c,axis):
        '''
        Gets the next set of indices from previous set,
        with respect to the given axis
        '''
        a,b,c = a-1,b-1,c-1
        if axis == 0:
            a,b,c = a,-c,b
        elif axis == 1:
            a,b,c = -c,b,a
        elif axis == 2:
            a,b,c = -b,a,c
        else:
            raise Exception("Should not be here")
        # return a,b,c
        return a+1,b+1,c+1

    @staticmethod
    def rotate_face(cell,axis,numRotations=1):
        '''
        Rotates the face of the cell, enabling pieces
        to be in the same location but still be 
        differently placed
        '''
        if DEBUG == 1:
            print("Rotate face:", cell,end=' : ')
        if numRotations % 2 == 1:
            if axis == 0:
                cell = (cell[0],cell[2],cell[1])
            elif axis == 1:
                cell = (cell[2],cell[1],cell[0])
            elif axis == 2:
                cell = (cell[1],cell[0],cell[2])
        if DEBUG == 1:
            print(cell)
        return cell
    
def compare(expected,tested,return_dict=False,display=False):
    same = True
    differences = {}
    if display:
        print()
    for layer in range(3):
        for slice in range(3):
            for cell in range(3):
                if expected[layer][slice][cell] != tested[layer][slice][cell]:
                    same = False
                    if return_dict:
                        differences[(layer,slice,cell)] = (expected[layer][slice][cell],tested[layer][slice][cell])
                    if display:
                        print(f'({layer},{slice},{cell}): Expected: {str(expected[layer][slice][cell])} Actual: {str(tested[layer][slice][cell])}')
                    if not return_dict and not display:
                        return False
    if return_dict:
        return differences
    else:
        return same


class UIRubiksCube(RubiksCube):
    def __init__(self):
        super().__init__()
        self.faces = ('Y','R','G','B','O','W',' ')
    
    def display_face(self,axis,pos):
        if axis == 0:
            for column in self.cube[pos][::1 if pos == 0 else -1]:
                for cell in column:
                    print(self.faces[cell[0]],end='')
                print()
        elif axis == 1:
            for layer in self.cube[::-1]:
                for cell in layer[pos][::-1 if pos == 2 else 1]:
                    print(self.faces[cell[1]],end='')
                print()
        elif axis == 2:
            for layer in self.cube[::-1]:
                for column in layer[::-1 if pos==0 else 1]:
                    print(self.faces[column[pos][2]],end='')
                print()

    def display_cube(self):
        '''
        Textually display cube, displays each layer,
        first layer printed is bottom layer of cube
        first line in printed layer is on face closest
        to user. First characters in line are leftern 
        cells in cube.
        '''
        for layer in self.cube:
            print(10*'_')
            # print('\n\n',end='')
            for slice in layer:
                print('\n',end='')
                for cell in slice:
                    print(cell,end=' ')
        print()
    
    def display_all(self):
        print("Front")
        self.display_face(1,0)
        print("\nBack")
        self.display_face(1,2)
        print("\nLeft")
        self.display_face(2,0)
        print("\nRight")
        self.display_face(2,2)
        print("\nTop")
        self.display_face(0,2)
        print("\nBottom")
        self.display_face(0,0)








def create_cube():
    cube = np.zeros((3,3,3),int).tolist()

    cube[0][1][1]  = (0,-1,-1)
    cube[1][0][1]  = (-1,1,-1)
    cube[1][1][0]  = (-1,-1,2)
    cube[1][1][2]  = (-1,-1,3)
    cube[1][2][1]  = (-1,4,-1)
    cube[2][1][1]  = (5,-1,-1)

    cube[0][0][1]  = (0,1,-1)
    cube[0][1][0]  = (0,-1,2)
    cube[0][1][2]  = (0,-1,3)
    cube[0][2][1]  = (0,4,-1)

    cube[1][0][0]  = (-1,1,2)
    cube[1][0][2]  = (-1,1,3)
    cube[1][2][0]  = (-1,4,2)
    cube[1][2][2]  = (-1,4,3)

    cube[2][0][1]  = (5,1,-1)
    cube[2][1][0]  = (5,-1,2)
    cube[2][1][2]  = (5,-1,3)
    cube[2][2][1]  = (5,4,-1)


    cube[0][0][0] = (0,1,2)
    cube[0][0][2] = (0,1,3)
    cube[0][2][0] = (0,4,2)
    cube[0][2][2] = (0,4,3)

    cube[2][0][0] = (5,1,2)
    cube[2][0][2] = (5,1,3)
    cube[2][2][0] = (5,4,2)
    cube[2][2][2] = (5,4,3)

    cube[1][1][1] = (-1,-1,-1)
    return cube



