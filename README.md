# Continuous File Monitoring and GCS Copy Utility

# Overview
This Python utility provides a solution for monitoring specific files and directories in a specified path and copying them to Google Cloud Storage (GCS) when they have been created or modified. 
The utility is designed for use cases where you need to continuously monitor files and ensure that they are fully written before copying them to GCS.
The script automates the process of monitoring and copying files, eliminating the need for manual intervention. This utility is particularly valuable in scenarios where the seamless export of thread dumps, Out-of-Memory (OOM) generated heap dumps, or other critical data is essential. For example, imagine a Kubernetes environment where applications produce thread dumps and heap dumps when encountering issues. Manually exporting and managing these dumps can be time-consuming and error-prone. With this script in place, these dumps are automatically monitored and swiftly copied to Google Cloud Storage (GCS) for further analysis, ensuring that crucial diagnostic data is readily available for troubleshooting and problem resolution.

# Features
- Monitors files and directories in the specified path. <br />
- Copies files to a specified GCS bucket when they are created or modified. <br />
- Ensures that files are fully written before initiating the copy operation. <br />
- Supports error handling and logging to keep track of the copying process. <br />
- Configurable sleep duration between monitoring iterations. <br />

# Prerequisites
Before using the script, ensure the following prerequisites are met: <br />
- Python environment with required dependencies. <br />
- Google Cloud SDK configured with appropriate permissions. <br />
- Properly set values for GCSBUCKET and GCPPROJECT variables. <br />

# Error Handling
The script includes error handling to catch and log any issues related to setting up the GCP project or copying files to GCS. You can review the logs for debugging and monitoring purposes.

# Summary of the code

Configuration variables: <br />
&nbsp; GCSBUCKET: Specifies the destination GCS bucket. <br />
&nbsp; GCPPROJECT: Specifies the Google Cloud project ID. <br />
&nbsp; WATCHPATH: Specifies the path to monitor for files and directories. <br />
&nbsp; SLEEP: Specifies the sleep duration between iterations. <br />

set_gcp_project(project_name): A function to set the Google Cloud project using the gcloud command-line tool.

copy_to_gcs(src_path, dest_path): A function to copy files from the source path to the specified GCS destination path. It includes logic to ensure that the file has finished writing before copying it.

The main() function:
1. Initializes logging and sets the Google Cloud project.
2. Initializes previous_ts to 0.
3. Enters an infinite loop for continuous monitoring.
4. Inside the loop:<br />
   a. Checks if previous_ts is greater than 0 to determine if it's the initial iteration. <br />
   b. If it's the initial iteration (when previous_ts is 0), it logs an "Initial Looping" message and sets previous_ts to the current time.<br />
   c. If it's not the initial iteration, it collects a list of files and directories in the specified paths using glob.glob(WATCHPATH).<br />
   d. For each file or directory in the list, it checks their creation and modification times using os.path.getctime and os.path.getmtime.<br />
   e. If a file or directory has been created or modified since the previous iteration, it constructs a GCS path and issues a copy command using copy_to_gcs.<br />
   f. It then sleeps for a specified duration (SLEEP) before the next iteration.<br />
