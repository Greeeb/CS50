import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    """if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")"""
    corpus = crawl("c:/Users/daniil.navodey/Documents/CS50/pagerank/corpus0")
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    
    
    :param corpus: dict {"page name": set(pages linked to by that page)}
    :param page: string "page name" of the current page
    :param damping_factor: float of dumping factor
    
    :return: dict {"page name": float probability of choosing this page}
    """
    page_rank = {}
    
    for goal_page in corpus.keys():
        if corpus[page] != set():
            if goal_page in corpus[page]:
                page_rank[goal_page] = damping_factor / len(corpus[page]) + (1 - damping_factor) / len(corpus)
                #print("avg")
            else:
                page_rank[goal_page] = (1 - damping_factor) / len(corpus)
                #print("random")
        else:
            page_rank[goal_page] = (1 - damping_factor) / len(corpus)
            #print("empty set")

    return page_rank
    
    
def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    global_page_rank = {}
    temp_page_rank = {}
    for i in range(n):
        if i == 0:
            page = list(corpus.keys())[random.randint(0, len(corpus.keys()) - 1)]
        else:
            page = max(temp_page_rank, key=temp_page_rank.get)
        temp_page_rank = transition_model(corpus, page, damping_factor)
        for temp in temp_page_rank.keys():
            if temp in global_page_rank.keys():
                global_page_rank[temp] = temp_page_rank[temp] + global_page_rank[temp]
            else:
                global_page_rank[temp] = temp_page_rank[temp]
    for page in global_page_rank.keys():
        global_page_rank[page] = global_page_rank[page] / n
    
    return global_page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    global_page_rank = {}
    N = len(corpus)
    accuracy = 1 / N
    
    for key in corpus.keys():
        global_page_rank[key] = 1 / N
    
    while accuracy > 0.001:
        if accuracy == 1/N:
            page = list(corpus.keys())[random.randint(0, len(corpus.keys()) - 1)]
        else:
            page = max(temp_page_rank, key=temp_page_rank.get)
            
        temp_page_rank = transition_model(corpus, page, damping_factor)
        print(temp_page_rank)
        accuracy_list = []
        for temp in temp_page_rank.keys():
            accuracy_list.append(min(abs(global_page_rank[temp] - temp_page_rank[temp]), accuracy))
            accuracy = max(accuracy_list)
            global_page_rank[temp] = temp_page_rank[temp]
            print(temp, accuracy)
    
    return global_page_rank


if __name__ == "__main__":
    main()
