import json

def read_file(file_path, member_name):
    file = open(file_path, 'r')
    file_content = file.read()
    encoded_requests = json.loads(file_content)
    requests = []
    for elem in encoded_requests:
        requests.append(elem[member_name])
    return requests

def read_file_lines(file_path, member_name):
    file = open(file_path, 'r')
    file_content = file.read()
    documents = []
    lines = file_content.split("\n")
    objs = []
    for line in lines:
        objs.append(json.loads(line))
    for document in objs:
        documents.append(document[member_name])
    return documents
