import requests
import time
import urllib.request


upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"


# Helper for `upload_file()`
def _read_file(filename, chunk_size=5242880):
    with open(filename, "rb") as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            yield data
    return f


def download_file(bill_id, audio_file):
    filename = f'{bill_id}.mp4'
    urllib.request.urlretrieve(audio_file, filename)
    return filename


# Uploads a file to AAI servers
def upload_file(filename, header):
    filename = 'CA_201520160AB195.mp4'
    upload_response = requests.post(
        upload_endpoint,
        headers=header, data=_read_file(filename)
    )
    return upload_response.json()


# Request transcript for file uploaded to AAI servers
def request_transcript(upload_url, header):
    transcript_request = {
        'audio_url': upload_url['upload_url'],
        "speaker_labels": True
    }
    transcript_response = requests.post(
        transcript_endpoint,
        json=transcript_request,
        headers=header
    )
    return transcript_response.json()


# Make a polling endpoint
def make_polling_endpoint(transcript_response):
    polling_endpoint = "https://api.assemblyai.com/v2/transcript/"
    polling_endpoint += transcript_response['id']
    return polling_endpoint


# Wait for the transcript to finish
def wait_for_completion(polling_endpoint, header):
    while True:
        polling_response = requests.get(polling_endpoint, headers=header)
        polling_response = polling_response.json()

        if polling_response['status'] == 'completed':
            break

        time.sleep(5)
