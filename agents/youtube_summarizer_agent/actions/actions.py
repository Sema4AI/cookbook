# Modified_YouTube_Agent Action for Sema4.ai Action Server

from sema4ai.actions import action
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_search import YoutubeSearch

import re

def _extract_youtube_id(url):
    # Regular expression patterns to match various YouTube URL formats
    patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([^&]+)',  # Matches https://www.youtube.com/watch?v=VIDEO_ID
        r'(?:https?://)?(?:www\.)?youtu\.be/([^?]+)',  # Matches https://youtu.be/VIDEO_ID
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([^?]+)',  # Matches https://www.youtube.com/embed/VIDEO_ID
        r'(?:https?://)?(?:www\.)?youtube\.com/v/([^?]+)'  # Matches https://www.youtube.com/v/VIDEO_ID
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

@action(is_consequential=False)
def search(search_term: str, max_results: int = 3) -> str:
    """Searches for the YouTube videos with a search keyword.

    Args:
        search_term: A search term for the Youtube video search, example: "Agentic Automation"
        max_results: How many results to return, default 3.

    Returns:
        Youtube video links that match the search criteria. The return value is a json string.
    """
    try:
        results = YoutubeSearch(search_term, max_results=max_results).to_json()
        return results
    except Exception as e:
        return f"An error occurred: {str(e)}"

@action(is_consequential=False)
def get_transcript(video_url: str) -> str:
    """Extracts the transcription of a Youtube video,. Only works if subtitles or captions are available for the video.

    Args:
        video_url: Youtube video URL as a complete URL, example: "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"

    Returns:
        Complete transcription of the youtube video, including the timestamps
    """

    # Extract video ID from the URL
    video_id = _extract_youtube_id(video_url)

    if video_id is None:
        return "Could not extract YouTube video ID from the given URL."

    try:
        # Fetching the transcript
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

        # Function to format timestamps
        def format_time(seconds):
            minutes, seconds = divmod(int(seconds), 60)
            hours, minutes = divmod(minutes, 60)
            
            if hours > 0:
                return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                return f"{minutes:02d}:{seconds:02d}"
            
        # Concatenate all parts to create a full transcript with formatted timestamps
        transcript = '\n'.join([
            f"{format_time(entry['start'])} - {format_time(entry['start'] + entry['duration'])}: {entry['text']}"
            for entry in transcript_list
        ])
        return transcript
    
    except Exception as e:
        return f"An error occurred: {str(e)}"