# hde
Heap Dump Exporter

Here's a summary of the code:

Configuration variables:
   GCSBUCKET: Specifies the destination GCS bucket.
   GCPPROJECT: Specifies the Google Cloud project ID.
   WATCHPATH: Specifies the path to monitor for files and directories.
   SLEEP: Specifies the sleep duration between iterations.

set_gcp_project(project_name): A function to set the Google Cloud project using the gcloud command-line tool.

copy_to_gcs(src_path, dest_path): A function to copy files from the source path to the specified GCS destination path. It includes logic to ensure that the file has finished writing before copying it.

The main() function:
1. Initializes logging and sets the Google Cloud project.
2. Initializes previous_ts to 0.
3. Enters an infinite loop for continuous monitoring.
4. Inside the loop:
   a. Checks if previous_ts is greater than 0 to determine if it's the initial iteration.
   b. If it's the initial iteration (when previous_ts is 0), it logs an "Initial Looping" message and sets previous_ts to the current time.
   c. If it's not the initial iteration, it collects a list of files and directories in the specified paths using glob.glob(WATCHPATH).
   d. For each file or directory in the list, it checks their creation and modification times using os.path.getctime and os.path.getmtime.
   e. If a file or directory has been created or modified since the previous iteration, it constructs a GCS path and issues a copy command using copy_to_gcs.
   f. It then sleeps for a specified duration (SLEEP) before the next iteration.
