'''
                                            column_types()

Returns pandas dataframe column names, column object pandas dtypes and column python data types

The `dtype` results from `pandas.Dataframe.info()` are outputs from `pandas.DataFrame.dtypes()` method.
The `dtypes()` method does not differentiate between string iterable python objects (strings, dictionaries, lists, tuples),
it classifies all them as objects data types, the `column_types()` function returns the dataframe column names,
column object pandas dtypes and column python data types

Author: Alex Ricciardi
'''
import pandas as pd

def column_types(df):
    '''
    Takes the argumnt:
        df, pandas DataFrame data type
    Returns:
         A Dataframe of the inputed DataFrame
            column names
            column object pandas dtypes
            column python data types
    '''
    # Stores df columns names and columns pandas dtypes
    column_n = df[df.columns].dtypes.to_frame().rename(columns={0:'pandas_dtype'})
    # Stores  df columns python data types
    # Uses row indexed `0` values
    column_n['python_type'] = [type(df.loc[0][col]).__name__ for col in df.columns]
    # Checks column_n `type` values for NoneType
    for col in column_n.index:
        if column_n.loc[col]['python_type'] == 'NoneType':
            # Seach df row with no NaN
            for i in range(len(df)):
                if df.loc[i][col] != None:
                    colunm_n.loc[col]['type'] = type(df.loc[i][col]).__name__
                    break
                    # If the df column is all NaN values, the function will return a 'NoneType' for that particular column
    df_column_names = column_n.reset_index().rename(columns={'index':'Columns'})
    return df_column_names