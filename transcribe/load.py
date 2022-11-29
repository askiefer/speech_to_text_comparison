import csv
import time

from typing import Dict


def get_video_filepaths(filename: str) -> Dict:
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        video_filepaths = {}
        times = {}
        for i, row in enumerate(reader):
            bill_id = row["Bill ID"]
            if not bill_id in video_filepaths:
                video_filepath = row["Link to video"]
                video_filepath = video_filepath.split("#")
                video_filepaths[bill_id] = video_filepath[0]
        import pdb;
        pdb.set_trace()
        print("Number of videos:", len(video_filepaths))
        time.sleep(1)
    return video_filepaths, endtimes


def get_groundtruth_sentences() -> str:
    filename = "../DD_transcripts_serota.csv"
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        # final_str = ""
        # for row in reader:
        #     bill_id = row["Bill ID"]
        #     if bill_id:
        #         final_str += row["Utterance"].strip()
    return reader


if __name__ == "__main__":
    filepath = "../DD_transcripts_serota.csv"
    _, endtimes = get_video_filepaths(filepath)
    print(endtimes)
