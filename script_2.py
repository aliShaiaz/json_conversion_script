import json
import os

# Directories
src = '/Users/shaiazali/Documents/Interviews/Quantigo AI/sampleJson/Files'
dst = '/Users/shaiazali/Documents/Interviews/Quantigo AI/sampleJson/Formatted_Files'


# Combining & Renaming Function
def combine_rename(source_folder, destination_folder):

    # Output File Structure
    new_combined_json_data = {
        'description': '',
        'tags': [],
        'size': {
            'height': 720,
            'width': 1280
        },
        'objects': []
    }

    # Aggregating All Files in 'source_folder'
    for filename in os.listdir(source_folder):
        if filename.endswith('.json'):
            with open(os.path.join(source_folder, filename), 'r') as json_file:
                json_data = json.load(json_file)

            # Extending 'objects' to aggregate
            new_combined_json_data['objects'].extend(json_data['objects'])

    # Converting 'Vehicle' to 'Car' & 'License Plate' to 'Number'
    for objects in new_combined_json_data['objects']:
        if objects['classTitle'] == 'Vehicle':
            objects['classTitle'] = 'Car'
        if objects['classTitle'] == 'License Plate':
            objects['classTitle'] = 'Number'

    # Generate the new file name
    new_combined_filename = 'combined_json_files.json'

    # Writing the formatted JSON data to a new file
    with open(os.path.join(destination_folder, new_combined_filename), 'w') as new_json_file:
        json.dump(new_combined_json_data, new_json_file, indent=2)

    print(f"Formatted JSON saved as {new_combined_filename}")


combine_rename(src, dst)
