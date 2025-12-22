import os
import shutil
from datetime import datetime
 
def archive_existing_outputs(output_folder, archive_folder):
    if not os.path.exists(output_folder) or not os.listdir(output_folder):
        print("No output files to archive.")
        return
 
    # Create a unique archive subfolder name using current datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_archive_subfolder = os.path.join(archive_folder, f"archive_{timestamp}")
    os.makedirs(new_archive_subfolder, exist_ok=True)
 
    # Move all files from output to archive
    for item in os.listdir(output_folder):
        src_path = os.path.join(output_folder, item)
        dst_path = os.path.join(new_archive_subfolder, item)
        shutil.move(src_path, dst_path)
 
    print(f"Archived old output files to: {new_archive_subfolder}")