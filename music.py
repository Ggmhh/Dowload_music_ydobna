import os
import pytube
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip
from rich.console import Console

console = Console()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def download_audio(youtube_url, output_path):
    try:
        yt = pytube.YouTube(youtube_url)
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(output_path=output_path)
        return True
    except pytube.exceptions.PytubeError as e:
        console.print(f"Ошибка при скачивании аудио: {e}", style="bold red")
        return False

def convert_mp4_to_mp3(input_path, output_folder):
    mp4_files = [file for file in os.listdir(input_path) if file.endswith(".mp4")]
    mp3_folder = os.path.join(output_folder, "mp3_files")  # Создаем подпапку "mp3_files" в output_folder
    os.makedirs(mp3_folder, exist_ok=True)  # Убеждаемся, что папка существует или создаем ее

    for mp4_file in mp4_files:
        mp3_file = mp4_file.replace(".mp4", ".mp3")
        mp4_path = os.path.join(input_path, mp4_file)
        mp3_path = os.path.join(mp3_folder, mp3_file)
        video = AudioFileClip(mp4_path)
        video.write_audiofile(mp3_path)
        video.close()

    return mp3_folder  # Возвращаем путь к созданной папке с MP3 файлами

def delete_all_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            console.print(f"Ошибка при удалении файла {file_path}: {e}", style="bold red")

def main():
    clear_console()  # Очистить консоль при запуске

    while True:
        additional_text = "|  \/  || | | |/ ___| |_ _| / ___|  |\n| |\/| || | | |\___ \  | | | |      |\n| |  | || |_| | ___) | | | | |___   |\n|_|  |_| \___/ |____/ |___| \____|  |\n"
        separator = "=" * 36
        styled_text = f"[red]{separator}\n{additional_text}{separator}[/red]\n[1] Скачать аудио по ссылке с ютуба\n[2] Преобразовать mp4 в mp3\n[3] Удалить все аудио файлы\n[4] Выйти"

        console.print(styled_text, end="\n")

        choice = input("Выберите опцию (1/2/3/4): ")

        if choice == '1':
            while True:
                youtube_url = input("Введите URL YouTube видео (или 'q' для выхода): ")
                if youtube_url.lower() == 'q':
                    break
                output_dir = "output"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                mp3_output = os.path.join(output_dir)
                if download_audio(youtube_url, mp3_output):
                    console.print(f"Аудио сохранено в: [cyan]{mp3_output}[/cyan]")
        elif choice == '2':
            input_dir = "output"
            output_dir = "output"
            mp3_folder = convert_mp4_to_mp3(input_dir, output_dir)
            console.print(f"MP4 файлы конвертированы в MP3 и сохранены в папке: [cyan]{mp3_folder}[/cyan]")
        elif choice == '3':
            output_folder = "output"
            delete_all_files_in_folder(output_folder)
            console.print(f"Все аудио файлы удалены из папки: [cyan]{output_folder}[/cyan]")
        elif choice == '4':
            break
        else:
            console.print("Неверный выбор. Пожалуйста, выберите 1, 2, 3 или 4.", style="bold red")

if __name__ == "__main__":
    main()
