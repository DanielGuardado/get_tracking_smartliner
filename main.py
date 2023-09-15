import pandas as pd
from ftp_downloader import FTPDownloader
import os
from datetime import datetime
from shipstation import mark_shipped, get_order_id
from sqlitedb import SQLiteDB
from email_helper import send_email
import traceback


def main():
    # Get current datetime in the desired format
    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    directory_path = os.path.join("tmp", current_datetime)

    ftp_downloader = FTPDownloader.from_config()
    downloaded_files = ftp_downloader.download_file(directory_path)

    db = SQLiteDB()
    existing_po_numbers = db.get_all_po_numbers()
    # Iterate through each .csv file in the directory
    # send_email("Test Run", "this is a test")
    if downloaded_files:
        for filename in os.listdir(directory_path):
            if filename.lower().endswith(".csv"):
                try:
                    file_path = os.path.join(directory_path, filename)

                    # Use pandas to read the .csv file
                    df = pd.read_csv(file_path)

                    # Iterate through each row and extract po_number and tracking_number
                    for _, row in df.iterrows():
                        po_number = str(row["po_number"])
                        tracking_number = row["tracking_number"]

                        # If the po_number is not in the database, mark as shipped and add to the database
                        if po_number not in existing_po_numbers:
                            print(
                                f"PO Number: {po_number}, Tracking Number: {tracking_number}"
                            )
                            order_id = get_order_id(po_number)
                            mark_shipped(order_id, tracking_number)
                            db.insert_data(po_number, tracking_number)
                except:
                    send_email(
                        f"Error getting tracking for file {filename}",
                        traceback.format_exc(),
                    )

                # Delete the file from the FTP server
                ftp_downloader.delete_file_from_ftp(filename)


if __name__ == "__main__":
    try:
        main()
    except:
        send_email("Error getting tracking", traceback.format_exc())
