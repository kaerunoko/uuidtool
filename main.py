from flask import Flask, request
import uuid
import json
import datetime
import time

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET'])
def generate_uuid():
    version = request.args.get('version', '')
    if version == '1':
        return uuid.uuid1().hex
    elif version == '3':
        return uuid.uuid3().hex
    elif version == '4':
        return uuid.uuid4().hex
    elif version == '5':
        return uuid.uuid5().hex
    else:
        return 'error'

@app.route('/convert', methods=['GET'])
def convert():
    request_uuids = request.args.get('uuid', '')
    if request_uuids == '':
        return ''

    return json.dumps(map(perse_uuid, request_uuids.split(',')))

def perse_uuid(request_uuid):
    try:
        target_uuid = uuid.UUID(request_uuid)
    except:
        return {'uuid': request_uuid, 'status': 'parse error'}

    if target_uuid.version == 1:
        # UUID epoch 1582-10-15 00:00:00 and the Unix epoch 1970-01-01 00:00:00.
        uuid_datetime = datetime.datetime.fromtimestamp((target_uuid.time - 0x01b21dd213814000L)*100/1e9)
        dt = uuid_datetime.strftime('%Y/%m/%d %H:%M:%S.%f')
        return {
            'uuid': request_uuid,
            'version': target_uuid.version,
            'status': 'success',
            'datatime': dt}
    else:
        return {
            'uuid': request_uuid,
            'version': target_uuid.version,
            'status': 'success'}

if __name__ == '__main__':
    app.run()
