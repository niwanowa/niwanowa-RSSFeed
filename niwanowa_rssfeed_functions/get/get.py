"""
get:
      summary: 'RSSFeedを取得するAPI'
      responses:
        '200':
          description: 'Successful response'
          content:
            application/xml:
              example: |
                <?xml version="1.0" encoding="UTF-8"?>
                <rss version="2.0">
                  <channel>
                    <title>Your RSS Feed</title>
                    <link>http://yourwebsite.com</link>
                    <description>Your feed description</description>
                  </channel>
                </rss>
      x-amazon-apigateway-integration:
        httpMethod: post
        type: aws_proxy
        uri:
          Fn::Sub: arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${GetRSSFeedFunction.Arn}/invocations
"""
import json
import boto3
import os

def lambda_handler(event, context):
    # S3クライアント作成
    s3 = boto3.client('s3')
    BUCKET_NAME = os.environ['BUCKET_NAME']

    # S3からrss.xmlを取得。
    # 対象ファイルがない場合はエラーを出力する
    try:
        response = s3.get_object(
            Bucket=BUCKET_NAME,
            Key='rss.xml'
        )
    except Exception as e:
        print(e)
        raise e
    
    # Lambdaプロキシ統合に対応したレスポンスを返す
    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/xml"
        },
        "body": response['Body'].read().decode('utf-8')
    }


    # response = {
    #     "statusCode": 200,
    #     "headers": {
    #         "Content-Type": "application/xml"
    #     },
    #     "body": """<?xml version="1.0" encoding="UTF-8"?>
    #         <rss version="2.0">
    #             <channel>
    #                 <title>Your RSS Feed</title>
    #                 <link>http://yourwebsite.com</link>
    #                 <description>Your feed description</description>
    #             </channel>
    #         </rss>"""
    # }

    return response
