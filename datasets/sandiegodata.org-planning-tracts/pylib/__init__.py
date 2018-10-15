
import re

def clean_currency(v):
    return re.sub(r'[\$\,]','',v)
    
def extract_county(resource, doc, env, *args, **kwargs):
    from geoid.acs import Tract
    
    r = doc.reference('census_planning_database') 

    state_id = int(resource.state)
    county_id = int(resource.county)

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
        
        if i == 0:
            yield ['geoid'] + list(row.keys())
        
        if  int(state) == state_id and  int(county) ==  county_id:
        
            for col in ['Med_House_Value_ACS_12_16', 'Med_House_Value_ACSMOE_12_16', 
                'Aggr_House_Value_ACS_12_16', 'Aggr_House_Value_ACSMOE_12_16',
                'avg_Agg_HH_INC_ACS_12_16', 'avg_Agg_HH_INC_ACSMOE_12_16', 
                'Med_HHD_Inc_ACS_12_16', 'Med_HHD_Inc_ACSMOE_12_16',
                'Aggregate_HH_INC_ACS_12_16', 'Aggregate_HH_INC_ACSMOE_12_16',
                'avg_Agg_House_Value_ACS_12_16','avg_Agg_House_Value_ACSMOE_12_16']:
                


                row[col] = clean_currency(row[col])

            tract = Tract(state, county, tract )
            yield [str(tract)] + list(row.values())
