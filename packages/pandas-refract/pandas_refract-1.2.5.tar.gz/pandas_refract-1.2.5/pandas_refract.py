import numpy as np


__title__ = "pandas-refract"
__version__ = "1.2.5"
__author__ = "Nicholas Lawrence"
__license__ = "MIT"
__copyright__ = "Copyright 2018-2019 Nicholas Lawrence"


def refract(df, conditional, reset_index=True):
    """

    Return pair of Dataframes split against Truthy and Falseyness of provided array. Option to reset index in place.

    / >>> data = {'temperature': ['high', 'low', 'low', 'high'],
                  'overcast': [True, False, True, False]
                  }

    / >>> df = pandas.DataFrame(data)

    / >>> hot_df, cold_df = refract(df, df.temperature == 'high')

    / >>> overcast_df, not_overcast_df = refract(df, df.overcast, reset_index=True)

    / >>> print(overcast_df.iloc[0], not_overcast_df.iloc[0])

    """
    conditional = np.asarray(conditional, bool)
    true_df = df[conditional]
    false_df = df[~conditional]

    if reset_index:
        true_df = true_df.reset_index(drop=True)
        false_df = false_df.reset_index(drop=True)

    return true_df, false_df


def disperse(df, label, reset_index=True):
    """

    Return dictionary where key is a unique value in given dataframe series and value is dataframe where given column is
    key value. Bad performance for columns with many unique values -- best performance on label-like columns. Will treat
    nulls and nones as the same label, assigning them to the None key in the returned dictionary.

    / >>> data = {'temperature': ['high', 'low', 'low', 'high', 'medium', 'medium'],
                  'overcast'   : [True, False, True, False, False, True]
                  }

    / >>> df = pd.DataFrame(data)

    / >>> prism = disperse(df, 'temperature')

    / >>> {'high':   temperature  overcast
                    0      high      True
                    1      high     False,

           'low':   temperature  overcast
                    0       low     False
                    1       low      True,

           'medium':   temperature  overcast
                    0    medium     False
                    1    medium      True
          }

    """
    notnulls, nulls = refract(df, df[label].notnull())
    unique_values = set(notnulls[label])

    prism = {}

    if reset_index:
        for val in unique_values:
            prism[val] = notnulls[notnulls[label] == val].reset_index(drop=True)
            
        if not nulls.empty:
            prism[None] = nulls.reset_index(drop=True)

    else:
        for val in unique_values:
            prism[val] = notnulls[notnulls[label] == val]
            
        if not nulls.empty:
            prism[None] = nulls

    return prism
