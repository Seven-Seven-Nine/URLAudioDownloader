import shutil
import subprocess
import time
from console_interface_lib import ConsoleInterface

class AudioDownloader:
    """
    Класс для работы с yt-dlp. Контролирует работу yt-dlp и вызывает запуск процесса.
    """
    def __init__(self) -> None:
        self.__checking_yt_dlp: bool = AudioDownloader.__check_executable("yt-dlp")
        self.__checking_ffmpeg: bool = AudioDownloader.__check_executable("ffmpeg")
        self.__checking_deno: bool = AudioDownloader.__check_executable("deno")

    @staticmethod
    def __check_executable(name: str) -> bool:
        """
        Метод для проверки зависимостей в PATH.

        Args:
            name (str): название пакета, программы или другое, что нужно проверить в PATH.

        Returns:
            bool: True, если есть в PATH. Аналогично с False.
        """
        return shutil.which(name) is not None

    def start_download_audio(self, urls: list[str], playlist: bool, path_output: str, cookies: str) -> None:
        """
        Метод скачивания аудио с ссылок.

        Args:
            urls (list[str]): список ссылок для скачивания аудио.
            playlist (bool, optional): нужно ли скачивать плейлист по ссылке или нет. По умолчанию False.
            path_output (str | None, optional): место скачивания файлов. По умолчанию None.
        """
        ConsoleInterface.display_message(f"Результат проверки наличия \"yt-dlp\": {self.__checking_yt_dlp}.", "debug")
        ConsoleInterface.display_message(f"Результат проверки наличия \"ffmpeg\": {self.__checking_ffmpeg}.", "debug")
        ConsoleInterface.display_message(f"Результат проверки наличия \"deno\": {self.__checking_deno}.", "debug")

        if not (self.__checking_yt_dlp and self.__checking_ffmpeg and self.__checking_deno):
            ConsoleInterface.display_message("Для функционирования нет необходимых зависимостей, проверь установку \"yt-dlp\", \"ffmpeg\" и \"deno\".", "error")
            return
        
        MAX_ATTEMPTS: int = 6 # Количество повторений
        RETRY_DELAY: int = 5 # Секунды, через которое начнётся попытка скачивания

        for url in urls:
            attempt: int = 0
            success: bool = False

            while attempt < MAX_ATTEMPTS and not success:
                attempt += 1
                ConsoleInterface.display_message(f"Попытка №{attempt} для скачивания аудио по ссылке: \"{url}\".")

                args: list[str] = [
                    "yt-dlp",
                    "-f", "bestaudio",
                    "--extract-audio",
                    "--audio-format", "mp3",
                    "--audio-quality", "0",
                    "--sleep-interval", "5", "--max-sleep-interval", "10",
                    "--embed-thumbnail", "--add-metadata",
                ]

                if path_output != "none":
                    args.append("-P")
                    args.append(path_output)
                
                if playlist == False:
                    args.append("--no-playlist")

                if cookies != "none":
                    args.append("--cookies-from-browser")
                    args.append(cookies)

                args.append(url)

                try:
                    result = subprocess.run(args, check=True, capture_output=True, text=True)
                    success = True
                    ConsoleInterface.display_message(f"Скачивание аудио по ссылке \"{url}\" успешно завершено.")
                except subprocess.CalledProcessError as error:
                    ConsoleInterface.display_message(f"Ошибка скачивания аудио при попытке №{attempt} для ссылки \"{url}\": {error.stderr}", "warning")
                    if attempt < MAX_ATTEMPTS:
                        ConsoleInterface.display_message(f"Повтор через {RETRY_DELAY} секунд...")
                        time.sleep(RETRY_DELAY)
            if not success:
                ConsoleInterface.display_message(f"Не удалось скачать аудио по ссылке \"{url}\" после {MAX_ATTEMPTS} попыток.", "error")
