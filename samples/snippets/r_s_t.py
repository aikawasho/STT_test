import time

def rec_save():
    
    import pyaudio
    import numpy as np
    import wave
    import struct

    CHUNK = 4096
    FORMAT = pyaudio.paInt16 # 16bit
    CHANNELS = 1             # monaural
    fs = 16000
    rec_time = 3 # record time [s] 

    pa = pyaudio.PyAudio()

    stream = pa.open(rate=fs,
            channels=CHANNELS,
            format=FORMAT,
            input=True,
            frames_per_buffer=CHUNK)

    frames = []
    for i in range(0, int(fs / CHUNK * rec_time)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    pa.terminate()

    output_path =  "./" +str(int(time.time()))+ ".wav"
    wf = wave.open(output_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pa.get_sample_size(FORMAT))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    return output_path,fs

def upload_blob(bucket_name, source_file_name, destination_blob_name):

    from google.cloud import storage

    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )
    
def transcribe_file(speech_file,fs):
    """Transcribe the given audio file."""
    from google.cloud import speech
    import io

    client = speech.SpeechClient()

    # [START speech_python_migration_sync_request]
    # [START speech_python_migration_config]
    with io.open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=fs,
        language_code="ja-JP",
    )
    # [END speech_python_migration_config]

    # [START speech_python_migration_sync_response]
    response = client.recognize(config=config, audio=audio)

    # [END speech_python_migration_sync_request]
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
    # [END speech_python_migration_sync_response]

def transcribe_gcs(gcs_uri):
    """Transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech

    client = speech.SpeechClient()

    # [START speech_python_migration_config_gcs]
    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code="ja-JP",
    )
    # [END speech_python_migration_config_gcs]

    response = client.recognize(config=config, audio=audio)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))        
        
if __name__ == "__main__":
    import os
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/shota/Downloads/My First Project-06971ca6a80e.json'
    local_name,fs = rec_save()
    transcribe_file(local_name,fs)
    
