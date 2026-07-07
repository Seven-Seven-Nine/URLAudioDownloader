from console_interface_lib import ConsoleInterface
from argparse import ArgumentParser

from src.url_audio_downloader.LinkExtractor import LinkExtractor
from src.url_audio_downloader.AudioDownloader import AudioDownloader

def initializing_arguments():
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument("--version", action="version", version="%(prog)s 1.0.1", help="Показать версию приложения.")
    parser.add_argument("--debug", action="store_true", help="Включить режим отладки.")
    parser.add_argument("--url", default="none", help="Ссылка на видео для скачивания аудио.")
    parser.add_argument("--file", default="none", help="Путь к файлу с ссылками.")
    parser.add_argument("--output", default="none", help="Путь, куда скачивать файлы, если не указать, то yt-dlp будет скачивать файлы в место запуска программы.")
    parser.add_argument("--playlist", action="store_true", help="Добавляет возможность скачивать плейлист, который может быть указан в ссылке.")
    parser.add_argument("--cookies", default="none", help="Указывает откуда брать cookies, нужно, если YouTube требует капчи или блокирует подозрительный трафик.")

    return parser.parse_args()

def run() -> None:
    args = initializing_arguments()

    ConsoleInterface.display_message("Запуск URL Audio Downloader")
    
    audioDownloader: AudioDownloader = AudioDownloader()

    if args.debug:
        ConsoleInterface.debugging_mode = True
        ConsoleInterface.display_message("Активирован режим отладки.", "debug")

        ConsoleInterface.display_message(f"Полученное значение аргумента \"--url\": {args.url}", "debug")
        ConsoleInterface.display_message(f"Полученное значение аргумента \"--file\": {args.file}", "debug")
        ConsoleInterface.display_message(f"Полученное значение аргумента \"--output\": {args.output}", "debug")
        ConsoleInterface.display_message(f"Полученное значение аргумента \"--playlist\": {args.playlist}", "debug")
        ConsoleInterface.display_message(f"Полученное значение аргумента \"--cookies\": {args.cookies}", "debug")
    
    if args.file != "none":
        ConsoleInterface.display_message("Получен путь к файлу.", "debug")
        linkExtractor: LinkExtractor = LinkExtractor(args.file)
        audioDownloader.start_download_audio(linkExtractor.get_array_links(), args.playlist, args.output, args.cookies)

    if args.url != "none":
        ConsoleInterface.display_message("Получен URL-адрес.", "debug")
        audioDownloader.start_download_audio([args.url], args.playlist, args.output, args.cookies)
        

    if args.output == "none" and args.url == "none":
        ConsoleInterface.display_message("Ошибка! Необходимо указать путь к файлу или URL-адрес видео. Введи --help для получения справочной информации о доступных аргументах.", "error")

if __name__ == "__main__":
    run()
