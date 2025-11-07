import os
import glob

def combine_files_to_single_txt(folder_path, output_filename="combined_files.txt"):
    """
    Reads all files in a folder and combines their content into a single text file
    
    Args:
        folder_path (str): Path to the folder containing files
        output_filename (str): Name of the output text file
    """
    
    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist!")
        return
    
    # Get all files in the folder (excluding subdirectories)
    all_files = [f for f in os.listdir(folder_path) 
                if os.path.isfile(os.path.join(folder_path, f))]
    
    if not all_files:
        print("No files found in the specified folder!")
        return
    
    # Sort files for consistent ordering
    all_files.sort()
    
    # Create the output file
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        output_file.write(f"COMBINED CONTENT FROM FOLDER: {folder_path}\n")
        output_file.write("=" * 50 + "\n\n")
        
        files_processed = 0
        
        for filename in all_files:
            file_path = os.path.join(folder_path, filename)
            
            # Skip the output file if it's in the same folder
            if file_path == os.path.join(folder_path, output_filename):
                continue
            
            try:
                # Write file header
                output_file.write(f"FILE: {filename}\n")
                output_file.write("-" * 40 + "\n")
                
                # Read and write file content
                with open(file_path, 'r', encoding='utf-8') as input_file:
                    content = input_file.read()
                    output_file.write(content)
                
                # Add separation between files
                output_file.write("\n\n" + "=" * 50 + "\n\n")
                files_processed += 1
                print(f"Processed: {filename}")
                
            except UnicodeDecodeError:
                # Skip binary files or files with different encoding
                print(f"Skipped (binary/unreadable): {filename}")
                # Still write the filename to indicate it was skipped
                output_file.write(f"[BINARY FILE - CONTENT NOT COPIED]\n")
                output_file.write("\n\n" + "=" * 50 + "\n\n")
                
            except Exception as e:
                print(f"Error reading {filename}: {str(e)}")
                output_file.write(f"[ERROR READING FILE: {str(e)}]\n")
                output_file.write("\n\n" + "=" * 50 + "\n\n")
    
    print(f"\nSuccessfully processed {files_processed} files!")
    print(f"Combined content saved to: {output_filename}")

# Usage example
if __name__ == "__main__":
    # Specify the folder path here
    folder_path = "C:\\Users\\Vishal\\Documents\\hospital_final_backend\\app\\models"  # Current directory
    # folder_path = "C:/Your/Folder/Path"  # Or specify absolute path
    
    # Call the function
    combine_files_to_single_txt(folder_path, "all_files_combined.txt")