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
        ## This data will be used for pie chart. We need domain wise number to display the top domains
        ## and this data is enough for that I guess.

        df = pd.read_excel ('templates/Data-with-domain.xlsx')
        data = []
        final_df = pd.DataFrame(data)
        final_df = df['Domain'].value_counts()
        #print(final_df)
        final_df = final_df.astype(str)
        result = {
            #reource type needs update
            'resource_type': 'train_outward_data_states',
            'results': json.loads(final_df.to_json())
        }
        print(result)
        dynamo_db.Table(table_name).put_item(
            Item=result
        )
    except Exception as e:
        print(e)

if __name__ == '__main__':
    lambda_handler("", "")