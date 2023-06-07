import json
import os

# Directories
src = '/Users/shaiazali/Documents/Interviews/Quantigo AI/sampleJson/Files'
dst = '/Users/shaiazali/Documents/Interviews/Quantigo AI/sampleJson/Formatted_Files'

# Json Formating Function


def formatJson(source_folder, destination_folder):
    for filename in os.listdir(source_folder):
        if filename.endswith('.json'):
            with open(os.path.join(source_folder, filename), 'r') as json_file:
                json_data = json.load(json_file)

            # Convert the JSON data to the desired format
            # Defining 'annotation_objects' & 'license_plate' Structure
            annotation_objects = {
                'vehicle': {
                    'presence': 0,
                    'bbox': []
                },
                'license_plate': {
                    'presence': 0,
                    'bbox': []
                }
            }
            annotation_attributes = {
                'vehicle': {
                    'Type': '',
                    'Pose': '',
                    'Model': '',
                    'Make': '',
                    'Color': ''
                },
                'license_plate': {
                    'Difficulty Score': 0,
                    'Value': '',
                    'Occlusion': 0
                }
            }

            # Updating 'annotation_objects' & 'license_plate'
            for objects in json_data['objects']:
                object_name = objects['classTitle'].replace(' ', '_').lower()

                # Presence Checker
                presence_flag = 0
                if object_name == 'vehicle':
                    annotation_objects['vehicle']['presence'] = 1
                elif object_name == 'license_plate':
                    annotation_objects['license_plate']['presence'] = 1

                # Setting bbox
                for subList in objects['points']['exterior']:
                    annotation_objects[object_name]['bbox'].extend(subList)

                # Adding Attributes
                tempDict = {}
                for tags in objects['tags']:
                    if (tags['name'] == 'Difficulty Score'):
                        tempDict[tags['name']] = int(tags['value'])
                    else:
                        tempDict[tags['name']] = tags['value']
                annotation_attributes[object_name].update(tempDict)

            # Null checker
            for objects in annotation_objects:
                if annotation_objects[objects]['presence'] == 0:
                    for attr in annotation_attributes[objects]:
                        annotation_attributes[objects][attr] = None

            # Creating final formatted_json_data
            formatted_json_data = [
                {
                    'dataset_name': filename,
                    'image_link': '',
                    'annotation_type': 'image',
                    'annotation_objects': annotation_objects,
                    'annotation_attributes': annotation_attributes
                }
            ]

            # Generate the new file name
            new_json_filename = 'formatted_' + filename

            # Writing the formatted JSON data to a new file
            with open(os.path.join(destination_folder, new_json_filename), 'w') as new_json_file:
                json.dump(formatted_json_data, new_json_file, indent=2)

            print(f"Formatted JSON saved as {new_json_filename}")


formatJson(src, dst)
