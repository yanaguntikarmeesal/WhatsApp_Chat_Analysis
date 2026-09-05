

from collections import Counter

import emoji
import pandas as pd

from urlextract import URLExtract
from wordcloud import WordCloud


# --------------------------------------------------
# URL EXTRACTOR
# --------------------------------------------------

extract = URLExtract()


# --------------------------------------------------
# FILTER USER
# --------------------------------------------------

def filter_user(selected_user, df):

    if selected_user != "Overall":

        return df[
            df["user"] == selected_user
        ].copy()

    return df.copy()


# --------------------------------------------------
# FETCH STATISTICS
# --------------------------------------------------

def fetch_stats(selected_user, df):

    df = filter_user(
        selected_user,
        df
    )

    # Total messages

    num_messages = df.shape[0]

    # Total words

    words = []

    for message in df["message"].fillna(""):

        words.extend(
            message.split()
        )

    # Media messages

    num_media_messages = df[
        df["message"].str.strip()
        == "<Media omitted>"
    ].shape[0]

    # Links

    links = []

    for message in df["message"].fillna(""):

        links.extend(
            extract.find_urls(message)
        )

    return (
        num_messages,
        len(words),
        num_media_messages,
        len(links)
    )


# --------------------------------------------------
# MOST BUSY USERS
# --------------------------------------------------

def most_busy_users(df):

    # Remove system notifications

    temp = df[
        df["user"]
        != "group_notification"
    ].copy()

    # Top users

    x = (
        temp["user"]
        .value_counts()
        .head()
    )

    # Percentage

    percentage = (
        temp["user"]
        .value_counts(
            normalize=True
        )
        .mul(100)
        .round(2)
        .reset_index()
    )

    percentage.columns = [
        "name",
        "percent"
    ]

    return x, percentage


# --------------------------------------------------
# STOP WORDS
# --------------------------------------------------

def get_stop_words():

    try:

        with open(
            "stop_hinglish.txt",
            "r",
            encoding="utf-8"
        ) as f:

            return set(
                f.read().split()
            )

    except FileNotFoundError:

        return set()


# --------------------------------------------------
# GET WORDS
# --------------------------------------------------

def get_message_words(
    selected_user,
    df
):

    temp = filter_user(
        selected_user,
        df
    )

    # Remove group notifications

    temp = temp[
        temp["user"]
        != "group_notification"
    ]

    # Remove media messages

    temp = temp[
        temp["message"].str.strip()
        != "<Media omitted>"
    ]

    stop_words = get_stop_words()

    words = []

    for message in temp["message"].fillna(""):

        for word in message.lower().split():

            cleaned = word.strip(
                ".,!?;:\"'()[]{}<>"
            )

            if (
                cleaned
                and cleaned not in stop_words
            ):

                words.append(cleaned)

    return words


# --------------------------------------------------
# MOST COMMON WORDS
# --------------------------------------------------

def most_common_words(
    selected_user,
    df
):

    words = get_message_words(
        selected_user,
        df
    )

    return pd.DataFrame(
        Counter(words)
        .most_common(25)
    )


# --------------------------------------------------
# WORD CLOUD
# --------------------------------------------------

def create_wordcloud(
    selected_user,
    df
):

    words = get_message_words(
        selected_user,
        df
    )

    if not words:

        return None

    text = " ".join(words)

    wordcloud = WordCloud(
        width=1000,
        height=500,
        background_color="white",
        min_font_size=10
    ).generate(text)

    return wordcloud


# --------------------------------------------------
# EMOJI ANALYSIS
# --------------------------------------------------

def emoji_helper(
    selected_user,
    df
):

    temp = filter_user(
        selected_user,
        df
    )

    emojis = []

    for message in temp["message"].fillna(""):

        emojis.extend(
            [
                char
                for char in message
                if char in emoji.EMOJI_DATA
            ]
        )

    return pd.DataFrame(
        Counter(emojis).most_common(),
        columns=[0, 1]
    )


# --------------------------------------------------
# MONTHLY TIMELINE
# --------------------------------------------------

def monthly_timeline(
    selected_user,
    df
):

    temp = filter_user(
        selected_user,
        df
    )

    timeline = (
        temp.groupby(
            [
                "year",
                "month_num",
                "month"
            ]
        )
        .size()
        .reset_index(
            name="message"
        )
        .sort_values(
            [
                "year",
                "month_num"
            ]
        )
    )

    timeline["time"] = (
        timeline["month"]
        + "-"
        + timeline["year"]
        .astype(str)
    )

    return timeline


# --------------------------------------------------
# DAILY TIMELINE
# --------------------------------------------------

def daily_timeline(
    selected_user,
    df
):

    temp = filter_user(
        selected_user,
        df
    )

    daily = (
        temp.groupby(
            "only_date"
        )
        .size()
        .reset_index(
            name="message"
        )
        .sort_values(
            "only_date"
        )
    )

    return daily


# --------------------------------------------------
# WEEK ACTIVITY
# --------------------------------------------------

def week_activity_map(
    selected_user,
    df
):

    temp = filter_user(
        selected_user,
        df
    )

    order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    return (
        temp["day_name"]
        .value_counts()
        .reindex(
            order,
            fill_value=0
        )
    )


# --------------------------------------------------
# MONTH ACTIVITY
# --------------------------------------------------

def month_activity_map(
    selected_user,
    df
):

    temp = filter_user(
        selected_user,
        df
    )

    order = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]

    return (
        temp["month"]
        .value_counts()
        .reindex(
            order,
            fill_value=0
        )
    )


# --------------------------------------------------
# ACTIVITY HEATMAP
# --------------------------------------------------

def activity_heatmap(
    selected_user,
    df
):

    temp = filter_user(
        selected_user,
        df
    )

    order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    heatmap = (
        temp.pivot_table(
            index="day_name",
            columns="period",
            values="message",
            aggfunc="count",
            fill_value=0
        )
        .reindex(order)
    )

    return heatmap

