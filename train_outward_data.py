import pandas as pd
import json
import boto3
import os

dynamo_db = boto3.resource('dynamodb')
table_name = "_".join(
    [os.getenv('env', 'prod'), os.getenv("main_data_table_name","covid_main_data")]
)

def lambda_handler(event,context):
    try:
        df = pd.read_excel ('templates/output2.xlsx')
        data = []
        final_df = pd.DataFrame(data)
        final_df['source_state'] = df['source_state'].unique()
        for s in df['source_state'].unique():
            final_df.loc[(final_df['source_state'] == s), 'number_of_trains'] = df.loc[(
                df['source_state'] == s), 'number_of_trains'].sum()
        for s in df['source_state'].unique():
            final_df.loc[(final_df['source_state'] == s), 'number_of_passengers'] = df.loc[(
                df['source_state'] == s), 'number_of_passengers'].sum()
        # print(final_df)
        final_df.sort_values('number_of_passengers')
        final_df = final_df.astype(str)
        result = {
            'resource_type': 'train_outward_data_states',
            'results': json.loads(final_df.reset_index().to_json(orient='records'))
        }
        print(result) 
        dynamo_db.Table(table_name).put_item(
            Item=result
        )
    except Exception as e:
        print(e)

if __name__ == '__main__':
    lambda_handler("", "")