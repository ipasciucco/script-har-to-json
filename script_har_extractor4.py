import json
import os
from haralyzer import HarParser

input_dir = './input_files'
output_dir = './output_files'
os.makedirs(output_dir, exist_ok=True)

def extract_requests_responses_from_har(file_path):
    with open(file_path, 'r', encoding='utf-8') as har_file:
        har_data = json.load(har_file)
        entries = har_data['log']['entries']
        return entries

for filename in os.listdir(input_dir):
    if filename.endswith('.har'):
        har_file_path = os.path.join(input_dir, filename)
        entries = extract_requests_responses_from_har(har_file_path)

        filtered_entries = []
        for entry in entries:
            url = entry['request'].get('url', '')
            mime = entry['response']['content'].get('mimeType', '')

            if not ('sap/opu/odata' in url or '/sap/hana' in url or 'PM_SRV' in url):
                continue

            if mime in ['text/css', 'application/javascript']:
                continue

            if '$metadata' in url:
                headers = entry['response'].get('headers', [])
                has_ct_header = any(
                    h.get('name') == 'Content-Type' and h.get('value') == 'application/xml'
                    for h in headers
                )
                if not has_ct_header:
                    headers.insert(0, {
                        'name': 'Content-Type',
                        'value': 'application/xml'
                    })
                    entry['response']['headers'] = headers

            filtered_entries.append(entry)

        output_data = []
        for entry in filtered_entries:
            request = entry['request']
            response = entry['response']
            request_info = {
                'request': request,
                'response': response
            }
            output_data.append(request_info)

        output_filename = 'invista_' + os.path.splitext(filename)[0] + '.json'
        output_file_path = os.path.join(output_dir, output_filename)

        with open(output_file_path, 'w') as output_file:
            json.dump(output_data, output_file, indent=4)

        print(f"Los datos se han guardado en el archivo: {output_file_path}")