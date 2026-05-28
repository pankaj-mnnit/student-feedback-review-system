from textblob import TextBlob


def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text using TextBlob.
    Returns a tuple: (sentiment_label, polarity_score)

    Classification Rules (comment-based only, NOT rating-based):
    - polarity > 0.1: positive
    - polarity < -0.1: negative
    - otherwise: neutral

    Error Handling:
    - Empty/blank text returns neutral.
    - If TextBlob fails for any reason, returns neutral and logs the error.
    """
    if not text or not text.strip():
        return "neutral", 0.0

    try:
        blob = TextBlob(text.strip())
        polarity = blob.sentiment.polarity

        if polarity > 0.1:
            label = "positive"
        elif polarity < -0.1:
            label = "negative"
        else:
            label = "neutral"

        return label, round(polarity, 4)

    except Exception as e:
        print(f"[SENTIMENT] TextBlob error: {e}")
        return "neutral", 0.0
