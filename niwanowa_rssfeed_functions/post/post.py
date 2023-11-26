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
import os
import feedgenerator
import feedparser
from datetime import datetime

def lambda_handler(event, context):
    # S3クライアント作成
    s3 = boto3.client('s3')

    # 環境変数からS3のバケット名とファイル名を取得
    BUCKET_NAME = os.environ['BUCKET_NAME']
    FILE_NAME = os.environ['FILE_NAME']

    # rssファイル読み込み
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_NAME)
    rss_xml_string = obj['Body'].read().decode('utf-8')

    # feedparserでパース
    feed = feedparser.parse(rss_xml_string)

    print(feed)

    # リクエストボディからlinkを取得
    link = event['link']

    print(link)

    # Lambdaプロキシ統合に対応したレスポンスを返す
    response = {
      "statusCode": 200,
      "headers": {
        "Content-Type": "application/json"
      },
      "body": json.dumps({"message": "Content added to the RSS feed"})
    }
