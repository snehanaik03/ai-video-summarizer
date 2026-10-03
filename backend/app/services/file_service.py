import os
import aiofiles
import subprocess
import fitz  # PyMuPDF
from fastapi import UploadFile
from app.utils.exceptions import FileProcessingError, UnsupportedFormatError

class FileService:
    @staticmethod
    async def save_upload_file(upload_file: UploadFile, destination: str) -> str:
        try:
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            async with aiofiles.open(destination, 'wb') as out_file:
                while content := await upload_file.read(1024 * 1024):  # 1MB chunks
                    await out_file.write(content)
            return destination
        except Exception as e:
            raise FileProcessingError(f"Failed to save file: {str(e)}")

    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            raise FileProcessingError(f"Failed to extract text from PDF: {str(e)}")

    @staticmethod
    def extract_text_from_image(file_path: str) -> str:
        # In a full implementation, you'd use Tesseract or similar. 
        # For now, returning a mock or calling an OCR service.
        return f"Mock extracted text from image {os.path.basename(file_path)}."

    @staticmethod
    def extract_audio_from_video(video_path: str, output_dir: str) -> str:
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.basename(video_path)
        name, _ = os.path.splitext(base_name)
        audio_path = os.path.join(output_dir, f"{name}.mp3")
        
        ffmpeg_cmd = "ffmpeg"
        try:
            import imageio_ffmpeg
            ffmpeg_cmd = imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:
            pass

        command = [
            ffmpeg_cmd, "-i", video_path,
            "-q:a", "0", "-map", "a", audio_path,
            "-y"
        ]
        
        try:
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return audio_path
        except subprocess.CalledProcessError as e:
            raise FileProcessingError(f"Failed to extract audio using ffmpeg: {e.stderr.decode()}")
        except FileNotFoundError:
            raise FileProcessingError("ffmpeg not found. Please install ffmpeg or imageio-ffmpeg.")

    @staticmethod
    def validate_file_type(filename: str, allowed_types: list) -> bool:
        ext = FileService.get_file_extension(filename)
        return ext.lower() in allowed_types

    @staticmethod
    def get_file_extension(filename: str) -> str:
        if not filename:
            return ""
        _, ext = os.path.splitext(filename)
        return ext.lower()

file_service = FileService()
