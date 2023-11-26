"""
/reset:
    get:
      summary: 'RSSFeedをリセット(初回生成)するAPI'
      responses:
        '200':
          description: 'Initialized RSSFeed'
      x-amazon-apigateway-integration:
        httpMethod: post
        type: aws_proxy
        uri:
          Fn::Sub: arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${ResetRSSFeedFunction.Arn}/invocations
"""
import json
import boto3
import os

def lambda_handler(event, context):
    # S3クライアント作成
    s3 = boto3.client('s3')
    BUCKET_NAME = os.environ['BUCKET_NAME']

    # S3のrss.xmlを固定ファイルで置換する。
    s3.put_object(
        Bucket=BUCKET_NAME,
        Body="""<?xml version="1.0" encoding="UTF-8"?>
            <rss version="2.0">
                <channel>
                    <title>にわのわのRSS</title>
                    <link>http://yourwebsite.com</link>
                    <description>Your feed description</description>
                </channel>
            </rss>""",
        Key='rss.xml',
        ContentType='application/xml'
    )

    # Lambdaプロキシ統合に対応したレスポンスを返す
    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({"message": "Initialized RSSFeed"})
    }

    return response