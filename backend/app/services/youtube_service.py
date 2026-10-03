import re
import os
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from typing import Dict, List
from app.utils.exceptions import VideoSummarizerException, InvalidURLError

class YouTubeService:
    @staticmethod
    def extract_video_id(url: str) -> str:
        url = url.strip()
        regex = r"(?:https?://)?(?:www\.|m\.)?(?:youtube\.com/(?:watch\?.*?v=|embed/|v/|shorts/|live/)|youtu\.be/)([a-zA-Z0-9_-]{11})"
        match = re.search(regex, url)
        if match:
            return match.group(1)
        raise InvalidURLError("Invalid YouTube URL")

    @staticmethod
    def get_video_metadata(url: str) -> dict:
        video_id = YouTubeService.extract_video_id(url)
        # Try YouTube oEmbed first (instant, 100% reliable, no bot-blocks)
        try:
            import urllib.request
            import json
            oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
            req = urllib.request.Request(oembed_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                return {
                    "title": data.get("title", f"YouTube Video ({video_id})"),
                    "thumbnail": data.get("thumbnail_url", f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"),
                    "duration": 0,
                    "id": video_id
                }
        except Exception:
            pass

        # Fallback to yt-dlp
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'js_runtimes': {'node': {}},
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'ios', 'mweb']
                }
            }
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    "title": info.get("title", f"YouTube Video ({video_id})"),
                    "thumbnail": info.get("thumbnail", f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"),
                    "duration": info.get("duration", 0),
                    "id": info.get("id", video_id)
                }
        except Exception:
            # Fallback metadata if both network attempts encounter restrictions
            return {
                "title": f"YouTube Lecture ({video_id})",
                "thumbnail": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
                "duration": 0,
                "id": video_id
            }

    @staticmethod
    def get_transcript_from_captions(video_id: str) -> str:
        try:
            api = YouTubeTranscriptApi()
            transcript_obj = api.fetch(video_id)
            text = " ".join([
                item.text if hasattr(item, 'text') else item['text'] 
                for item in transcript_obj
            ])
            if text.strip():
                return text
        except Exception:
            pass

        try:
            api = YouTubeTranscriptApi()
            transcript_list = api.list(video_id)
            for t in transcript_list:
                fetched = t.fetch()
                text = " ".join([
                    item.text if hasattr(item, 'text') else item['text'] 
                    for item in fetched
                ])
                if text.strip():
                    return text
        except Exception:
            pass

        # Fallback 3: Try extracting subtitles via yt-dlp mobile clients
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'skip_download': True,
                'writesubtitles': True,
                'writeautomaticsub': True,
                'js_runtimes': {'node': {}},
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'ios', 'mweb']
                    }
                }
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
                subtitles = info.get('subtitles', {}) or info.get('automatic_captions', {})
                # Look for English, orig, or first available language
                sub_lang = None
                for lang in ['en', 'en-orig', 'en-US', 'en-GB']:
                    if lang in subtitles:
                        sub_lang = lang
                        break
                if not sub_lang and subtitles:
                    for k in subtitles.keys():
                        if k != 'live_chat':
                            sub_lang = k
                            break
                if sub_lang and subtitles.get(sub_lang):
                    formats = subtitles[sub_lang]
                    fmt = next((f for f in formats if f.get('ext') == 'json3'), formats[0])
                    import urllib.request
                    import json
                    req = urllib.request.Request(fmt['url'], headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(req, timeout=8) as r:
                        data = json.loads(r.read().decode('utf-8'))
                        events = data.get('events', [])
                        text_parts = []
                        for ev in events:
                            for seg in ev.get('segs', []):
                                text_parts.append(seg.get('utf8', ''))
                        full_text = " ".join("".join(text_parts).split())
                        if full_text.strip():
                            return full_text
        except Exception:
            pass

        return ""

    @staticmethod
    def download_audio(url: str, output_dir: str) -> str:
        os.makedirs(output_dir, exist_ok=True)
        ffmpeg_location = None
        try:
            import imageio_ffmpeg
            ffmpeg_location = imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:
            pass

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'js_runtimes': {'node': {}},
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'ios', 'mweb']
                }
            }
        }
        if ffmpeg_location:
            ydl_opts['ffmpeg_location'] = ffmpeg_location
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                prep_filename = ydl.prepare_filename(info)
                if ffmpeg_location:
                    base, _ = os.path.splitext(prep_filename)
                    mp3_file = f"{base}.mp3"
                    if os.path.exists(mp3_file):
                        return mp3_file
                return prep_filename
        except Exception as e:
            raise VideoSummarizerException(f"Failed to extract audio from video: {str(e)}", status_code=400)

    @staticmethod
    def get_playlist_videos(playlist_url: str) -> List[dict]:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'js_runtimes': {'node': {}},
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'ios', 'mweb']
                }
            }
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(playlist_url, download=False)
                if 'entries' in info:
                    return [{"url": f"https://www.youtube.com/watch?v={entry['id']}", "title": entry.get("title")} for entry in info['entries']]
                return []
        except Exception as e:
            raise VideoSummarizerException(f"Failed to fetch playlist: {str(e)}", status_code=400)

    @staticmethod
    def process_youtube_url(url: str, output_dir: str) -> dict:
        video_id = YouTubeService.extract_video_id(url)
        metadata = YouTubeService.get_video_metadata(url)
        
        transcript = YouTubeService.get_transcript_from_captions(video_id)
        audio_path = None
        if not transcript:
            audio_path = YouTubeService.download_audio(url, output_dir)
            # Transcription needs to be done by the caller using TranscriptionService
            
        return {
            "title": metadata["title"],
            "thumbnail_url": metadata["thumbnail"],
            "transcript": transcript,
            "audio_path": audio_path,
            "video_id": video_id
        }

youtube_service = YouTubeService()
