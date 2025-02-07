def get_event(path, method, params=None, body=None, headers=None):
    headers = headers or {
        'Accept': '*/*',
        'Authorization': 'token',
        'content-type': 'application/json'
    }
    return {
        'type': 'LAMBDA',
        'resource': path,
        'path': path,
        'httpMethod': method.upper(),
        'headers': {
            'CloudFront-Forwarded-Proto': 'https',
            'CloudFront-Is-Desktop-Viewer': 'true',
            'CloudFront-Is-Mobile-Viewer': 'false',
            'CloudFront-Is-SmartTV-Viewer': 'false',
            'CloudFront-Is-Tablet-Viewer': 'false',
            'CloudFront-Viewer-Country': 'FR',
            'Host': 'htzd2rneg1.execute-api.eu-west-1.amazonaws.com',
            'User-Agent': 'insomnia/2021.4.1',
            'Via': '2.0 4dd111c814b0b5cf8bf82e59008da625.cloudfront.net (CloudFront)',
            'X-Amz-Cf-Id': 'ka1hbQCSUOZ-d0VQYuE_gtF4icy443t7kP3UGsDLZDF_5QyTX13FoQ==',
            'X-Amzn-Trace-Id': 'Root=1-6124f604-3fb9457c7489ebf14ed0f8f6',
            'X-Forwarded-For': '78.234.174.193, 130.176.152.165',
            'X-Forwarded-Port': '443',
            'X-Forwarded-Proto': 'https',
            **headers
        },
        'multiValueHeaders': {},
        'body': body or {},
        'queryStringParameters': {},
        'multiValueQueryStringParameters': params or {},
        'pathParameters': {},
        'stageVariables': None,
        'isBase64Encoded': False,
        'requestContext': {
            'httpMethod': 'GET',
            'resourceId': 'fp5ol74tr7',
            'resourcePath': '/',
            'extendedRequestId': 'EktgyFweDoEFabw=',
            'requestTime': '24/Aug/2021:13:37:08 +0000',
            'path': '/dev/',
            'accountId': '935392763270',
            'protocol': 'HTTP/1.1',
            'stage': 'dev',
            'domainPrefix': 'htzd2rneg1',
            'requestTimeEpoch': 1629812228818,
            'requestId': '2fa7f00a-58fe-4f46-a829-1fee00898e42',
            'domainName': 'htzd2rneg1.execute-api.eu-west-1.amazonaws.com',
            'apiId': 'htzd2rneg1'
        },
        'params': {
            'path': {},
            'querystring': {},
            'header': {'Accept': '*/*', 'Authorization': 'token', 'CloudFront-Forwarded-Proto': 'https',
                       'CloudFront-Is-Desktop-Viewer': 'true', 'CloudFront-Is-Mobile-Viewer': 'false',
                       'CloudFront-Is-SmartTV-Viewer': 'false', 'CloudFront-Is-Tablet-Viewer': 'false',
                       'CloudFront-Viewer-Country': 'FR', 'content-type': 'application/json',
                       'Host': 'htzd2rneg1.execute-api.eu-west-1.amazonaws.com', 'User-Agent': 'insomnia/2021.4.1',
                       'Via': '2.0 4dd111c814b0b5cf8bf82e59008da625.cloudfront.net (CloudFront)',
                       'X-Amz-Cf-Id': 'ka1hbQCSUOZ-d0VQYuE_gtF4icy443t7kP3UGsDLZDF_5QyTX13FoQ==',
                       'X-Amzn-Trace-Id': 'Root=1-6124f604-3fb9457c7489ebf14ed0f8f6',
                       'X-Forwarded-For': '78.234.174.193, 130.176.152.165', 'X-Forwarded-Port': '443',
                       'X-Forwarded-Proto': 'https'}},
        'context': {
            'resourceId': 'fp5ol74tr7',
            'authorizer': '',
            'resourcePath': '/',
            'httpMethod': 'GET',
            'extendedRequestId': 'EktgyFweDoEFabw=',
            'requestTime': '24/Aug/2021:13:37:08 +0000',
            'path': '/dev/',
            'accountId': '935392763270',
            'protocol': 'HTTP/1.1',
            'requestOverride': '',
            'stage': 'dev',
            'domainPrefix': 'htzd2rneg1',
            'requestTimeEpoch': '1629812228818',
            'requestId': '2fa7f00a-58fe-4f46-a829-1fee00898e42',
            'identity': '',
            'domainName': 'htzd2rneg1.execute-api.eu-west-1.amazonaws.com',
            'responseOverride': '',
            'apiId': 'htzd2rneg1'
        }
    }
