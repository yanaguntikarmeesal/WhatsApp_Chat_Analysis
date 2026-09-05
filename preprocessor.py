


import re
import pandas as pd


def preprocess(data):

    # --------------------------------------------------
    # WHATSAPP DATE/TIME PATTERN
    # --------------------------------------------------

    pattern = (
        r"\d{1,2}/\d{1,2}/\d{2,4},"
        r"\s\d{1,2}:\d{2}\s-\s"
    )

    # --------------------------------------------------
    # SPLIT MESSAGES
    # --------------------------------------------------

    messages = re.split(pattern, data)[1:]

    dates = re.findall(pattern, data)

    if not messages or not dates:
        return pd.DataFrame()

    # --------------------------------------------------
    # CREATE DATAFRAME
    # --------------------------------------------------

    df = pd.DataFrame(
        {
            "user_message": messages,
            "message_date": dates
        }
    )

    # --------------------------------------------------
    # CONVERT DATE
    # --------------------------------------------------

    df["date"] = pd.to_datetime(
        df["message_date"].str.rstrip(" -"),
        dayfirst=True,
        errors="coerce"
    )

    # Remove unnecessary column

    df.drop(
        columns=["message_date"],
        inplace=True
    )

    # --------------------------------------------------
    # EXTRACT USER AND MESSAGE
    # --------------------------------------------------

    users = []
    clean_messages = []

    for message in df["user_message"]:

        entry = re.split(
            r"([\w\W]+?):\s",
            message,
            maxsplit=1
        )

        if len(entry) >= 3:

            users.append(entry[1])

            clean_messages.append(
                entry[2]
            )

        else:

            users.append(
                "group_notification"
            )

            clean_messages.append(
                entry[0]
            )

    df["user"] = users

    df["message"] = clean_messages

    # --------------------------------------------------
    # REMOVE OLD COLUMN
    # --------------------------------------------------

    df.drop(
        columns=["user_message"],
        inplace=True
    )

    # Remove invalid dates

    df.dropna(
        subset=["date"],
        inplace=True
    )

    # --------------------------------------------------
    # DATE FEATURES
    # --------------------------------------------------

    df["year"] = df["date"].dt.year

    df["month_num"] = df["date"].dt.month

    df["only_date"] = df["date"].dt.date

    df["month"] = (
        df["date"].dt.month_name()
    )

    df["day"] = df["date"].dt.day

    df["day_name"] = (
        df["date"].dt.day_name()
    )

    df["hour"] = df["date"].dt.hour

    df["minute"] = df["date"].dt.minute

    # --------------------------------------------------
    # TIME PERIOD
    # --------------------------------------------------

    df["period"] = (
        df["hour"]
        .astype(str)
        .str.zfill(2)
        + "-"
        + (
            (df["hour"] + 1) % 24
        )
        .astype(str)
        .str.zfill(2)
    )

    return df

