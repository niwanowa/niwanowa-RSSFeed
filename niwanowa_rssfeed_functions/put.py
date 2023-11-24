"""
parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
          example: '1'
put:
    summary: '指定されたRSSfeedを更新するAPI'
    requestBody:
    required: true
    content:
        text/plain:
        schema:
            type: string
            example: 'Updated Content'
    responses:
    '200':
        description: 'Content updated in the RSS feed'
"""

import json
import boto3

def lambda_handler(event, context):

    return {"message": "PUT"}