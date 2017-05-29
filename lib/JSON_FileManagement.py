import json


def json_file_to_object(json_file_path):
    """Opens a JSON file and returns a list or dictionary object created from the JSON file contents.
        Error will occur if file is NOT of JSON format"""
    json_file = open(json_file_path, "r")
    try:
        decoded_json_file = json.loads(json_file.read())
    except json.decoder.JSONDecodeError:
        print("Not a valid JSON file")
        exit()
    json_file.close()

    return decoded_json_file


def save_file_as_json(file_path, data):
    file = open(str(file_path), "w")
    json.dump(data, file)
    file.close()
    print("File saved at", file_path)

def dump_json_to_string(json_object):
    return json.dumps(json_object)
