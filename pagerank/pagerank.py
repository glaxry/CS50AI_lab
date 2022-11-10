import os
import random
import re
import sys
import numpy as np
DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
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
    """
    
    if len(corpus[page]) == 0:
        prob_distribution = dict.fromkeys(corpus.keys(), 1/len(corpus))
    else:
        prob_distribution = dict.fromkeys(corpus.keys(), (1-damping_factor)/len(corpus))
        for p in corpus[page]:
            prob_distribution[p] += damping_factor/len(corpus[page])
    return prob_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    result = dict()
    for key in corpus:
    	result[key] = 0
    temp = list(corpus.keys())
    rand = random.randint(0, len(corpus) - 1)
    index = temp[rand]
    
    for i in range(0, n + 1):
    	result[index] += 1
    	transition = transition_model(corpus, index, damping_factor)
    	p = np.array(list(transition.values()))
    	index = np.random.choice(list(transition.keys()), p=p.ravel())
    	
    for key in result:
    	result[key] = result[key] / n
    return result
	

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
	
    numlinks = dict()
    result = dict()
    for key in corpus:
        numlinks[key] = len(corpus[key])
        result[key] = 1 / len(corpus)
    while 1:
        last_result = result.copy()
        for key in result:
        	x = sum([result[i] / numlinks[i] for i in result.keys() if key in corpus[i] and numlinks[i] > 0]) 
        	result[key] = (1 - damping_factor) / len(corpus) + damping_factor * x
        sum1 = 0
        for key in result:
            if abs(result[key] - last_result[key]) < 0.001:
                sum1 += 1
        if sum1 == len(result):
            break
    return result


if __name__ == "__main__":
    main()
