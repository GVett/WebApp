from flask import Blueprint, request, jsonify
import requests
import json

api_blueprint = Blueprint('api_blueprint', __name__, template_folder = 'templates')

@api_blueprint.route('/api', methods=['GET'])
def query_records():
    with open('app/api/data.json', 'r') as f:
        data = f.read()
        records = json.loads(data)
        server_ip = 'https://Intro-to-Server-Side.s-bryceb.repl.co/api'
        headers = {'Content-Type': 'application/json'}
        requests.put(server_ip, headers = headers, data = records[0])
        for record in records:
              return jsonify(record)
        return jsonify({'error': 'data not found'})

@api_blueprint.route('/api', methods=['PUT'])
def create_record():
  try:
    record = request.get_json(forced=True)
  except:
    print("Failed")
    record = {"mood": "happy"}
  finally:
    print("Got out of there")
  with open('app/api/data.json', 'r') as f:
      data = f.read()
  if not data:
      records = [record]
  else:
      records = json.loads(data)
      records.append(record)
  with open('app/api/data.json', 'w') as f:
      f.write(json.dumps(records, indent=2))
  return jsonify(record)

@api_blueprint.route('/api', methods=['POST'])
def update_record():
    record = json.loads(request.data)
    new_records = []
    with open('app/api/data.json', 'r') as f:
        data = f.read()
        records = json.loads(data)
    for r in records:
        if r['color'] == record['color']:
            r['value'] = record['value']
        new_records.append(r)
    with open('app/api/data.json', 'w') as f:
        f.write(json.dumps(new_records, indent=2))
    return jsonify(record)
    
@api_blueprint.route('/api', methods=['DELETE'])
def delete_record():
    record = json.loads(request.data)
    new_records = []
    with open('app/api/data.json', 'r') as f:
        data = f.read()
        records = json.loads(data)
        for r in records:
            if r['color'] == record['color']:
                continue
            new_records.append(r)
    with open('app/api/data.json', 'w') as f:
        f.write(json.dumps(new_records, indent=2))
    return jsonify(record)