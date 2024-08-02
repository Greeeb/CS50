import sys

from crossword import *
import copy

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.domains.keys():
            temp = copy.deepcopy(self.domains[variable])
            for value in temp:
                if len(value) != variable.length:
                    self.domains[variable].remove(value)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revision = False
        x_values = copy.deepcopy(self.domains[x])
        y_values = copy.deepcopy(self.domains[y])
        overlaps = self.crossword.overlaps[x, y]
        for x_value in x_values:
            for y_value in y_values:
                if overlaps != None:
                    (i,j) = overlaps
                    if x_value[i] != y_value[j]:
                        try:
                            self.domains[x].remove(x_value)
                        except:
                            pass
                        revision = True
        return revision
                
                
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
            arcs = list(self.crossword.overlaps.keys())
        
        for (x, y) in arcs:
            if self.revise(x, y):
                if len(self.domains[x]) == 0 or len(self.domains[y]) == 0:
                    return False
                for arc in [temp for temp in arcs if x not in temp]:
                    arcs.append(arc)
                    
        return True
                

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment.keys()) != len(self.domains.keys()):
            return False
        for variable in assignment.keys():
            if len(assignment[variable]) != 1:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        values = []
        for variable in assignment.keys():
            print(assignment[variable])
            if assignment[variable] in values:
                return False
            else:
                values.append(assignment[variable])
            
            if variable.length != assignment[variable]:
                return False
            
            temp = [
                self.crossword.overlaps[list(self.crossword.overlaps.keys())[i]] for i in range(len(list(self.crossword.overlaps.keys())))
                if variable in list(self.crossword.overlaps.keys())[i]
            ]
            for x in temp:
                (i, j) = self.crossword.overlaps[x]
                if x[0][i] != x[1][j]:
                    return False
            
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        neighbors = self.crossword.neighbors(var)
        constrains = {}
        for value in self.domains[var]:
            counter = 0
            for node in neighbors:
                (i, j) = [self.crossword.overlaps[x] for x in range(len(self.crossword.overlaps))
                          if self.crossword.overlaps[x] == (var, node) or self.crossword.overlaps[x] == (node, var)][0]
                if value[i] == node[j]:
                    print("constrain")
                    counter += 1
            constrains[value] = counter
            
        return list({k: v for k, v in sorted(constrains.items(), key=lambda item: item[1])}.keys())

        
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        result = ()
        for variable in self.domains.keys():
            if variable not in assignment.keys():
                if result == ():
                    result = (variable, len(self.domains[variable]))
                else:
                    if len(self.domains[variable]) < list(result)[1]:
                        result = (variable, len(self.domains[variable]))
                    elif len(self.domains[variable]) == list(result)[1]:
                        result = (variable, len(self.domains[variable])) if len(self.crossword.neighbors(variable))>len(self.crossword.neighbors(list(result)[0])) else result

        return list(result)[0]
                
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        while not self.assignment_complete(assignment):
            variable = self.select_unassigned_variable(assignment)
            
            
            
        return assignment if self.consistent(assignment) else None 

def main():

    """# Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")"""

    for i in range(3):
        for j in range(3):
            # Parse command-line arguments
            structure = rf"C:\Users\daniil.navodey\Documents\CS50\crossword\data\structure{i}.txt" # sys.argv[1]
            words = rf"C:\Users\daniil.navodey\Documents\CS50\crossword\data\words{j}.txt" # sys.argv[2]
            output = rf"C:\Users\daniil.navodey\Documents\CS50\crossword\structure-{i},words-{j}.png" # sys.argv[3] if len(sys.argv) == 4 else None

            # Generate crossword
            crossword = Crossword(structure, words)
            creator = CrosswordCreator(crossword)
            assignment = creator.solve()

            # Print result
            if assignment is None:
                print("No solution.")
            else:
                creator.print(assignment)
                if output:
                    creator.save(assignment, output)


if __name__ == "__main__":
    main()
