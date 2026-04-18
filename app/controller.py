import glob
import os
from app.pipeline import process_pdf


def run_app(config):

    os.makedirs(config["input_folder"], exist_ok=True)
    os.makedirs(config["output_folder"], exist_ok=True)
    os.makedirs(config["log_folder"], exist_ok=True)

    pdf_files = glob.glob(
        os.path.join(config["input_folder"], "*.pdf")
    )

    if not pdf_files:
        print("No PDFs found.")
        return

    for pdf in pdf_files:
        process_pdf(pdf, config)

    print("All PDFs processed.")