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
import feedgenerator
from datetime import datetime, timezone

def lambda_handler(event, context):
    # S3クライアント作成
    s3 = boto3.client('s3')

    # 環境変数からS3のバケット名とファイル名を取得
    BUCKET_NAME = os.environ['BUCKET_NAME']
    FILE_NAME = os.environ['FILE_NAME']

    # rssファイルの要素を初期化する。
    feed_title = "にわのわのRSS"
    feed_link = "https://example.com/rss"
    feed_description = "にわのわさんのRSSFeed。"
    feed_language = "ja"
    feed_author = "にわのわ"

    # エントリーの要素を変数で代入（例として2つのエントリーを生成）
    entry_title = "にわのわさんのブログ"
    entry_link = "https://hugo.niwanowa.tips/"
    entry_summary = "にわのわさんがやってるブログだよ。"

    # RSSフィードの基本構造を生成
    feed = feedgenerator.Atom1Feed(
        title=feed_title,
        link=feed_link,
        description=feed_description,
        language=feed_language,
        author_name=feed_author,
    )

    # フィードにエントリーを追加
    feed.add_item(
        title=entry_title,
        link=entry_link,
        description=entry_summary,
        pubdate=datetime.now(timezone.utc)
    )

    # RSSフィードのXMLを生成
    rss_xml_string = feed.writeString('utf-8')

    # S3のrss.xmlを置換する。
    s3.put_object(
        Bucket=BUCKET_NAME,
        Body=rss_xml_string.encode('utf-8'),
        Key=FILE_NAME,
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