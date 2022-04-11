import copy
import numpy as np

class RubiksCube:
    def __init__(self):
        # self.cube

        self.cube = self.create_cube()

    def rotate(self,axis,pos):
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
        a = 0 if axis != 0 else pos
        b = 0 if axis != 1 else pos
        c = 0 if axis != 2 else pos

        A = (a,b,c)
        B = self.next_set(*A,axis)
        C = self.next_set(*B,axis)
        D = self.next_set(*C,axis)

        S = (A,B,C,D)

        # print(S)

        DSet = copy.deepcopy(self.cube[D[0]][D[1]][D[2]])
        # print("Deep copy: ",DSet)

        for i in range(3,0,-1): #3,2,1,0 #D,C,B,A
            # self.cube[S[i][0]] [S[i][1]] [S[i][2]] = rotate_face( self.cube[S[i-1][0]] [S[i-1][1]] [S[i-1][2]],axis)
            cell_change = (S[i][0], S[i][1], S[i][2])
            cell_from = (S[i-1][0], S[i-1][1], S[i-1][2])
            self.cube[cell_change[0]] [cell_change[1]] [cell_change[2]] = self.cube[cell_from[0]] [cell_from[1]] [cell_from[2]]
            self.cube[cell_change[0]] [cell_change[1]] [cell_change[2]] = self.rotate_face( self.cube[cell_change[0]] [cell_change[1]] [cell_change[2]],axis)

        self.cube[A[0]][A[1]][A[2]] =  DSet
        self.cube[A[0]][A[1]][A[2]] = self.rotate_face(self.cube[A[0]][A[1]][A[2]],axis)


        if axis == 0:
            a = pos
            b = 1
            c = 0
        elif axis == 1:
            a = 1
            b = pos
            c = 0
        elif axis == 2:
            a = 1
            b = 0
            c = pos

        A = (a,b,c)
        B = self.next_set(*A,axis)
        C = self.next_set(*B,axis)
        D = self.next_set(*C,axis)



        S = (A,B,C,D)

        DSet = copy.deepcopy(self.cube[D[0]][D[1]][D[2]])
        # print("Deep copy: ",DSet)

        for i in range(3,0,-1): #3,2,1,0 #D,C,B,A
            # self.cube[S[i][0]] [S[i][1]] [S[i][2]] = self.rotate_face( self.cube[S[i-1][0]] [S[i-1][1]] [S[i-1][2]],axis)
            cell_change = (S[i][0], S[i][1], S[i][2])
            cell_from = (S[i-1][0], S[i-1][1], S[i-1][2])
            self.cube[cell_change[0]] [cell_change[1]] [cell_change[2]] = self.cube[cell_from[0]] [cell_from[1]] [cell_from[2]]
            self.cube[cell_change[0]] [cell_change[1]] [cell_change[2]] = self.rotate_face( self.cube[cell_change[0]] [cell_change[1]] [cell_change[2]],axis)

        # self.cube[D[0]][D[1]][D[2]] = self.rotate_face(DSet,axis)
        self.cube[A[0]][A[1]][A[2]] =  DSet
        self.cube[A[0]][A[1]][A[2]] = self.rotate_face(self.cube[A[0]][A[1]][A[2]],axis)

    def display_cube(self):
        for layer in self.cube:
            print('\n\n',end='')
            for slice in layer:
                print('\n',end='')
                for cell in slice:
                    print(cell,end=' ')
        print()

    def compare(self,other,return_dict=False,display=False):
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
    def rotate_face(cell,axis):
        '''
        Rotates the face of the cell, enabling pieces
        to be in the same location but still be 
        differently placed
        '''
        # print("Rotate face:", cell,end=' : ')
        if axis == 0:
            cell = (cell[0],cell[2],cell[1])
        elif axis == 1:
            cell = (cell[2],cell[1],cell[0])
        elif axis == 2:
            cell = (cell[1],cell[0],cell[2])
        # print(cell)
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



