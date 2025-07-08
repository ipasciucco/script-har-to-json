import os
import json
from haralyzer import HarParser

def extract_requests_responses_from_har(file_path):
    with open(file_path, 'r', encoding='utf-8') as har_file:
        har_data = json.load(har_file)
        entries = har_data['log']['entries']
        return entries

def process_all_har_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.har'):
            har_file_path = os.path.join(input_folder, filename)
            output_filename = 'invista_' + os.path.splitext(filename)[0] + '.json'
            output_file_path = os.path.join(output_folder, output_filename)

            print(f"Procesando: {filename}")

            try:
                entries = extract_requests_responses_from_har(har_file_path)

                filtered_entries = [
                    entry for entry in entries
                    if 'sap/opu/odata' in entry['request']['url'] or '/sap/hana' in entry['request']['url']
                ]

                output_data = []
                for entry in filtered_entries:
                    output_data.append({
                        'request': entry['request'],
                        'response': entry['response']
                    })

                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    json.dump(output_data, output_file, indent=4, ensure_ascii=False)

                print(f"Guardado en: {output_file_path}")
            except Exception as e:
                print(f"Error procesando {filename}: {e}")

if __name__ == "__main__":
    input_folder = './input_files'
    output_folder = './output_files'
    process_all_har_files(input_folder, output_folder)