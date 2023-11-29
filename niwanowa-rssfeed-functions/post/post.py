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
from datetime import datetime, timezone
import requests
from bs4 import BeautifulSoup
import time

def lambda_handler(event, context):
    print(event)
    # S3クライアント作成
    s3 = boto3.client('s3')

    # 環境変数からS3のバケット名とファイル名を取得
    BUCKET_NAME = os.environ['BUCKET_NAME']
    FILE_NAME = os.environ['FILE_NAME']

    # rssファイル読み込み
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_NAME)
    rss_xml_string = obj['Body'].read().decode('utf-8')

    # feedparserでパース
    feed_parser = feedparser.parse(rss_xml_string)

    print(feed_parser)

    # FeedParserDictからfeedgeneratorのAtom用Feedオブジェクトを作成
    feed_generator = feedgenerator.Atom1Feed(
        title=feed_parser.feed.title,
        link=feed_parser.feed.link,
        description=feed_parser.feed.subtitle,
        language=feed_parser.feed.language,
        author_name=feed_parser.feed.author,
    )



    # Feedオブジェクトにパーサーのエントリーを追加
    for entry in feed_parser.entries:
        print(entry)
        feed_generator.add_item(
            title=entry.get('title'),
            link=entry.get('link'),
            description=entry.get('description', 'description is empty'),
            pubdate=datetime.fromtimestamp(time.mktime(entry.updated_parsed)),
        )


    print(feed_generator.writeString('utf-8'))

    # リクエストボディからlinkを取得
    link = json.loads(event['body']).get('link')

    # linkからページタイトルを取得
    page_title = get_page_title(link)

    # feedにエントリー追加
    feed_generator.add_item(
        title=page_title,
        link=link,
        description=page_title,
        pubdate=datetime.now(timezone.utc),
    )

    # Stringに書き出し
    rss_xml_string = feed_generator.writeString('utf-8')

    # #s3にアップロード
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
        "body": json.dumps({"message": "Content added to the RSS feed"})
    }

    return response

def get_page_title(link):
    # ページタイトルを取得する。
    # ページタイトルが取得できない場合は、空文字を返す。

    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "html.parser")
        page_title = soup.title.string if soup.title else None
        return page_title
    except Exception as e:
      print(e)
      return None