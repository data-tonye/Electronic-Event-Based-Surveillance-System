# Electronic-Event-Based-Surveillance-System (eEBS)

## Introduction
This project is aimed at demonstrating how health surveillance officers at different levels can monitor online news or events to anticipate a potential health threat.

According to the World Health Organization (WHO), Event-based surveillance is the organized colection, monitoring, assessment and interpretation of unstructured ad hoc information regard health events or risk,which may represent an acute risk to health.

popular examples of a electronic event based surveillance system are [HealthMap](https://healthmap.org/) and Tatafo (used by Nigeria Centre for Disease Control (NCDC))

This is a prototype emualating some core features of an electronic event based surveillance system.

Folders and Files used:
main.py : Contains the executable Streamlit code

code_base.py : Contains the main code for most of the fuctions for the web app.

data :  search_database.db and plot.db are used to save search history of news searches and meta data on searches.

Instructions:

- clone the repo 
- run the main.py file on your IDE environment: "streamlit run main.py"
*You must have streamlit account to use this method*

Or

[click here](https://share.streamlit.io/data-tonye/electronic-event-based-surveillance-system/main/main.py)

**Note: The KeyError you see first is an issue from the Google Search API (SERPAPI) which fails to recognise the key "news_results" but go on to type a disease term**
