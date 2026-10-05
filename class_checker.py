import json
import time
import urllib.request
import urllib.parse
import http.cookiejar

webhook_url = "discord webhook here "

term = "term here"
subject = "subject here"
course_number = "course number"
crn = "the crn"

base_url = "https://registration.wayne.edu/StudentRegistrationSsb/ssb"
wait_time = 30


def send_discord(message):
    data = json.dumps({"content": message}).encode()
    req = urllib.request.Request(webhook_url, data=data)
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "Mozilla/5.0")
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        print("could not send discord message", e)


def get_seats():
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    opener.addheaders = [("User-Agent", "Mozilla/5.0")]

    opener.open(base_url + "/term/termSelection?mode=search").read()

    body = urllib.parse.urlencode({"term": term}).encode()
    opener.open(base_url + "/term/search?mode=search", body).read()

    params = urllib.parse.urlencode({
        "txt_subject": subject,
        "txt_courseNumber": course_number,
        "txt_term": term,
        "pageOffset": 0,
        "pageMaxSize": 50,
    })
    result = opener.open(base_url + "/searchResults/searchResults?" + params).read()
    data = json.loads(result)

    for section in data["data"]:
        if section["courseReferenceNumber"] == crn:
            return section["seatsAvailable"]

    return None


def main():
    print("checking " + subject + " " + course_number + "...")
    send_discord("class checker started")

    while True:
        try:
            seats = get_seats()
            print("seats open:", seats)

            if seats is not None and seats > 0:
                send_discord(subject + " " + course_number + " has " + str(seats) + " seat(s) open!")
                break
        except Exception as e:
            print("something went wrong", e)

        time.sleep(wait_time)


main()
