from console_interface_lib import ConsoleInterface

class LinkExtractor:
    """
    Класс для получения массива ссылок из файла.
    """
    def __init__(self, path_file_with_links: str) -> None:
        ConsoleInterface.display_message(f"Полученный путь к файлу с ссылками для скачивания аудио: \"{path_file_with_links}\".", "debug")

        self.__path_file_with_links: str = path_file_with_links
        self.__array_links: list[str] = self.__parse_file_with_links()

    def __parse_file_with_links(self) -> list[str]:
        """
        Метод для получения ссылок из текстового файла.

        Returns:
            list[str]: массив с ссылками.
        """
        links: list[str] = []
        try:
            with open(self.__path_file_with_links, "r", encoding="utf-8") as file:
                for line in file:
                    link = line.strip()
                    if link:
                        links.append(link)
                        ConsoleInterface.display_message(f"Обнаружена ссылка: \"{link}\".", "debug")
        except FileNotFoundError:
            ConsoleInterface.display_message(f"Файл \"{self.__path_file_with_links}\" не найден.", "error")
        except Exception as error:
            ConsoleInterface.display_message(f"Ошибка чтения файла: {error}", "error")
        return links
    
    def get_array_links(self) -> list[str]:
        return self.__array_links