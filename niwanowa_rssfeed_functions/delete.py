"""
parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
          example: '1'
    delete:
      summary: '指定されたRSSfeedを削除するAPI'
      responses:
        '200':
          description: 'Content deleted from the RSS feed'
"""

import json
import boto3

def lambda_handler(event, context):
  # Lambdaプロキシ統合に対応したレスポンスを返す
  response = {
    "statusCode": 200,
    "headers": {
      "Content-Type": "application/json"
    },
    "body": json.dumps({"message": "Content deleted from the RSS feed"})
  }

  return response
