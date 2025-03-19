import pandas as pd
import rdflib

def check_csv(left_side, right_side):
    left = pd.read_csv(left_side)
    right = pd.read_csv(right_side)
    left = left.reindex(sorted(left.columns), axis=1)
    right = right.reindex(sorted(right.columns), axis=1)
    left.sort_values(by=left.columns.tolist(), inplace=True)
    right.sort_values(by=right.columns.tolist(), inplace=True)
    left.reset_index(drop=True, inplace=True)
    right.reset_index(drop=True, inplace=True)
    for col in left.columns:
        if type(left[col][0]) != type(right[col][0]):
            right[col] = right[col].astype(type(left[col][0]))
    return left.equals(right)


print(check_csv('mushroom_cleaned.csv', 'mushroom_rdf.csv'))