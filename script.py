import json
import os

source_folder = '/Users/shaiazali/Documents/Interviews/Quantigo AI/sampleJson/Files'
destination_folder = '/Users/shaiazali/Documents/Interviews/Quantigo AI/sampleJson/Formatted_Files'

for filename in os.listdir(source_folder):
    if filename.endswith('.json'):
        with open(os.path.join(source_folder, filename), 'r') as json_file:
            json_data = json.load(json_file)

        # Defining Structure #
        annotation_objects = {
            "vehicle": {
                "presence": 0,
                "bbox": []
            },
            "license_plate": {
                "presence": 0,
                "bbox": []
            }
        }
        annotation_attributes = {
            "vehicle": {},
            "license_plate": {
                "Difficulty Score": 0,
                "Value": "",
                "Occlusion": 0
            }
        }

        for objects in json_data['objects']:
            object_name = objects['classTitle'].replace(' ', '_').lower()

            # Presence Checker
            presence_flag = 0
            if object_name == 'vehicle':
                annotation_objects['vehicle']['presence'] = 1
            if object_name == 'license_plate':
                annotation_objects['license_plate']['presence'] = 1

            # setting bbox
            for subList in objects['points']['exterior']:
                annotation_objects[object_name]['bbox'].extend(subList)

            # Adding Attributes
            tempDict = {}
            for tags in objects['tags']:
                if (tags['name'] == "Difficulty Score"):
                    tempDict[tags['name']] = int(tags['value'])
                    # print(tempDict)
                else:
                    tempDict[tags['name']] = tags['value']
            annotation_attributes[object_name].update(tempDict)

        # Convert the JSON data to the desired format
        formatted_json_data = [
            {
                'dataset_name': filename,
                'image_link': '',
                'annotation_type': 'image',
                "annotation_objects": annotation_objects,
                "annotation_attributes": annotation_attributes
            }
        ]

        # Generate the new file name
        new_json_filename = 'formatted_' + filename

        # Writing the formatted JSON data to a new file
        with open(os.path.join(destination_folder, new_json_filename), 'w') as new_json_file:
            json.dump(formatted_json_data, new_json_file, indent=2)

        print(f"Formatted JSON saved as {new_json_filename}")
