from struct import pack
import secret
from flask import Flask, request
import cid
import json as jsn

app = Flask(__name__)

EVENT_HEADER = 'X-GitHub-Event'
SIGNATURE_HEADER = 'X-Hub-Signature-256'

INVALID_ENDINGS = ['SNAPSHOT', 'DEVELOPMENT', 'TEST', 'TESTING', 'TESTED', 'TESTING', 'DEV', 'RC', 'RELEASE-CANDIDATE']

@app.route('/webhook/<token>', methods=['POST'])
def register_deployment(token):
    print('token:', token)
    json = request.json
    print('event:', request.headers[EVENT_HEADER])
    if not secret.exists_in_secret(token):
        print('invalid')
        return 'Invalid secret'
    if request.headers[EVENT_HEADER] != 'registry_package':
        print('not package')
        return 'Not a package event'
    # requires the action to be 'published', and the package_type must be docker
    print(jsn.dumps(json, indent=4))
    if not json or json['action'] != 'published' and json['package']['package_type'] != 'docker':
        print('wrong stuff idk')
        return 'Wrong stuff'
    json = json['registry_package']
    package_version = json['package_version']['version'].upper()
    if package_version.endswith(tuple(INVALID_ENDINGS)):
        print('cock')
        return 'test'
    created_at = json['created_at']
    pid = json['id']
    author = json['owner']['login']
    name = json['namespace']
    print(f'{author} build package for production is ready: {pid} {created_at}')
    print(f'Pulling latest image for: {name}')
    package_url = json['package_version']['package_url']
    print(package_url)
    cid.pull(package_url)
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
