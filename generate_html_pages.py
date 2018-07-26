#!/usr/bin/env python3

"""
Krishna Bhattarai
super secret TV project
QuantumIOT, 2018
"""

import sys, os, datetime, json, requests, time

HTML_DIRECTORY = "html"
DEBUG = 1


def http_post(url, body, headers):
    response = requests.post(url=url, data=body, headers=headers)
    return response if response.status_code == 200 else print("The status code of the post was ", response.status_code)


def http_get(url, body, headers):
    response = requests.get(url=url, data=body, headers=headers)
    return response if response.status_code == 200 else print("The status code of the post was ", response.status_code)


def current_date():
    """
    :return: Get current date with only year month and date and the rest as zero eg: 2018-06-04T00:00:00
    """
    return time.strftime("%Y-%m-%dT00:00:00")


def key_value_pair_matches(some_json, filter_key, filter_value):
    """
    :param some_json: a json object
    :param filter_key: key to test
    :param filter_value: value to test
    :return: A Boolean i.e. either True or False depending on if the key value pairs in some_json match the parameters
    """
    return True if some_json[filter_key] == filter_value else False


def filter_dict(list_of_objects, filter_key, filter_value):
    """
    :param list_of_objects: a list of json objects
    :param filter_key: key to test
    :param filter_value: value to test
    :return: a new list of json objects whose key and value pairs match the parameters
    """
    return [items for items in list_of_objects if key_value_pair_matches(items, filter_key, filter_value)]


def return_matching_object(objects_list, key, value):
    """
    Returns the first matching object that matches the provided key value pair
    :param objects_list: list of json objects
    :param key: key to match in the objects list
    :param value: value to match in the objects list
    :return: the first object that matches the key and value params provided
    """
    matched_object = None
    for item in objects_list:
        if item[key] == value:
            matched_object = item
            break
    return matched_object


def change_24_hours_to_12_hours(timestamp):
    """
    Given a timestamp return the time HH:MM %p in 12 hour format
    :param timestamp: 2018-06-04T13:30:00
    :return: 04:30 PM
    """
    return datetime.datetime.strptime(timestamp.split("T")[1][0:5], "%H:%M").strftime("%I:%M %p")


def add_runtime_to_showtime(showtime, runtime_in_minues):
    """
    :param showtime: timestamp in this format 2018-06-04T00:00:00
    :param runtime_in_minues: integer
    :return: new time stamp in 2018-06-04T00:00:00 with the minutes added
    """
    new_time_stamp = datetime.datetime.strptime(showtime, "%Y-%m-%dT%H:%M:%S") + datetime.timedelta(minutes=runtime_in_minues)
    return new_time_stamp.strftime("%Y-%m-%dT%H:%M:%S")


def get_now_showing_sessions():
    url = 'http://vista.studiomoviegrill.com/WSVistaWebClient/OData.svc/GetNowShowingSessions'
    body = {"siteGroupId": "0009"}
    headers = {'Accept': 'application/json'}
    return http_get(url, body, headers).text


def get_now_showing_scheduled_films():
    url = 'http://vista.studiomoviegrill.com/WSVistaWebClient/OData.svc/GetNowShowingScheduledFilms'
    body = {}
    headers = {'Accept': 'application/json'}
    return http_get(url, body, headers).text


def ensure_directory_exists(directory):
    os.makedirs(os.path.dirname(directory), exist_ok=True)
    return


def remove_old_html_pages():
    directory = os.listdir(HTML_DIRECTORY)
    for files in directory:
        if files.endswith(".html"):
            os.remove(os.path.join(HTML_DIRECTORY, files))


def write_html_content_to_file(theater, location, scheduled_film_id, show_time_start, show_time_end, run_time, title, url):
    html_string = """<!doctype html>
    <html lang="en">
       <head>
          <!-- Required meta tags -->
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
          <!-- Bootstrap CSS -->
          <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
          <title>Studio Movie Grill</title>
       </head>
       <body>
          <div class="container-fluid bg-dark">
             <div class="row">
                <div class="col-sm-3 bg-dark border-right text-white">
                   <p style="font-size:100px" class="text-center">%d</p>
                </div>
                <div class="col-sm-9 bg-dark text-white">
                   <p></p>
                   <p style="font-size:35px">%s</p>
                   <h2>%s</h2>
                   <p></p>
                </div>
             </div>
          </div>
          <div class="containter-fluid">
             <div class="row">
                <div class="col-sm-12 img-responsive">
                   <img src="%s" class="img-fluid w-100">
                </div>
             </div>
          </div>
          <div class="containter-fluid">
             <div class = "row">
                <div style="height:100px" class="col-sm-6 bg-dark text-white">
                   <p id="demo2" style="font-size:35px" class="text-right">Starting in</p>
                </div>
                <div style="height:100px" class="col-sm-6 bg-dark text-white">
                   <p id="demo" style="font-size:35px" class="text-left"></p>
                </div>
             </div>
          </div>
          <!-- Optional JavaScript -->
          <!-- jQuery first, then Popper.js, then Bootstrap JS -->
          <script src="./scripts/jquery-3.2.1.slim.min.js"></script>
          <script src="./scripts/popper.min.js"></script>
          <script src="./scripts/bootstrap.min.js"></script>
          <script>
             // Set the date we're counting down to
             var countDownDate = new Date().getTime() + 10000;

             // Update the count down every 1 second
             var x = setInterval(function() {

             // Get todays date and time
             var now = new Date().getTime();

             // Find the distance between now an the count down date
             var distance = countDownDate - now;

             // Time calculations for days, hours, minutes and seconds
             var days = Math.floor(distance / (1000 * 60 * 60 * 24));
             var hours = Math.floor((distance %% (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
             var minutes = Math.floor((distance %% (1000 * 60 * 60)) / (1000 * 60));
             var seconds = Math.floor((distance %% (1000 * 60)) / 1000);

             // Output the result in an element with id="demo"
             document.getElementById("demo").innerHTML =  hours.toString().padStart(2, "0") + ":" + minutes.toString().padStart(2, "0") + ":" + seconds.toString().padStart(2, "0") ;

             // If the count down is over, write some text
             if (distance < 1000) {
                 countDownDate = new Date().getTime() + (1000 * 60 * %d);
                 document.getElementById("demo2").innerHTML = "Ending in";
             }
             }, 1000);
        </script>
    </body>
    </html>""" % (theater, title, change_24_hours_to_12_hours(show_time_start), url, int(run_time))

    fp = open(HTML_DIRECTORY + "/" + "location=" + str(location) + "_theater=" + str(theater) + "_scheduledfilmid=" + scheduled_film_id +"_showtimestarts=" + show_time_start + "_showtimeends=" + show_time_end + ".html", "w+")
    fp.write(html_string)
    fp.close()


def generate_html_pages(now_showing_sessions, now_showing_scheduled_films, location):
    print("%-8s %-8s %-15s %-20s %-20s %-8s %-40s %-60s" % ("Theater", "Location", "ScheduledFilmId",  "ShowtimeStart", "ShowtimeEnd", "RunTime", "Title", "URL")) if DEBUG else ""
    for items in now_showing_sessions:
        Theater = items["ScreenNumber"]
        Title = return_matching_object(now_showing_scheduled_films, "ScheduledFilmId", items["ScheduledFilmId"])['Title']
        ShowtimeStart = items["Showtime"]
        RunTime = return_matching_object(now_showing_scheduled_films, "ScheduledFilmId", items["ScheduledFilmId"])['RunTime']
        ShowtimeEnd = add_runtime_to_showtime(items["Showtime"], int(RunTime))
        ScheduledFilmId = items["ScheduledFilmId"]

        URL = "http://srv001.vista.smg" + str(location[1:]) + ".studiomoviegrill.com/Cinema-CDN/Image/Entity/FilmTitleGraphic/h-" + ScheduledFilmId
        print("%-8s %-8s %-15s %-20s %-20s %-8s %-40s %-60s" % (Theater, location,  ScheduledFilmId, ShowtimeStart, ShowtimeEnd, RunTime, Title, URL)) if DEBUG else ""
        write_html_content_to_file(Theater, location, ScheduledFilmId, ShowtimeStart, ShowtimeEnd,  RunTime, Title, URL,)


def usage():
    print("Please try again with a location code and theater number")
    print("USAGE  : ./generate_html_pages.py <4-digit-location-code> <theater-number>")
    print("example: ./generate_html_pages.py 0009 1")
    sys.exit(1)


def main():
    location, theater = "", ""
    if len(sys.argv) == 3:
        location, theater = sys.argv[1], int(sys.argv[2])
    else:
        usage()

    usage() if len(location) != 4 else ""

    """ Filter by Location Number, Business Date, and Theater Number """

    sessions_by_location_theater_date = filter_dict(filter_dict(filter_dict(json.loads(get_now_showing_sessions())["value"], 'CinemaId', location), 'SessionBusinessDate', current_date()), 'ScreenNumber', theater)
    
    scheduled_films_filtered_by_location = filter_dict(json.loads(get_now_showing_scheduled_films())['value'], "CinemaId", location)

    remove_old_html_pages()

    generate_html_pages(sessions_by_location_theater_date, scheduled_films_filtered_by_location, location)


if __name__ == "__main__":
    main()
