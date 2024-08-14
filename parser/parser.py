import nltk # natural language took kit
import sys
import os

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "i" | "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> N V 
S -> NP V | N VP | NP VP | NP VP Conj NP VP | N VP Conj VP | N VP Conj N V | N VP Conj N VP
NP -> Det N | P Det N | Det N NP | NP P NP | P N | Det NP | Adj NP
NP -> NP NP | Det Adj N | P Det Adj N | P N | N P N | N P NP | NP Adv
VP -> V N | VP NP | V NP | VP N | Adv VP | V Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # # If filename specified, read sentence from file
    # if len(sys.argv) == 2:
    #     with open(sys.argv[1]) as f:
    #         s = f.read()

    # # Otherwise, get sentence as input
    # else:
    #     s = input("Sentence: ")
    for i in range (1,11):
        filename = os.path.join(os.path.abspath(os.curdir), fr"parser/sentences/{i}.txt")
        print(f"\n***** word -> {i} *****")

        # Convert input into list of words
        s = preprocess(open(filename).read())

        # Attempt to parse sentence
        try:
            trees = list(parser.parse(s))
        except ValueError as e:
            print(e)
            return
        if not trees:
            print("Could not parse sentence.")
            return

        # Print each tree with noun phrase chunks
        for tree in trees:
            tree.pretty_print()

            print("Noun Phrase Chunks")
            for np in np_chunk(tree):
                print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    print(sentence)
    result = sentence.split()

    # delete dot at the end of the sentennce
    result[-1] = result[-1][:-1]

    # lower every word
    result = [result[i].lower() for i in range(len(result))]  

    # temporarily save the result list to be able to edit it while traversing with temp
    temp = result
    for word in temp:
        for letter in word:
            # if the letter is an actual letter
            if letter in "qwertzuiopüasdfghjklöäyxcvbnm":
               break
            # remove the word if it doesnt consist of any letter
            elif letter == word[-1]:
                result.remove(word)
    
  
    print(result)

    return result


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    NP = []
    subtrees = tree.subtrees()

    # traverse through all the subtrees in the given tree
    for subtree in subtrees:
        # exclude the root, left only with subtrees
        if subtree != tree:
            # create a list of all labels of subtrees excluding root label
            subtrees_labels = [i.label().lower() for i in subtree.subtrees()][1:]

            # check if the root label is np and no nps are found in subtrees, return root
            if (subtree.label().lower() == "np") and ("np" not in subtrees_labels) and (len(subtrees_labels) > 1):
                NP.append(subtree)

    return NP



if __name__ == "__main__":
    main()
