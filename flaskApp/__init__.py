from flask import Flask, render_template, request, jsonify
import requests
import json
import time
import hashlib
import urllib

app = Flask(__name__)

@app.route('/order')
def order():
    return render_template('order.html')

@app.route('/ready', methods=['POST'])
def ready():
    params = {}
    apiKey = 'U1FVQVJFLTEwMDAxMTIwMTgwNDA2MDkyNTMyMTA1MjM0'
    params['version'] = '1.0'
    params['mbrNo'] = request.form['mbrNo']
    params['goodsName'] = request.form['goodsName']
    params['mbrRefNo'] = 'OID' + str(int(time.time() * 100000))
    params['paymethod'] = 'CARD'
    params['amount'] = '1000'
    params['approvalUrl'] = 'http://localhost:5000/success'
    params['closeUrl'] = 'http://localhost:5000/close'
    params['timestamp'] = str(int(time.time() * 100000))
    signFormat = '{0}|{1}|{2}|{3}|{4}'
    signature = hashlib.sha256(signFormat.format(params['mbrNo'], params['mbrRefNo'],
                                                 params['amount'], apiKey, params['timestamp']).encode()).hexdigest()
    params['signature'] = signature
    params['merchantData'] = params['mbrRefNo']

    url = 'https://test-api-std.mainpay.co.kr/v1/payment/ready'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = requests.post(url, data=urllib.parse.urlencode(params), headers=headers)

    print('## URL : ', res.request.url)
    print('## 요청헤더 : ', res.request.headers)
    print('## 요청보디 : ', res.request.body)
    print('## 요청결과 : ', res.text)

    return res.json()


@app.route('/success', methods=['GET'])
def success():
    params = {}
    apiKey = 'U1FVQVJFLTEwMDAxMTIwMTgwNDA2MDkyNTMyMTA1MjM0'
    params['version'] = '1.0'
    params['mbrNo'] = '100011'
    params['aid'] = request.args.get('aid')
    params['authToken'] = request.args.get('authToken')
    params['mbrRefNo'] = request.args.get('merchantData')
    params['paymethod'] = 'CARD'
    params['amount'] = '1000'
    params['timestamp'] = str(int(time.time() * 100000))
    signFormat = '{0}|{1}|{2}|{3}|{4}'
    signature = hashlib.sha256(signFormat.format(params['mbrNo'], params['mbrRefNo'],
                                                 params['amount'], apiKey, params['timestamp']).encode()).hexdigest()
    params['signature'] = signature

    url = 'https://test-api-std.mainpay.co.kr/v1/payment/pay'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = requests.post(url, data=urllib.parse.urlencode(params), headers=headers)

    print('## URL : ', res.request.url)
    print('## 요청헤더 : ', res.request.headers)
    print('## 요청보디 : ', res.request.body)
    print('## 요청결과 : ', res.text)
    return render_template('success.html', result=res.json())

@app.route('/close')
def close():
    return render_template('close.html')