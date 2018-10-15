""" Example pylib functions"""


def extract(resource, doc, env, *args, **kwargs):
    """ An example row generator function.

    Reference this function in a Metatab file as the value of a Datafile:

            Datafile: python:pylib#row_generator

    The function must yield rows, with the first being headers, and subsequenct rows being data.

    :param resource: The Datafile term being processed
    :param doc: The Metatab document that contains the term being processed
    :param args: Positional arguments passed to the generator
    :param kwargs: Keyword arguments passed to the generator
    :return:


    The env argument is a dict with these environmental keys:

    * CACHE_DIR
    * RESOURCE_NAME
    * RESOLVED_URL
    * WORKING_DIR
    * METATAB_DOC
    * METATAB_WORKING_DIR
    * METATAB_PACKAGE

    It also contains key/value pairs for all of the properties of the resource.

    """

    from operator import itemgetter
    from metapack.rowgenerator import PandasDataframeSource

    col_map = {
        'geoid': 'geoid',
         'land_area': 'land_area',
        'tot_population_acs_12_16': 'total_population',
        'pop_5_17_acs_12_16': 'population_5_17',
        'nh_white_alone_acs_12_16': 'population_nh_white',
        'college_acs_12_16': 'population_college_degree',
        'med_hhd_inc_acs_12_16': 'median_household_income',
        'aggregate_hh_inc_acs_12_16': 'aggregate_household_income',
        'avg_agg_hh_inc_acs_12_16': 'average_agg_household_income',
        'avg_agg_house_value_acs_12_16': 'average_agg_house_value'
        }
  

    pdb = doc.reference('source_pdb').dataframe()
    
    df = pdb[list(col_map.keys())].rename(columns=col_map)
    
    for row in PandasDataframeSource('<local>', df, None):
        yield row
    