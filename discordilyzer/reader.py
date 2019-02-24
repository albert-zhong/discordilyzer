from textblob import TextBlob
import csv


def get_mean_sentiment(path):

    authors = {}  # Creates dictionary of authors: author name is the key and polarity/subjectivity list is the value
    with open(path, "r") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)  # Skips header

        for row in reader:
            if is_safe(row[2]):  # Sanitizes message
                text = ignore_non_ascii(row[2])
                blob = TextBlob(text)
                if row[0] not in authors:
                    authors[row[0]] = [blob.polarity, blob.subjectivity, 1]
                else:
                    authors[row[0]][0] += blob.polarity
                    authors[row[0]][1] += blob.subjectivity
                    authors[row[0]][2] += 1

    for x in authors:
        authors[x][0] = authors[x][0] / authors[x][2]
        authors[x][1] = authors[x][1] / authors[x][2]

    return authors


def ignore_non_ascii(text):
    return str(text.encode('utf-8').decode('ascii', 'ignore'))


def is_safe(text):
    if text.isspace() or "Changed the channel name." in text or "Added a recipient." in text or "Started a call." in text or "https" in text:
        return False
    else:
        return True
