import os
import sys
import subprocess
import time
import glob
import logging

GCSBUCKET = "gs://$BUCKET_NAME/"
GCPPROJECT = "$PROJECT_ID"
WATCHPATH = "/PATH/"
#WATCHPATH = "/var/lib/kubelet/pods/*/volumes/kubernetes.io~empty-dir/heap-dumps/*/*/*"
SLEEP = 30

def set_gcp_project(project_name):
    try:
        subprocess.check_call(["gcloud", "config", "set", "project", project_name], stderr=subprocess.STDOUT)
        logging.info("Project set to: " + project_name)
    except subprocess.CalledProcessError as e:
        logging.critical("Something went wrong while setting up the gcp-project: " + e.output.decode())

# Create an empty set to track copied file paths
copied_files = set()

def copy_to_gcs(src_path, dest_path):
    try:
        file_size = os.path.getsize(src_path)
        while True:
            time.sleep(2)
            new_size = os.path.getsize(src_path)
            if new_size == file_size:
                break  # Exit the loop when the file size remains the same
            file_size = new_size

        # Check if the file has been copied before
        if src_path not in copied_files:
            subprocess.check_call(["/google-cloud-sdk/bin/gsutil", "cp", src_path, dest_path], stderr=subprocess.STDOUT)
            logging.info("Copy successful: " + src_path + " -> " + dest_path)
            # Add the file path to the set of copied files
            copied_files.add(src_path)
        else:
            logging.info("File already copied: " + src_path)
    except subprocess.CalledProcessError as e:
        logging.error(e.output.decode())

def main():
    logging.basicConfig(stream=sys.stdout, format='%(asctime)s.%(msecs)03d %(name)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)

    set_gcp_project(GCPPROJECT)

    previous_ts = 0

    while True:
        if previous_ts > 0:
            current_time = time.time()
            dirlist = [path for path in glob.glob(WATCHPATH)]

            for file in dirlist:
                file_ctime = os.path.getctime(file)
                file_mtime = os.path.getmtime(file)

                if file_ctime > previous_ts or file_mtime > previous_ts:
                    dir_name = os.path.basename(os.path.dirname(file))
                    file_name = os.path.basename(file)
                    dir_file_name = dir_name + "_" + file_name
                    gcs_path = GCSBUCKET + dir_file_name
                    logging.info("Issuing Command: gsutil cp " + file + " " + gcs_path)
                    copy_to_gcs(file, gcs_path)

            time.sleep(SLEEP)

        else:
            logging.info("Initial Looping")
            current_time = time.time()

        previous_ts = current_time

if __name__ == "__main__":
    main()
