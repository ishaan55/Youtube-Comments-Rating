import googleapiclient.discovery
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('GOOGLE_API_KEY')
VIDEO_ID = 'P8p3zXSzY4c'

youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEY)

# Get comments for the video
def get_video_comments(VIDEO_ID):
    comments = []
    results = youtube.commentThreads().list(videoId=VIDEO_ID, part='snippet', textFormat='plainText').execute()

    while results:
        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        # Check if there are more comments to retrieve
        if 'nextPageToken' in results:
            # kwargs['pageToken'] = results['nextPageToken']
            results = youtube.commentThreads().list(videoId=VIDEO_ID, part='snippet', textFormat='plainText', pageToken=results['nextPageToken']).execute()
        else:
            break

    return comments

if __name__ == '__main__':
    try:
        comments = get_video_comments(VIDEO_ID)
        print(comments)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
