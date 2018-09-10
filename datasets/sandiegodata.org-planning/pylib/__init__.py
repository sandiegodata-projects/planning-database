
import re

def clean_currency(v):
    return re.sub(r'[\$\,]','',v)
    
def extract_sandiego(resource, doc, env, *args, **kwargs):
    from geoid.acs import Tract
    
    r = doc.reference('census_planning_database') 

    for i, row in enumerate(r.iterdict):
        
        
        state = row['State']
        county = row['County']
        tract = row['Tract']
        
        del row['GIDTR']
        del row['State']
        del row['County']
        del row['State_name']
        del row['County_name']
        del row['Tract']
        del row['Num_BGs_in_Tract']
        
        row['Med_House_Value_ACS_12_16'] = clean_currency('Med_House_Value_ACS_12_16')
        row['Med_House_Value_ACSMOE_12_16'] = clean_currency('Med_House_Value_ACSMOE_12_16')
        row['Aggr_House_Value_ACS_12_16'] = clean_currency('Aggr_House_Value_ACS_12_16')
        row['Aggr_House_Value_ACSMOE_12_16'] = clean_currency('Aggr_House_Value_ACSMOE_12_16')
        row['Avg_Agg_HH_INC_ACS_12_16'] = clean_currency('Avg_Agg_HH_INC_ACS_12_16')
        row['Avg_Agg_HH_INC_ACSMOE_12_16'] = clean_currency('Avg_Agg_HH_INC_ACSMOE_12_16')
        
        if i == 0:
            yield ['geoid'] + list(row.keys())
        elif  state == '06' and  county == '073':
            tract = Tract(state, county, tract )
            yield [str(tract)] + list(row.values())
