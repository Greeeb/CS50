import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    
    """if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")"""
    for i in range(3):
        path = f"c:/Users/daniil.navodey/Documents/CS50/heredity/data/family{i}.csv"
        people = load_data(path)# sys.argv[1])

        # Keep track of gene and trait probabilities for each person
        probabilities = {
            person: {
                "gene": {
                    2: 0,
                    1: 0,
                    0: 0
                },
                "trait": {
                    True: 0,
                    False: 0
                }
            }
            for person in people
        }

        # Loop over all sets of people who might have the trait
        names = set(people)
        for have_trait in powerset(names):

            # Check if current set of people violates known information
            fails_evidence = any(
                (people[person]["trait"] is not None and
                people[person]["trait"] != (person in have_trait))
                for person in names
            )
            if fails_evidence:
                continue

            # Loop over all sets of people who might have the gene
            for one_gene in powerset(names):
                for two_genes in powerset(names - one_gene):

                    # Update probabilities with new joint probability
                    p = joint_probability(people, one_gene, two_genes, have_trait)
                    update(probabilities, one_gene, two_genes, have_trait, p)

        # Ensure probabilities sum to 1
        normalize(probabilities)

        # Print results
        for person in people:
            print(f"{person}:")
            for field in probabilities[person]:
                print(f"  {field.capitalize()}:")
                for value in probabilities[person][field]:
                    p = probabilities[person][field][value]
                    print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    p = []
    family = {"parents": {},
             "child": None}
    temp = None
    for x in people.keys():
        if people[x]["mother"] == None:
            family["parents"][x] = None
        else: temp = x
    family["child"] = temp
    # family = {"parents": {"first": None, "second": None}, "child": "third"}
    
    # parents
    for parent in family["parents"].keys():
        if (parent not in one_gene) and (parent not in two_genes):
            i = 0
        else:
            i = 1 if parent in one_gene else 2 
            
        trait = False if parent not in have_trait else True
        
        p.append(PROBS["gene"][i] * PROBS["trait"][i][trait])
        family["parents"][parent] = i
    
    # child
    child_name = family["child"]
    if (child_name not in one_gene) and (child_name not in two_genes):
        i = 0
    else:
        i = 1 if child_name in one_gene else 2 
            
    trait = False if parent not in have_trait else True
    
    probability = 0
    i1 = family["parents"][list(family["parents"].keys())[0]]
    i2 = family["parents"][list(family["parents"].keys())[1]]
    
    if i1==i2:
        if i==1:
            probability = (1-PROBS["mutation"])*PROBS["mutation"]*2 if i1!=1 else (1-PROBS["mutation"])*PROBS["mutation"]*0.25
        elif i==2:
            if i1==0:
                probability = PROBS["mutation"]**2
            else:
                probability = (1-PROBS["mutation"])**2*i1/2*i2/2
        else:
            if i1==0:
                probability = (1-PROBS["mutation"])**2
            else:
                probability = PROBS["mutation"]**2*i1/2*i2/2
    elif i1==0 or i2==0:
        if i!=1:
            probability = (1-PROBS["mutation"])*PROBS["mutation"]*(i1+i2)/2
        else:
            probability = (PROBS["mutation"]**2 + (1-PROBS["mutation"])**2)*(i1+i2)/2
    else:
        if i==0:
            probability = PROBS["mutation"]**2 * 0.5
        elif i==1:
            probability = (1-PROBS["mutation"])*PROBS["mutation"]
        else:
            probability = (1-PROBS["mutation"])**2 * 0.5
            
    
    probability = probability * PROBS["trait"][i][trait]
    
    p.append(probability)
    return p[0] * p[1] * p[2]
        


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities.keys():
        if (person not in one_gene) and (person not in two_genes):
            i = 0
        else:
            i = 1 if person in one_gene else 2 
            
        trait = False if person not in have_trait else True
        
        probabilities[person]["gene"][i] += p
        probabilities[person]["trait"][trait] += p

        


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    sum = 0
    for person in probabilities.keys():
        sum = probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + probabilities[person]["gene"][2]
        for i in range(3):
            probabilities[person]["gene"][i] = probabilities[person]["gene"][i]/sum
        
        sum = probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        probabilities[person]["trait"][True] = probabilities[person]["trait"][True]/sum
        probabilities[person]["trait"][False] = probabilities[person]["trait"][False]/sum
     
    return probabilities


if __name__ == "__main__":
    main()
