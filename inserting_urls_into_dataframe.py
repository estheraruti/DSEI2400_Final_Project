import pandas as pd

# initializing the lists to store the search engine name and url data
search_engines = []
urls = []


# defining the loop
def separate_url(x):
    for search_engine, url in x.items():
        search_engines.extend([search_engine] * len(url))
        urls.extend(url)


# create an empty df similar to database "search" table

    df_search = pd.DataFrame()

    df_search['search_engine'] = search_engines
    df_search['urls'] = urls
    return df_search

if __name__ == "__main__":
    separate_url