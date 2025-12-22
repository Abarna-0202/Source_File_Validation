# # # installing all the package- this will be done with the first run
# # import subprocess
# # import sys
# # import os

# # os.system('cls')
 
# # def install_and_import(package):
# #     try:
# #         __import__(package)
# #     except ImportError:
# #         print(f"{package} not found. Installing...")
# #         subprocess.check_call([sys.executable, "-m", "pip", "install", package])
# #         print(f"{package} installed successfully!")
 
# # install_and_import("pandas")
# # install_and_import("PyYaml")
# # install_and_import("openpyxl")
# # # -----------------------------------------------------------------

# # import os
# # import yaml
# # from datetime import datetime
# # from Source_File_Analysis import analyze_required_columns  # Import the new function
# # from Archive_Existing_Outputs import archive_existing_outputs # Archive function move output existing files

# # def main():
# #     start_time = datetime.now()
# #     print("Start time:", start_time.strftime("%H:%M:%S"))
    
# #     try:
# #         with open('config.yaml', 'r') as file:
# #             config = yaml.safe_load(file)
# #     except FileNotFoundError:
# #         print("Error: config.yaml file not found.")
# #         return
# #     except PermissionError:
# #         print("Error: Permission denied while accessing config.yaml.")
# #         return

# #     current_dir = os.path.dirname(os.path.realpath(__file__))
# #     folder_parent = os.path.join(current_dir, config['output_folder_parent'])
# #     input_folder = os.path.join(current_dir, config['input_folder_text'])
# #     source_file_analysis_output = os.path.join(folder_parent, config['source_file_analysis_output'])  # New output file

# #     try:
# #         os.makedirs(folder_parent, exist_ok=True)
# #     except PermissionError:
# #         print(f"Error: Permission denied while creating the output folder: {folder_parent}")
# #         return
# # # Archive old files in output folder before new processing
# #     archive_folder = os.path.join(current_dir, config['archive_folder'])
# #     output_folder = os.path.join(current_dir, config['output_folder_parent'])
 
# #     try:
# #         archive_existing_outputs(output_folder, archive_folder)
# #     except Exception as e:
# #         print(f"Error during archiving: {e}")
# #         return
 
# #     # Call the function from Text_To_Excel.py
# #     try:
# #         from Text_To_Excel import process_and_validate_files
# #         process_and_validate_files(config['expected_columns_per_sheet'], config['specific_words'], input_folder, 
# #                                    os.path.join(folder_parent, config['output_file_consolidated']), 
# #                                    os.path.join(folder_parent, config['count_of_records_excel']), 
# #                                    os.path.join(folder_parent, config['empty_columns_summary_excel']))
# #     except Exception as e:
# #         print(f"Error during text to Excel processing: {e}")
# #         return

# #     # Call the new function from Source_File_Analysis.py
# #     try:
# #         analyze_required_columns(config['mapping_file'], input_folder, source_file_analysis_output)
# #     except Exception as e:
# #         print(f"Error during source file analysis: {e}")
# #         return

# #     end_time = datetime.now()
# #     print("End time:", end_time.strftime("%H:%M:%S"))
# #     time_taken = end_time - start_time
# #     print("Time taken:", time_taken)

# # if __name__ == "__main__":
# #     main()


# installing all the package- this will be done with the first run

## pip install xlsxwriter

import subprocess

import sys

import os
 
os.system('cls')
 
def install_and_import(package):

    try:

        __import__(package)

    except ImportError:

        print(f"{package} not found. Installing...")

        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

        print(f"{package} installed successfully!")
 
install_and_import("pandas")

install_and_import("PyYaml")

install_and_import("openpyxl")

# -----------------------------------------------------------------
 
import os

import yaml

from datetime import datetime

from Source_File_Analysis import analyze_required_columns  # Import the new function

from Archive_Existing_Outputs import archive_existing_outputs # Archive function move output existing files

from fields_comparison import compare_fields  # New import for fields comparison
 
def main():

    start_time = datetime.now()

    print("Start time:", start_time.strftime("%H:%M:%S"))

    try:

        with open('config.yaml', 'r') as file:

            config = yaml.safe_load(file)

    except FileNotFoundError:

        print("Error: config.yaml file not found.")

        return

    except PermissionError:

        print("Error: Permission denied while accessing config.yaml.")

        return
 
    current_dir = os.path.dirname(os.path.realpath(__file__))

    folder_parent = os.path.join(current_dir, config['output_folder_parent'])

    input_folder = os.path.join(current_dir, config['input_folder_text'])

    source_file_analysis_output = os.path.join(folder_parent, config['source_file_analysis_output'])  # New output file
 
    try:

        os.makedirs(folder_parent, exist_ok=True)

    except PermissionError:

        print(f"Error: Permission denied while creating the output folder: {folder_parent}")

        return

# Archive old files in output folder before new processing

    archive_folder = os.path.join(current_dir, config['archive_folder'])

    output_folder = os.path.join(current_dir, config['output_folder_parent'])
 
    try:

        archive_existing_outputs(output_folder, archive_folder)

    except Exception as e:

        print(f"Error during archiving: {e}")

        return
 
    # Call the function from Text_To_Excel.py

    try:

        from Text_To_Excel import process_and_validate_files

        process_and_validate_files(config['expected_columns_per_sheet'], config['specific_words'], input_folder,

                                   os.path.join(folder_parent, config['output_file_consolidated']),

                                   os.path.join(folder_parent, config['count_of_records_excel']),

                                   os.path.join(folder_parent, config['empty_columns_summary_excel']))

    except Exception as e:

        print(f"Error during text to Excel processing: {e}")

        return
 
    # Call the new function from Source_File_Analysis.py

    try:

        analyze_required_columns(config['mapping_file'], input_folder, source_file_analysis_output)

    except Exception as e:

        print(f"Error during source file analysis: {e}")

        return
 
    # Call the fields comparison function (new)

    try:

        compare_fields(config['mapping_file'], input_folder, os.path.join(folder_parent, config['output_entity_check']))

    except Exception as e:

        print(f"Error during fields comparison: {e}")

        return
 
    end_time = datetime.now()

    print("End time:", end_time.strftime("%H:%M:%S"))

    time_taken = end_time - start_time

    print("Time taken:", time_taken)
 
if __name__ == "__main__":

    main()



