import sys
import yt_dlp

from console_interface_lib import ConsoleInterface
from argparse import ArgumentParser, Namespace
from yt_dlp.utils import escapeHTML
from pathlib import Path

from src.url_audio_downloader.UrlExtractor import UrlExtractor


class AudioDownloader:
    """
    Основной класс приложения.
    """
    def __init__(self) -> None:
        self.__args: Namespace = self.__initializing_arguments()

        self.__url: str | None = None
        self.__path_file: str | None = None

        # Пути к упакованным бинарным файлам.
        self.__base: Path = getattr(sys, "_MEIPASS", Path(sys.executable).parent)
        self.__path_to_ffmpeg: Path = Path(self.__base, "bin", "ffmpeg.exe")
        self.__path_to_deno: Path = Path(self.__base, "bin", "deno.exe")

        ConsoleInterface.display_message(f"Созданный путь к упакованному \"ffmpeg\": \"{self.__path_to_ffmpeg}\".", "debug")
        ConsoleInterface.display_message(f"Созданный путь к упакованному \"deno\": \"{self.__path_to_deno}\".", "debug")
    
    def __initializing_arguments(self) -> Namespace:
        """
        Инициализация аргументов приложения.

        Returns:
            Namespace: переданные аргументы при запуске приложения.
        """
        parser: ArgumentParser = ArgumentParser()

        parser.add_argument("--version", action="version", version="%(prog)s 1.0.4", help="Показать версию приложения.")
        parser.add_argument("--debug", action="store_true", help="Включить режим отладки.")
        parser.add_argument("--url", default="none", help="Ссылка на видео для скачивания аудио.")
        parser.add_argument("--file", default="none", help="Путь к файлу с ссылками.")
        parser.add_argument("--output", default="none", help="Путь, куда скачивать файлы, если не указать, то yt-dlp будет скачивать файлы в место запуска программы.")
        parser.add_argument("--playlist", action="store_true", help="Добавляет возможность скачивать плейлист, который может быть указан в ссылке.")
        parser.add_argument("--cookies", default="none", help="Название браузера, например \"--cookies firefox\" или путь к файлу с cookies. Необходимо для загрузки закрытых плейлистов или если YouTube нашёл подозрительный трафик.")
    
        return parser.parse_args()

    def processing_argument_values(self) -> None:
        """
        Обработка полученных значений аргументов.
        """
        if self.__args.debug:
            ConsoleInterface.debugging_mode = True
            ConsoleInterface.display_message("Активирован режим отладки.", "debug")

            ConsoleInterface.display_message(f"Полученное значение аргумента \"--url\": {self.__args.url}", "debug")
            ConsoleInterface.display_message(f"Полученное значение аргумента \"--file\": {self.__args.file}", "debug")
            ConsoleInterface.display_message(f"Полученное значение аргумента \"--output\": {self.__args.output}", "debug")
            ConsoleInterface.display_message(f"Полученное значение аргумента \"--playlist\": {self.__args.playlist}", "debug")
            ConsoleInterface.display_message(f"Полученное значение аргумента \"--cookies\": {self.__args.cookies}", "debug")

        if self.__args.file != "none":
            ConsoleInterface.display_message("Получен путь к файлу.", "debug")
            self.__path_file = self.__args.file
            if not self.__path_file is None:
                urlExtractor: UrlExtractor = UrlExtractor(self.__path_file)
                self.__download_audio(urlExtractor.get_list_url())
            else:
                ConsoleInterface.display_message("Ошибка! Аргумент \"--file\" не был корректно передан.", "error")
                sys.exit(1)

        if self.__args.url != "none":
            ConsoleInterface.display_message("Получен URL-адрес.", "debug")
            self.__url = self.__args.url
            if not self.__url is None: 
                self.__download_audio([self.__url])
            else:
                ConsoleInterface.display_message("Ошибка! Аргумент \"--url\" не был корректно передан.", "error")
                sys.exit(1)
                

        if self.__args.output == "none" and self.__args.url == "none":
            ConsoleInterface.display_message("Ошибка! Необходимые аргументы \"--file\" и \"--url\" не обнаружены.", "error")
            sys.exit(1)

    def __download_audio(self, list_urls: list[str]) -> None:
        """
        Основной метод запуска скрипта скачивания аудио-файлов.

        Args:
            list_urls (list[str]): список всех URL для загрузки аудио.
        """
        ydl_options: yt_dlp._Params = {
            "format": "bestaudio/best",
            "writethumbnail": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": 0,  # Аналог --audio-quality 0
                },
                {
                    "key": "FFmpegMetadata",
                    "add_chapters": True,
                    "add_metadata": True,
                },
                {
                    "key": "FFmpegThumbnailsConvertor", 
                    "format": "png"
                },
                {
                    "key": "EmbedThumbnail"
                }
            ]
        }

        if not self.__args.debug:
            ydl_options.update({"quiet": True})

        if self.__args.output != "none":
            out_dir: Path = Path(self.__args.output)
            out_dir.mkdir(parents=True, exist_ok=True)
            ydl_options.update({"outtmpl": f"{out_dir}/%(title)s.%(id)s.%(ext)s"})
            ConsoleInterface.display_message("Добавление опции загрузки аудио-файлов в определённое место.", "debug")

        if self.__args.cookies != "none":
            cookies_val: str = self.__args.cookies
            if Path(cookies_val).exists() or cookies_val.endswith('.txt') or '\\' in cookies_val or '/' in cookies_val:
                # Это файл cookies
                ydl_options.update({"cookiefile": cookies_val})
                ConsoleInterface.display_message(f"Добавлена опция использования файла cookies: {cookies_val}", "debug")
            elif cookies_val in ("edge", "chrome", "chromium"):
                ConsoleInterface.display_message("Cookies из chromium-браузеров не могут быть изъяты yt-dlp из-за усиленного шифрования.", "warning")
            else:
                ydl_options.update({"cookiesfrombrowser": (cookies_val,)})
                ConsoleInterface.display_message(f"Добавлена опция получения cookies из браузера: {cookies_val}", "debug")

        if self.__args.playlist:
            ydl_options.update({"noplaylist": False})
            ConsoleInterface.display_message("Добавление опции принудительной загрузки плейлиста.", "debug")
        else:
            ydl_options.update({"noplaylist": True})
            ConsoleInterface.display_message("Добавление опции отключения загрузки плейлиста.", "debug")

        if getattr(sys, "frozen", False):
            ConsoleInterface.display_message("Запущена сборка, добавление опций использования упакованных зависимостей.", "debug")
            ydl_options.update({
                "js_runtimes": {
                    "deno": {
                        "path": str(self.__path_to_deno)
                    }
                },
                "ffmpeg_location": str(self.__path_to_ffmpeg)
            })

        for url in list_urls:
            ConsoleInterface.display_message(f"Количество ссылок для загрузки аудио: {len(list_urls)}.", "debug")
            
            if self.__args.playlist:
                ConsoleInterface.display_message(f"Загрузка плейлиста по ссылке – \"{url}\".")
            else:
                ConsoleInterface.display_message(f"Загрузка аудио по ссылке – \"{url}\".")

            for attempt_download_audio in range(4):
                try:
                    with yt_dlp.YoutubeDL(ydl_options) as ydl:
                        ydl.download(url_list=[url])
                    ConsoleInterface.display_message("Аудио загружено успешно.")
                    break
                except KeyboardInterrupt:
                    ConsoleInterface.display_message("Загрузка аудио прервано пользователем (ctrl + c).")
                    sys.exit(0)
                except Exception as error:
                    ConsoleInterface.display_message(f"Попытка {attempt_download_audio + 1}/4 не удалась: {error}", "error")
