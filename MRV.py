import sys
from copy import deepcopy
import datetime

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt


# r is row
# c is column
# v is a variable

# variables(a list of 81 elements): one variable is a square
# ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9']

# constraints(a list of 27 elements): 9 rows, 9 columns and 9 boxes, each of them has 9 variables
#[['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'], ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9'], ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9'], ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9'], ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9'], ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9'], ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9'], ['I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9'], ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1'], ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'], ['A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'I3'], ['A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'I4'], ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'I5'], ['A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6', 'I6'], ['A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'I7'], ['A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'I8'], ['A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9', 'H9', 'I9'], ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'], ['A4', 'A5', 'A6', 'B4', 'B5', 'B6', 'C4', 'C5', 'C6'], ['A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9'], ['D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'F1', 'F2', 'F3'], ['D4', 'D5', 'D6', 'E4', 'E5', 'E6', 'F4', 'F5', 'F6'], ['D7', 'D8', 'D9', 'E7', 'E8', 'E9', 'F7', 'F8', 'F9'], ['G1', 'G2', 'G3', 'H1', 'H2', 'H3', 'I1', 'I2', 'I3'], ['G4', 'G5', 'G6', 'H4', 'H5', 'H6', 'I4', 'I5', 'I6'], ['G7', 'G8', 'G9', 'H7', 'H8', 'H9', 'I7', 'I8', 'I9']]

# peers(a dictionary of 81 elements): each variable has 20 peers
# {'I6': set(['I9', 'G6', 'G5', 'G4', 'F6', 'I8', 'I1', 'H6', 'I3', 'I2', 'I5', 'I4', 'H4', 'H5', 'B6', 'I7', 'A6', 'D6', 'E6', 'C6']), 'H9': set(['G7', 'I9', 'H8', 'D9', 'I8', 'H2', 'F9', 'H1', 'H6', 'H7', 'I7', 'G8', 'C9', 'E9', 'G9', 'H3', 'A9', 'H5', 'B9', 'H4']), ... }

#values(a dictionary of 81 elements): eaac3ch variable has its valid choices of values
# {'I6': '123456789', 'H9': '123456789', 'I2': '9', 'E8': '123456789', 'H3': '8', 'H7': '123456789', 'I7': '4', 'I4': '123456789', 'H5': '123456789', 'F9': '123456789', 'G7': '123456789',... }

#assignment(a dictionary of 81 elements): each variable is assigned a value
# {'B4': '6', 'H8': '1', 'I2': '9', 'F4': '1', 'I7': '4', 'F8': '3', 'D2': '5', 'H3': '8', 'G9': '8', 'G8': '6', 'A1': '8', 'E5': '4', 'H4': '5', 'B3': '3', 'D6': '7', 'C2': '7', 'E7': '7', 'E6': '5', 'C7': '2', 'C5': '9', 'G3': '1'}

rows = "ABCDEFGHI"
cols = "123456789"

class CSP:
    def __init__ (self, puzzle):
 
        self.puzzle  = puzzle
        self.variables = [r + c for r in rows for c in cols]
        
        self.assignment = {}
        self.values = self.get_values(puzzle)
       
        self.constraints = self.get_constraints()

        self.units = self.get_units()

        self.peers = self.get_peers()
        self.print_puzzle(self.assignment)
    
    def solved(self):
        return not any(len(self.values[var])!=1 for var in self.variables)
    
    def get_constraints(self):
        constraints = []
        for row in rows:
            row_constraint = []
            for col in cols:
                row_constraint.append(row + col)
            constraints.append(row_constraint)
        for col in cols:
            col_constraint = []
            for row in rows:
                col_constraint.append(row + col)
            constraints.append(col_constraint)
        for row in ('ABC','DEF','GHI'):
            for col in ('123','456','789'):
                box_constraint = []
                for r in row:
                    for c in col:
                        box_constraint.append(r + c)
                constraints.append(box_constraint)
        return constraints

        unitlist = ([cross(rows, c) for c in cols] +
                    [cross(r, cols) for r in rows] +
                    [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
        units = dict((s, [u for u in unitlist if s in u])
                     for s in squares)

    def get_units(self):
        units = {}
        for v in self.variables: 
            units[v] = []
            for c in self.constraints:
                if v in c:       
                    units[v].append(c)
        return units

    def get_peers(self):
        peers = {}
        for var in self.variables:
            peer = set()
            for constraint in self.constraints:
                if var in constraint:
                    peer = peer | set(constraint)
            peer = peer - set([var])
            peers[var] = peer    
        return peers

    def get_values(self, puzzle):
        i = 0
        j = 0
        values = dict()
        for var in self.variables:
            if puzzle[i][j] != 0:
                self.assignment[var] = str(puzzle[i][j])
                values[var] = str(puzzle[i][j])
            else:
                values[var] = "123456789"
            j += 1
            if (j >= 9):
                j = 0
                i += 1
        return values

    def print_values(self, values):
        for r in rows:
            line = ""
            for c in cols:
                val = values[r+c] 
                while len(val) < 12:
                    val += " "
                line += val
            print line
        print

    def print_puzzle(self, puzzle):
        for r in rows:
            for c in cols:
                if r+c in self.assignment.keys():
                    print self.assignment[r+c],
                else:
                    print "0",
                if c in "36":
                    print "|",
            print
            if r in "CF":
                print "----- + ----- + -----"
        print        

class Sudoku(object):
    def __init__(self, puzzle):
        self.puzzle = puzzle                # self.puzzle is a list of lists
        self.ans = deepcopy(puzzle)         # self.ans is a list of lists
        
        self.sudoku_csp = CSP(self.puzzle)  # model sudoku as CSP
        
        self.preprocess(self.sudoku_csp)    # reduce the domain of variables based on input puzzle

        self.visited = 0                    # count number of visited nodes

    def revise(self, csp, Xi, Xj):
        is_revised = False
        for x in csp.values[Xi]:
            if all (x == y for y in csp.values[Xj]):
                csp.values[Xi] = csp.values[Xi].replace(x, "")
                # print "remove", (Xi, x)
                is_revised = True
        return is_revised

    def preprocess(self, csp):
        assignment = csp.assignment
        for (var,value) in assignment.items():
            # print(var, value)
            inferences = self.forward_check(assignment, csp, var, value)
            # inferences = self.AC3(assignment, csp, var, value)
        # csp.print_values(csp.values)

    def is_consistent(self, var, value, assignment, csp):
        for peer in csp.peers[var]:
            if peer in assignment.keys() and assignment[peer]==value:
                return False
        return True

    def display(self, puzzle):
        for row in "ABCDEFGHI":
            line =""
            for col in "123456789":
                line += puzzle[row+col] + ' '
                if col in "36":
                    line += "| "
            print line
            if row in "CF":
                print "----- + ----- + -----"
    
    def get_ans(self, puzzle):
        x = 0
        y = 0
        for row in "ABCDEFGHI":
            for col in "123456789":
                self.ans[x][y] = puzzle[row+col]
                y += 1
            x += 1
            y = 0

    def is_complete(self, assignment):
        return len(assignment)==81

    def select_variables_noMRV(self, assignment, csp):
        for var in csp.values:
            if var not in assignment:
                return var

    def select_variables_MRV(self, assignment, csp):
        # unassigned_variables = dict((var, len(csp.values[var])) for var in csp.variables if var not in assignment)
        unassigned_variables = dict((var, len(csp.values[var])) for var in csp.values if var not in assignment)
        mrv = min(unassigned_variables, key=unassigned_variables.get)
        # print unassigned_variables
        # print "mrv", mrv, len(csp.values[mrv])
        return mrv

    def is_consistent(self, var, value, assignment, csp):
        for peer in csp.peers[var]:
            if peer in assignment.keys() and assignment[peer]==value:
                return False
        return True

    def forward_check(self, assignment, csp, var, value):
        for peer in csp.peers[var]:
            if peer not in assignment and value in csp.values[peer]:
                remaining = csp.values[peer] = csp.values[peer].replace(value, "")
                if len(remaining) == 0:
                    return False
                if len(remaining) == 1:
                    flag = self.forward_check(assignment, csp, peer, remaining)
                    if flag == False:
                        return False
                # unit test
                for u in csp.units[peer]:
                    dplaces = []
                    for v in u:
                        if value in csp.values[v]:
                            dplaces.append(v)
                    # print dplaces
                    if len(dplaces) == 0:
                        return False 
                    elif len(dplaces) == 1:
                        flag = self.forward_check(assignment, csp, dplaces[0], value)
                        if flag == False:
                            return False
        return True        

    def select_LCV(self, var, values_of_var, assignment, csp):
        if len(values_of_var) == 1:
            # print values_of_var
            return values_of_var[0]
        min_count = 30
        min_val = values_of_var[0]
        for val in values_of_var:
            count = 0
            for peer in csp.peers[var]:
                if peer not in assignment and val in csp.values[peer]:
                    count += 1
            if count < min_count:
                min_count = count
                min_val = val
            # print var, values_of_var, val, count
        # print "min_val", min_val
        return min_val        

    def backtrack(self, assignment, csp):
        # print "backtrack"
        if self.is_complete(assignment):
            return assignment
                                                
        var = self.select_variables_MRV(assignment, csp)        #MRV
        # var = self.select_variables_noMRV(assignment, csp)    #noMRV
        
        values = deepcopy(csp.values)
        
        values_of_var = csp.values[var]
        
        # for value in csp.values[var]:         #noLCV
        for i in range(len(values_of_var)):     #LCV
            value = self.select_LCV(var, values_of_var, assignment, csp) #LCV
            values_of_var = values_of_var.replace(value, "") #LCV
            self.visited += 1
            if self.is_consistent(var, value, assignment, csp):
                assignment[var] = value
                inferences = self.forward_check(assignment, csp, var, value)    #FC
                # inferences = self.AC3(assignment, csp, var, value)              #AC3
                if inferences:
                    result = self.backtrack(assignment, csp)
                    if result:
                        return result

                del assignment[var]
                csp.values.update(values)

        return False
            
    def backtracking_search(self, csp):
        return self.backtrack(deepcopy(csp.assignment), csp)

    def solve(self):
        start = datetime.datetime.now()    
        # solve the puzzle            
        self.puzzle = self.backtracking_search(self.sudoku_csp)
        end = datetime.datetime.now()

        if self.puzzle:
            self.display(self.puzzle) 
            self.get_ans(self.puzzle) 
            print("Number of visited nodes:" + str(self.visited))
            print("Time taken: " + str(end - start))  
        else:
            print "Failure"
        return self.ans

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0
    # start1 = datetime.datetime.now()  
    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()
    # end1 = datetime.datetime.now()  
    # print("Total time taken: " + str(end1 - start1))
    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
