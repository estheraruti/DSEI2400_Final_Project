import pandas as pd
import numpy as np
import re
import first_query_websearch
from first_query_websearch import df
import third_creating_df

def term_counts(df, query):
    for term in query:
        df['term_count_' + term] = 0
        for index, row in df.iterrows():
            match = re.findall(term, row.iloc[1], re.IGNORECASE)
            count = len(match)
            df.loc[index, 'term_count_' + term] = count
    return df

if __name__ == "__main__":
    query = input("Enter search query: ").strip()  # Strip leading/trailing whitespace
    if query:
        search_terms = [query]
        # Assuming you have your DataFrame df already defined
        df = term_counts(df, search_terms)
        print(df)  # Or do something else with the modified DataFrame
    else:
        print("No search query provided.")