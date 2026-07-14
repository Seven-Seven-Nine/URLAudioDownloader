from src.url_audio_downloader.AudioDownloader import AudioDownloader
from console_interface_lib import ConsoleInterface

def run() -> None:
    ConsoleInterface.display_message("Запуск URL Audio Downloader")
    
    audioDownloader: AudioDownloader = AudioDownloader()
    audioDownloader.processing_argument_values()

if __name__ == "__main__":
    run()
