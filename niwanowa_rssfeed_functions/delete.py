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

    return {"message": "DELETE"}