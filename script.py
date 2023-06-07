import json
import os

# Specify the folder path containing the JSON files
# source_folder = '/path/to/json/files/'
source_folder = '/Users/shaiazali/Documents/Interviews/Quantigo AI/sampleJson/Files'
destination_folder = '/Users/shaiazali/Documents/Interviews/Quantigo AI/sampleJson/Formatted_Files'

for filename in os.listdir(source_folder):
    if filename.endswith('.json'):
        with open(os.path.join(source_folder, filename), 'r') as json_file:
            json_data = json.load(json_file)
            # print(json_data['objects'][0]['classTitle'])


        annotation_objects = {}
        annotation_attributes = {}
        for objects in json_data['objects']:
            # Presence Checker
            presence_flag = 0
            if (objects['classTitle'] == 'Vehicle' or objects['classTitle'] == 'License Plate'):
                presence_flag = 1

            # Defining Structure
            object_name = objects['classTitle'].replace(' ', '_').lower()
            annotation_objects[object_name] = {
                "presence": presence_flag,
                "bbox": []
            }

            # setting bbox
            for subList in objects['points']['exterior']:
                annotation_objects[object_name]['bbox'].extend(subList)

            # Adding Attributes
            tempDict = {}
            for tags in objects['tags']:
                tempDict[tags['name']] = tags['value']
            annotation_attributes[object_name] = tempDict

        # print(annotation_objects)
        # print(annotation_attributes)

        # Convert the JSON data to the desired format
        formatted_json_data = [
            # 'filename': filename.replace('.json', ''),
            # 'data': json_data
            # Add more fields or modify the existing fields as needed

            {
                'dataset_name': filename,
                'image_link': '',
                'annotation_type': 'image',
                "annotation_objects": annotation_objects,
                "annotation_attributes": annotation_attributes
            }
        ]

        # Generate the new file name
        new_filename = 'formatted_' + filename

        # Write the formatted JSON data to a new file
        with open(os.path.join(destination_folder, new_filename), 'w') as new_json_file:
            json.dump(formatted_json_data, new_json_file, indent=4)

        print(f"Formatted JSON saved as {new_filename}")
