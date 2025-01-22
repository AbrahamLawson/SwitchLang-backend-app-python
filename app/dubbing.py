import requests 
from typing import Optional
from elevenlabs.client import ElevenLabs
import time 
import os

client = ElevenLabs(api_key="sk_2afdeda10e937d19e62e25872d4b31fc70f8cfed638c6f8a")

def wait_for_dubbing_completion(dubbing_id: str) -> bool:
    MAX_ATTEMPTS = 120
    CHECK_INTERVAL = 10  # In seconds
    
    for _ in range(MAX_ATTEMPTS):
        metadata = client.dubbing.get_dubbing_project_metadata(dubbing_id)
        
        if metadata.status == 'dubbed':
            return True
        elif metadata.status == 'dubbing':
            print(
                "Dubbing in progress... Will check status again in",
                CHECK_INTERVAL,
                "seconds.",
            )
            time.sleep(CHECK_INTERVAL)
        else:
            print("Dubbing failed:", metadata.error_message)
            return False
    print("Dubbing timed out")
    return False

def download_dubbed_file(dubbing_id: str, language_code: str) -> str: 
    dir_path = f"data/{dubbing_id}"
    os.makedirs(dir_path, exist_ok=True)
    
    file_path = f"{dir_path}/{language_code}.mp4"
    with open(file_path, "wb") as file: 
        for chunk in client.dubbing.get_dubbed_file(dubbing_id, language_code): 
            file.write(chunk)
    return file_path
            
            
def create_dub_from_url(
    source_url: str,
    source_language: str,
    target_language: str,
) -> Optional[str]:
        
    response = client.dubbing.dub_a_video_or_an_audio_file(
        source_url=source_url,
        target_lang=target_language,
        mode ='automatic',
        source_lang=source_language,
        num_speakers=1,
        watermark=True
    )
    
    dubbing_id = response.dubbing_id
    
    if wait_for_dubbing_completion(dubbing_id):
        output_file_path = download_dubbed_file(dubbing_id, target_language)
        return output_file_path
    else:
        return None