


import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide"
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("💬 WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader(
    "Choose WhatsApp exported chat file",
    type=["txt"]
)

# --------------------------------------------------
# MAIN APPLICATION
# --------------------------------------------------

if uploaded_file is not None:

    # Read uploaded file
    try:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
    except UnicodeDecodeError:
        data = uploaded_file.getvalue().decode("utf-8-sig")

    # Preprocess data
    df = preprocessor.preprocess(data)

    if df.empty:
        st.error(
            "No WhatsApp messages found. "
            "Please upload a valid WhatsApp exported .txt file."
        )
        st.stop()

    # --------------------------------------------------
    # USER LIST
    # --------------------------------------------------

    user_list = df["user"].unique().tolist()

    if "group_notification" in user_list:
        user_list.remove("group_notification")

    user_list.sort()

    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox(
        "Show analysis with respect to",
        user_list
    )

    # --------------------------------------------------
    # SHOW ANALYSIS BUTTON
    # --------------------------------------------------

    if st.sidebar.button("Show Analysis", type="primary"):

        # ==================================================
        # TOP STATISTICS
        # ==================================================

        (
            num_messages,
            words,
            num_media_messages,
            num_links
        ) = helper.fetch_stats(selected_user, df)

        st.title("📊 Top Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Messages",
                num_messages
            )

        with col2:
            st.metric(
                "Total Words",
                words
            )

        with col3:
            st.metric(
                "Media Shared",
                num_media_messages
            )

        with col4:
            st.metric(
                "Links Shared",
                num_links
            )

        st.divider()

        # ==================================================
        # MONTHLY TIMELINE
        # ==================================================

        st.title("📅 Monthly Timeline")

        timeline = helper.monthly_timeline(
            selected_user,
            df
        )

        if not timeline.empty:

            fig, ax = plt.subplots(
                figsize=(12, 5)
            )

            ax.plot(
                timeline["time"],
                timeline["message"],
                marker="o"
            )

            ax.set_xlabel("Month")
            ax.set_ylabel("Number of Messages")
            ax.set_title("Monthly Message Activity")

            plt.xticks(rotation=45)

            fig.tight_layout()

            st.pyplot(fig)

            plt.close(fig)

        # ==================================================
        # DAILY TIMELINE
        # ==================================================

        st.title("📈 Daily Timeline")

        daily_timeline = helper.daily_timeline(
            selected_user,
            df
        )

        if not daily_timeline.empty:

            fig, ax = plt.subplots(
                figsize=(12, 5)
            )

            ax.plot(
                daily_timeline["only_date"],
                daily_timeline["message"]
            )

            ax.set_xlabel("Date")
            ax.set_ylabel("Number of Messages")
            ax.set_title("Daily Message Activity")

            plt.xticks(rotation=45)

            fig.tight_layout()

            st.pyplot(fig)

            plt.close(fig)

        # ==================================================
        # ACTIVITY MAP
        # ==================================================

        st.title("🔥 Activity Map")

        col1, col2 = st.columns(2)

        # --------------------------------------------------
        # MOST BUSY DAY
        # --------------------------------------------------

        with col1:

            st.subheader("Most Busy Day")

            busy_day = helper.week_activity_map(
                selected_user,
                df
            )

            fig, ax = plt.subplots(
                figsize=(8, 5)
            )

            ax.bar(
                busy_day.index,
                busy_day.values
            )

            ax.set_xlabel("Day")
            ax.set_ylabel("Messages")

            plt.xticks(rotation=45)

            fig.tight_layout()

            st.pyplot(fig)

            plt.close(fig)

        # --------------------------------------------------
        # MOST BUSY MONTH
        # --------------------------------------------------

        with col2:

            st.subheader("Most Busy Month")

            busy_month = helper.month_activity_map(
                selected_user,
                df
            )

            fig, ax = plt.subplots(
                figsize=(8, 5)
            )

            ax.bar(
                busy_month.index,
                busy_month.values
            )

            ax.set_xlabel("Month")
            ax.set_ylabel("Messages")

            plt.xticks(rotation=45)

            fig.tight_layout()

            st.pyplot(fig)

            plt.close(fig)

        # ==================================================
        # WEEKLY ACTIVITY HEATMAP
        # ==================================================

        st.title("🗓️ Weekly Activity Map")

        user_heatmap = helper.activity_heatmap(
            selected_user,
            df
        )

        if not user_heatmap.empty:

            fig, ax = plt.subplots(
                figsize=(14, 6)
            )

            sns.heatmap(
                user_heatmap,
                annot=True,
                fmt=".0f",
                ax=ax
            )

            ax.set_xlabel("Time Period")
            ax.set_ylabel("Day")

            fig.tight_layout()

            st.pyplot(fig)

            plt.close(fig)

        # ==================================================
        # MOST BUSY USERS
        # ==================================================

        if selected_user == "Overall":

            st.title("👥 Most Busy Users")

            x, new_df = helper.most_busy_users(df)

            col1, col2 = st.columns(2)

            with col1:

                fig, ax = plt.subplots(
                    figsize=(8, 5)
                )

                ax.bar(
                    x.index,
                    x.values
                )

                ax.set_xlabel("User")
                ax.set_ylabel("Messages")

                plt.xticks(rotation=45)

                fig.tight_layout()

                st.pyplot(fig)

                plt.close(fig)

            with col2:

                st.dataframe(
                    new_df,
                    use_container_width=True
                )

        # ==================================================
        # WORD CLOUD
        # ==================================================

        st.title("☁️ Word Cloud")

        wordcloud = helper.create_wordcloud(
            selected_user,
            df
        )

        if wordcloud is not None:

            fig, ax = plt.subplots(
                figsize=(12, 6)
            )

            ax.imshow(
                wordcloud,
                interpolation="bilinear"
            )

            ax.axis("off")

            st.pyplot(fig)

            plt.close(fig)

        else:

            st.info("Not enough text to create a word cloud.")

        # ==================================================
        # MOST COMMON WORDS
        # ==================================================

        st.title("🔤 Most Common Words")

        most_common_df = helper.most_common_words(
            selected_user,
            df
        )

        if not most_common_df.empty:

            fig, ax = plt.subplots(
                figsize=(10, 7)
            )

            ax.barh(
                most_common_df[0],
                most_common_df[1]
            )

            ax.set_xlabel("Frequency")

            fig.tight_layout()

            st.pyplot(fig)

            plt.close(fig)

        # ==================================================
        # EMOJI ANALYSIS
        # ==================================================

        st.title("😀 Emoji Analysis")

        emoji_df = helper.emoji_helper(
            selected_user,
            df
        )

        col1, col2 = st.columns(2)

        with col1:

            st.dataframe(
                emoji_df,
                use_container_width=True
            )

        with col2:

            if not emoji_df.empty:

                top_emojis = emoji_df.head(10)

                fig, ax = plt.subplots(
                    figsize=(8, 8)
                )

                ax.pie(
                    top_emojis[1],
                    labels=top_emojis[0],
                    autopct="%0.2f%%"
                )

                ax.set_title("Top 10 Emojis")

                st.pyplot(fig)

                plt.close(fig)

            else:

                st.info("No emojis found.")

else:

    st.info(
        "👈 Upload a WhatsApp exported chat .txt file "
        "from the sidebar to start analysis."
    )

