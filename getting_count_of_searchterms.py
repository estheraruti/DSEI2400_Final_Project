import pandas as pd
import numpy as np
import re


search_terms = ["Childhood", "cancer", "early", "diagnosis", "methods"]
def term_counts(df):
    for term in search_terms:
        df['term_count_' + term] = 0
        for index,row in df.iterrows():
            match = re.findall(term, row.iloc[1], re.IGNORECASE)
            count = len(match)
            df.loc[index,'term_count_' + term] = count
    return df

if __name__ == "__main__":
    term_counts