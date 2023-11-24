"""
post:
      summary: 'RSSFeedを登録するAPI'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                link:
                  type: string
                  example: 'http://yourwebsite.com'
              required:
                - link
      responses:
        '200':
          description: 'Content added to the RSS feed'
"""

import json
import boto3

def lambda_handler(event, context):
    # S3クライアント作成
    s3 = boto3.client('s3')
    bucket = 'niwanowa-rssfeed'

    # S3からXMLを取得対象ファイルがない場合はエラーを出力する
    
    # Lambdaプロキシ統合に対応したレスポンスを返す
    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({"message": "POST"})
    }

    return response