from googlesearch import search 

def google_search(query):
    return search(query, num=5, stop=5)
    