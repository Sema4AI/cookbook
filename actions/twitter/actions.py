from sema4ai.actions import action
import urllib.parse


@action
def create_tweet_draft(tweet_text: str) -> str:
    """
    Create Twitter draft links. Takes in a suggested tweet text and returns a link that points user directly to Twitter to modify and post the tweet.

    Args:
        tweet_text: The text for the tweets. May contain emojis and links. For example "Check this out! 😃 https://example.com."

    Returns:
        str: A link to twitter to post the tweet.

    """
    base_url = "https://twitter.com/intent/tweet?text="
    encoded_text = urllib.parse.quote(tweet_text, safe='')
    tweet_draft_url = base_url + encoded_text
    return tweet_draft_url
