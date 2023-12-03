from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')

# Replace these values with your Alibaba Cloud OSS credentials
OSS_ACCESS_KEY_ID = 'your_access_key_id'
OSS_ACCESS_KEY_SECRET = 'your_access_key_secret'
OSS_ENDPOINT = 'http://your-endpoint.com'
OSS_BUCKET_NAME = 'your-bucket-name'

auth = oss2.Auth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET_NAME)


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        if file:
            # Read file content directly
            file_content = file.read()

            # Upload the file content to Alibaba Cloud OSS
            object_key = f"uploads/{file.filename}"
            bucket.put_object(object_key, file_content)

            # Return the OSS URL for the uploaded file
            oss_url = f"https://{OSS_BUCKET_NAME}.{OSS_ENDPOINT}/{object_key}"
            return jsonify({'success': True, 'message': 'File uploaded successfully', 'oss_url': oss_url})
        else:
            return jsonify({'success': False, 'message': 'No file received'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
        
@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)
