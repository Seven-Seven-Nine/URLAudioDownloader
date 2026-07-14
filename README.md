# URL Audio Downloader

Консольное приложение для простой загрузки аудио с YouTube. В исполняемый файл включены все необходимые зависимости: **deno**, **ffmpeg**, **yt-dlp**.

## Пример работы приложения

*P.S. нужно указывать абсолютные (полные) пути к текстовому файлу и место скачивания аудио файлов.*

1) Через файл со ссылками:

- Создай текстовый файл с любым названием, например: *urls.txt*.
- Добавляй URL-адреса на видео через каждую новую строчку:

```
https://www.youtube.com/watch?v=...
https://www.youtube.com/watch?v=...
https://www.youtube.com/watch?v=...
https://www.youtube.com/watch?v=...
https://www.youtube.com/watch?v=...
```
- Через запускаемый файл выполни команду: `./URLAudioDownloader --file "полный/путь/к/файлу.txt" --output "полный/путь/к/загрузке/аудио/" --mp3`.

2) Напрямую через URL-адрес видео:

- Запусти команду: `./URLAudioDownloader --url "https://www.youtube.com/watch?v=..." --output "полный/путь/к/загрузке/аудио/"`.

## Доступные аргументы приложения

- `--debug` — включает режим отладки.
- `--url "ссылка"` — указывается ссылка на видео для скачивания аудио.
- `--file "путь_к_файлу"` — указывается путь к текстовому файлу с URL-адресами.
- `--output "путь_к_папке_установки"` — указывается путь к месту установки.
- `--playlist` — добавляет возможность скачивать плейлист, который может быть указан в ссылке.
- `--cookies имя_браузера или путь_к_файлу_с_cookies` — указывает откуда yt-dlp будет брать cookies, нужно, чтобы YouTube не требовал теста на бота или если он блокирует подозрительный трафик, а так же для загрузки закрытого плейлиста. Можно указать имя браузера, откуда yt-dlp автоматически возьмёт cookies, но с chromium-браузерами работает плохо из-за усиленной защиты cookies, на firefox работает без проблем. Чтобы использовать cookies с chromium-браузеров можно экспортировать через расширения файл с cookies и указать путь до этого файла, чтобы yt-dlp использовал cookies из этого файла.

## Сборка

Установить *Pyinstaller* и выполнить команду в корне проекта:
- *Windows* – `pyinstaller --onefile --name="URLAudioDownloaderWindows" --add-binary "X:\путь\к\deno\deno.exe:bin" --add-binary "X:\путь\к\ffmpeg\bin\ffmpeg.exe:bin" --add-binary "X:\путь\к\ffmpeg\bin\ffplay.exe:bin" --add-binary "X:\путь\к\ffmpeg\bin\ffprobe.exe:bin" --icon "X:\путь\к\URLAudioDownloader\src\url_audio_downloader\assets\icon-url-audio-downloader.ico" main.py`.
- *Linux* –`pyinstaller --onefile --name="URLAudioDownloaderLinux" --add-binary "/путь/к/deno:bin" --add-binary "/путь/к/ffmpeg/ffmpeg:bin" --add-binary "/путь/к/ffmpeg/ffplay:bin" --add-binary "/путь/к/ffmpeg/ffprobe:bin" --icon "X:/путь/к/URLAudioDownloader/src/url_audio_downloader/assets/icon-url-audio-downloader.ico" main.py`.
