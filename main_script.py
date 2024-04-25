# This script will run all other scripts in order

import first_query_websearch
import second_ocr_url_clean
import third_creating_df
import fourth_query_searchterm_count



def main():
    first_query_websearch()
    second_ocr_url_clean()
    third_creating_df()
    fourth_query_searchterm_count()