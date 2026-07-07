from console_interface_lib import ConsoleInterface
import sys

class LinkExtractor:
    """
    Класс для получения массива ссылок из файла.
    """
    def __init__(self, path_file_with_links: str) -> None:
        ConsoleInterface.display_message(f"Полученный путь к файлу с ссылками для скачивания аудио: \"{path_file_with_links}\".", "debug")

        self.__path_file_with_urls: str = path_file_with_links

        if LinkExtractor.__checking_duplicate_url(self.__path_file_with_urls):
            self.__array_links: list[str] = self.__parse_file_with_links()
        else:
            ConsoleInterface.display_message("Убери повторяющиеся URL из текстового файла для продолжения...", "error")
            sys.exit(1)

    @staticmethod
    def __checking_duplicate_url(path_file_with_urls) -> bool:
        with open(path_file_with_urls, "r", encoding="utf-8") as file:
            urls: list[str] = []
            for line in file:
                urls.append(line.strip())

        seen = set()
        duplicates = set()

        for url in urls:
            if url in seen:
                duplicates.add(url)
            else:
                seen.add(url)

        if duplicates:
            ConsoleInterface.display_message(f"Обнаружены повторяющиеся URL.", "warning")
            for duplicate in duplicates:
                ConsoleInterface.display_message(f"Повторяющийся URL: \"{duplicate}\".", "warning")
            return False
        else:
            return True

    def __parse_file_with_links(self) -> list[str]:
        """
        Метод для получения ссылок из текстового файла.

        Returns:
            list[str]: массив с ссылками.
        """
        links: list[str] = []
        try:
            with open(self.__path_file_with_urls, "r", encoding="utf-8") as file:
                for line in file:
                    link = line.strip()
                    if link:
                        links.append(link)
                        ConsoleInterface.display_message(f"Обнаружена ссылка: \"{link}\".", "debug")
        except FileNotFoundError:
            ConsoleInterface.display_message(f"Файл \"{self.__path_file_with_urls}\" не найден.", "error")
        except Exception as error:
            ConsoleInterface.display_message(f"Ошибка чтения файла: {error}", "error")
        return links
    
    def get_array_links(self) -> list[str]:
        return self.__array_links