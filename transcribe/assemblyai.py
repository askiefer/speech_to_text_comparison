import argparse
import os
import time
# import utils
from transcribe import utils
from transcribe.compare import compare
import json
import requests

# from transcribe.load import get_video_filepaths


api_key = os.getenv("AAI_API_KEY")
header = {
    'authorization': api_key,
    'content-type': 'application/json'
}


def run(filepath):
    videos = get_video_filepaths(filepath)
    endpoints = {}
    for bill_id, video in videos.items():
        endpoint = transcribe(bill_id, video)
        endpoints[bill_id] = endpoint
    return endpoints


def get_transcript(file):
    bill_id = "CA_201520160AB195"
    polling_endpoints = {
        bill_id: "https://api.assemblyai.com/v2/transcript/rbxghrrklh-1a3e-4978-b32d-226f603ad8e9"
    }
    polling_endpoint = polling_endpoints[bill_id]
    res = get_sentences(polling_endpoint)
    confidence = res["confidence"]
    groundtruth, assembly = compare(bill_id)
    return groundtruth, assembly, confidence


def transcribe(bill_id: str, audio_file: str):
    # Create header with authorization along with content-type
    filename = download_file(bill_id, audio_file)

    # split the video
    upload_url = utils.upload_file(filename, header)
    start_time = time.time()
    # Request a transcription
    transcript_response = utils.request_transcript(upload_url, header)
    # Create a polling endpoint that will let us check when the transcription is complete
    polling_endpoint = utils.make_polling_endpoint(transcript_response)
    print(polling_endpoint)  # https://api.assemblyai.com/v2/transcript/rbxghrrklh-1a3e-4978-b32d-226f603ad8e9
    # Wait until the transcription is complete
    utils.wait_for_completion(polling_endpoint, header)
    end_time = time.time()
    print(f"Transcription time: {(end_time - start_time)}", )
    return polling_endpoint


# Get the sentences of the transcript
def get_sentences(polling_endpoint):
    sentences_response = requests.get(polling_endpoint + "/sentences", headers=header)
    sentences_response = sentences_response.json()
    return sentences_response


# if __name__ == "__main__":
#     endpoint = "https://api.assemblyai.com/v2/transcript/rbxghrrklh-1a3e-4978-b32d-226f603ad8e9"
#     print(get_sentences(endpoint))
