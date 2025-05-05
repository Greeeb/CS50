import os
import random
import re
import sys
from tracemalloc import start

DAMPING = 0.85
SAMPLES = 10000


def main():
    """if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")"""
    for i in range(3):
        corpus = crawl(fr"C:\Users\memen\THI\CS50\pagerank\corpus{i}")
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
                # print(corpus[page])
                # print(page_rank[goal_page])
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
    PageRank values should summ to 1.
    """
    global_page_rank = {}
    for key in corpus.keys():
        global_page_rank[key] = 0
    
    temp_page_rank = {}
    for i in range(n):
        if i == 0:
            page = list(corpus.keys())[random.randint(0, len(corpus.keys()) - 1)]
        else:
            page = random.choices(list(corpus.keys()), temp_page_rank.values())[0]
                    
        global_page_rank[page] += 1
        temp_page_rank = transition_model(corpus, page, damping_factor)
        
    for page in global_page_rank.keys():
        global_page_rank[page] = global_page_rank[page] / n
    
    return global_page_rank



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should summ to 1.
    """
    N = len(corpus)
    page_rank = {page: 1 / N for page in corpus}
    accuracy = 0.001 

    while True:
        new_rank = {}
        for page in corpus:
            total = 0
            for possible_page in corpus:
                links = corpus[possible_page]
                if not links:
                    total += page_rank[possible_page] / N
                elif page in links:
                    total += page_rank[possible_page] / len(links)

            new_rank[page] = (1 - damping_factor) / N + damping_factor * total

        if all(abs(new_rank[p] - page_rank[p]) < accuracy for p in page_rank):
            break

        page_rank = new_rank

    return page_rank



if __name__ == "__main__":
    main()
