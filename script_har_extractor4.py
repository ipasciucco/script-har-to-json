import json
from haralyzer import HarParser

def extract_requests_responses_from_har(file_path):
    with open(file_path, 'r', encoding='utf-8') as har_file:
        har_data = json.load(har_file)
        entries = har_data['log']['entries']
        return entries

# Example usage
har_file_path = './mobilepurchasereq/mobile3.har'
entries = extract_requests_responses_from_har(har_file_path)

filtered_entries = [entry for entry in entries if 'sap/opu/odata' in entry['request']['url'] or '/sap/hana' in entry['request']['url']]

output_file_path = './mobilepurchasereq/mobile3.json'  # Output JSON file path
output_data = []

for entry in filtered_entries:
    request = entry['request']
    response = entry['response']

    request_info = {
        'request': request,
        'response': response
    }

    output_data.append(request_info)

with open(output_file_path, 'w') as output_file:
    json.dump(output_data, output_file, indent=4)

print(f"Los datos se han guardado en el archivo: {output_file_path}")
