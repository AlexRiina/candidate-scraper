Scraper for Candidate Information

The main interface for running the scraper is through

    python scrape_websites.py

which reads candidate websites from a file name `websites.csv` with no header and a line per website like

    # websites.csv
    www.candidate1.com
    www.candidate2.com
    ...

The script crawls through each site and exports files like

    twitter-www.candidate1.com.csv
    email-www.candidate1.com.csv
    ...

that contain the original domain and social handles. I've been combining them
via python and manually confirming the output.
