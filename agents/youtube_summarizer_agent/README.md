# Youtube Summarizer Agent

## **Objective**
This agent is designed to create comprehensive summaries of YouTube tech videos. It starts by accepting a search query from the user. For these search queries, it presents the top 10 results and lets the user select a specific video. The agent then generates a high-level summary of the entire video, followed by a more detailed segment-by-segment breakdown. These segments are identified based on the video's narrative structure and content. For each segment, the agent provides start and end timestamps, keywords or a one-line summary, and relevant articles from tech publications like Medium or TechCrunch. This thorough analysis allows users to quickly grasp the video's key points, navigate to specific sections of interest, and explore related content for further study or reference.

## **Outline of Agent Process:**
1. Take a video search string from the user.
2. If it is a search string, show the top 10 results and get the video that the user wants from it.
Give a top-level summary, and give a segment-wise summary. Each segment can be based on the overall transcript, and how the video is telling the overall story.
3. Identify those key segments, and give the start and end times of such segments for that video.
4. For each segment, find a set of keywords or one-line summary and a browse of Medium or TechCrunch articles.
5. Share all results back to the user for further study or manual reference.