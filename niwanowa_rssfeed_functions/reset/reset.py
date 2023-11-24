"""
/reset:
    get:
      summary: 'RSSFeedをリセット(初回生成)するAPI'
      responses:
        '200':
          description: 'Content added to the RSS feed'
      x-amazon-apigateway-integration:
        httpMethod: post
        type: aws_proxy
        uri:
          Fn::Sub: arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${ResetRSSFeedFunction.Arn}/invocations
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
        "body": json.dumps({"message": "Initialized RSSFeed"})
    }

    return response