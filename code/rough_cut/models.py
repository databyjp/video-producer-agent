"""
Data models shared across all pipeline stages.

TranscriptWord      → one word from Whisper (with timestamps + confidence)
TranscriptSegment   → one Whisper segment (sentence-ish chunk of words)
KeepSegment         → a time range the LLM decided to keep
EditPlan            → the full set of keep segments + summary stats
"""

from dataclasses import dataclass, field


@dataclass
class TranscriptWord:
    """A single word as returned by faster-whisper word_timestamps."""
    word: str           # raw word string (may have leading space, punctuation)
    start: float        # start time in seconds
    end: float          # end time in seconds
    probability: float  # Whisper confidence 0.0–1.0


@dataclass
class TranscriptSegment:
    """One Whisper segment (typically a sentence or short phrase)."""
    id: int
    start: float        # segment start in seconds
    end: float          # segment end in seconds
    text: str           # full segment text
    words: list[TranscriptWord]
    avg_logprob: float  # average log-probability (quality indicator)
    no_speech_prob: float  # probability this segment is silence/noise


@dataclass
class KeepSegment:
    """A contiguous range of the source video that should appear in the cut."""
    start: float    # seconds into source video
    end: float      # seconds into source video
    label: str      # short snake_case label (from LLM), e.g. "intro_hook"
    reason: str     # LLM's one-sentence explanation for this segment

    @property
    def duration(self) -> float:
        return self.end - self.start


@dataclass
class EditPlan:
    """The complete edit decision list produced by the retake detector."""
    keep_segments: list[KeepSegment]
    source_duration: float  # total raw video duration in seconds

    @property
    def kept_duration(self) -> float:
        return sum(s.duration for s in self.keep_segments)

    @property
    def cut_duration(self) -> float:
        return self.source_duration - self.kept_duration

    @property
    def kept_pct(self) -> float:
        if self.source_duration == 0:
            return 0.0
        return (self.kept_duration / self.source_duration) * 100
