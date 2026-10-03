import os
from typing import Dict, Any
from app.utils.exceptions import TranscriptionError

_whisper_model = None

def get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        try:
            from faster_whisper import WhisperModel
            # Load the base model which is fast and lightweight
            _whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
        except ImportError:
            raise TranscriptionError("faster-whisper is not installed. Please install it to use transcription.", status_code=500)
        except Exception as e:
            raise TranscriptionError(f"Failed to load Whisper model: {str(e)}", status_code=500)
    return _whisper_model

class TranscriptionService:
    @staticmethod
    def transcribe_audio(file_path: str, separate_speakers: bool = False) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            raise TranscriptionError(f"Audio file not found: {file_path}", status_code=404)
        
        try:
            model = get_whisper_model()
            segments, info = model.transcribe(file_path, beam_size=5)
            
            result_segments = []
            full_text = []
            
            for segment in segments:
                # Basic separate speaker logic (simulated since faster-whisper doesn't do native diarization out of the box without Pyannote)
                speaker = "Speaker" if separate_speakers else None
                seg_dict = {
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text.strip()
                }
                if speaker:
                    seg_dict["speaker"] = speaker
                
                result_segments.append(seg_dict)
                full_text.append(segment.text.strip())
            
            return {
                "text": " ".join(full_text),
                "segments": result_segments
            }
        except Exception as e:
            raise TranscriptionError(f"Transcription failed: {str(e)}", status_code=500)

transcription_service = TranscriptionService()
