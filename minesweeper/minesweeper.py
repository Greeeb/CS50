import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if (len(self.cells) == self.count) and (self.count != 0):
            return self.cells
        return set()       

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if (self.count == 0) and (len(self.cells) > 0):
            return self.cells
        return set()  

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # print(self.cells, " - ", self.count)
        
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
            
        # print(self.cells, " - ", self.count)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # print(self.cells, " - ", self.count)
        if cell in self.cells:
            self.cells.remove(cell)
        
        # print(self.cells, " - ", self.count)

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        if cell not in self.mines:   
            self.mines.add(cell)
            for sentence in self.knowledge:
                sentence.mark_mine(cell)
            # print("Marked mine: ", cell)
            # print(" ")

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        if cell not in self.safes:
            self.safes.add(cell)
            for sentence in self.knowledge:
                sentence.mark_safe(cell)
            # print("Marked safe: ", cell)
            # print(" ")

    def nearby_cells(self, cell):
        nearby_cells = []
        for i in range(max(cell[0] - 1, 0), min(cell[0] + 2, self.height)):
            for j in range(max(cell[1] - 1, 0), min(cell[1] + 2, self.width)):
                if ((i, j) != cell) and ((i, j) not in self.mines) and ((i, j) not in self.safes):
                    nearby_cells.append((i,j))

        return nearby_cells

    def print_knowledge_base(self):
        print("Knowledge base:")
        for knowledge in self.knowledge:
            if knowledge.count != 0 and knowledge.cells != set():
                print(knowledge.cells, " - ", knowledge.count)
        print(" ")

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # mark the cell as a move that has been made    
        self.moves_made.add(cell)
        
        # mark the cell as safe
        self.mark_safe(cell)
        self.print_knowledge_base()
        
        # add a new sentence to the AI's knowledge base 
        # based on the value of `cell` and `count`
        nearby_cells = self.nearby_cells(cell)
        self.knowledge.append(Sentence(cells=nearby_cells, count=count))
                
        for knowledge in self.knowledge:
            if len(knowledge.cells) == knowledge.count and knowledge.count != 0:
                temp = copy.deepcopy(knowledge.cells)
                for cell in temp:
                    self.mark_mine(cell)
                    knowledge.mark_mine(cell)
            if knowledge.count == 0 and len(knowledge.cells) != 0:
                temp = copy.deepcopy(knowledge.cells)
                for cell in temp:
                    self.mark_safe(cell)
                    knowledge.mark_safe(cell)
                              
        # add any new sentences to the AI's knowledge base
        # if they can be inferred from existing knowledge
        
        if len(self.knowledge) > 1:
            temp = copy.deepcopy(self.knowledge)
            for knowledge in temp:
                for comparison in temp:
                    if comparison != knowledge and comparison.cells != set() and knowledge.cells != set() and knowledge.cells.issubset(comparison.cells):
                        print("knowledge: ", knowledge)
                        print("comparison: ", comparison)
                        for x in knowledge:
                            comparison.cells.remove(x)
                        self.knowledge.append(Sentence(cells=comparison.cells,
                                                       count=knowledge.count-comparison.count))
                        print("new: ", knowledge.cells-comparison.cells)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safes = list(self.safes) # [::-1]
        print(safes)
        for cell in safes:
            if cell not in self.moves_made:
                return cell
        return None
        
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        all_cells = list(itertools.product(range(8), repeat=2))
        if self.moves_made != []:
            for move in self.moves_made:
                all_cells.remove(move)
        if self.mines != []:
            for move in self.mines:
                all_cells.remove(move)
        return all_cells[random.randint(0, len(all_cells)-1)]
