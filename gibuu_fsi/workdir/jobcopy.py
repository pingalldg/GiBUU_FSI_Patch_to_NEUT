import os

# Path to the original job file
job_file_path = "path_to_folder/005_Neutrino_T2K-numu_res_ccqe.job"  # original file to base updates on

for i in range(6, 7):
    # Construct new path for path_To_External
    new_path = f"path_to_workdir/{i}/input_values{i}.f90"

    # Read the original file
    with open(job_file_path, 'r') as file:
        lines = file.readlines()

    # Replace the line containing path_To_External
    updated_lines = []
    for line in lines:
        if line.strip().startswith("path_To_External="):
            updated_line = f"      path_To_External = '{new_path}'\n"
            updated_lines.append(updated_line)
        else:
            updated_lines.append(line)

    # Construct the output directory and file
    output_dir = f"path_to_workdir/{i}"
    os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists

    output_file = os.path.join(output_dir, "005_Neutrino_T2K-numu.job")

    # Write the updated job file
    with open(output_file, 'w') as file:
        file.writelines(updated_lines)

    print(f"Updated job file written to: {output_file}")

