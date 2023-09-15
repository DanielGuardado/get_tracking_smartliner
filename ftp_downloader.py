from ftplib import FTP
import os
from config import ftp_data


class FTPDownloader:
    def __init__(self, host, username, password, source_path, port=21):
        self.host = host
        self.username = username
        self.password = password
        self.source_path = source_path
        self.port = port

    def delete_file_from_ftp(self, filename):
        """
        Deletes a specific file from the FTP server.

        :param filename: The name of the file to be deleted.
        """
        with FTP() as ftp:
            # Connect to the server
            ftp.connect(host=self.host, port=self.port)
            ftp.login(user=self.username, passwd=self.password)

            # Change to the source directory on the FTP server
            ftp.cwd(self.source_path)

            # Delete the file
            ftp.delete(filename)
            print(f"{filename} deleted from FTP server.")

    def download_file(self, dest_directory):
        """
        Downloads all .csv files from the specified source_path on the FTP server.

        :param dest_directory: The local directory where the files will be downloaded to.
        """
        with FTP() as ftp:
            # Connect to the server
            ftp.connect(host=self.host, port=self.port)
            ftp.login(user=self.username, passwd=self.password)

            # Change to the source directory on the FTP server
            ftp.cwd(self.source_path)

            # List all files in the source_path and filter for .csv files
            all_files = ftp.nlst()
            csv_files = [f for f in all_files if f.lower().endswith(".csv")]

            # If there are no .csv files, return without doing anything
            if not csv_files:
                print("No .csv files to download.")
                return

            # Ensure the destination directory exists
            if not os.path.exists(dest_directory):
                os.makedirs(dest_directory)

            for filename in csv_files:
                # Construct the full local path for the file
                local_file = os.path.join(dest_directory, os.path.basename(filename))

                # Download the file
                with open(local_file, "wb") as file:
                    ftp.retrbinary(f"RETR {filename}", file.write)

                print(f"{filename} downloaded successfully to {local_file}")
            return True

    @staticmethod
    def from_config():
        return FTPDownloader(
            ftp_data["host"],
            ftp_data["username"],
            ftp_data["password"],
            ftp_data["source_path"],
        )
