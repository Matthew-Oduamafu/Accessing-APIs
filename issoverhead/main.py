import requests
from datetime import datetime
import smtplib
from time import sleep

MY_LAT = 6.695070  # Your latitude
MY_LONG = -1.615800  # Your longitude
USER = "mattietorrent@gmail.com"
PASSWORD = "Matthew20@&"

iss_latitude = float("0.0")
iss_longitude = float("0.0")


def get_iss_location():
    global iss_latitude, iss_longitude
    response_ = requests.get(url="http://api.open-notify.org/iss-now.json")
    response_.raise_for_status()
    data_ = response_.json()
    iss_latitude = float(data_["iss_position"]["latitude"])
    iss_longitude = float(data_["iss_position"]["longitude"])


# Your position is within +5 or -5 degrees of the ISS position.
def get_position():
    return MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()
# If the ISS is close to my current position,
while True:

    get_iss_location()
    if get_position():
        # and it is currently dark
        # Then email me to tell me to look up.
        if not (sunrise <= time_now.hour <= sunset):
            try:
                print("Sending mail...")
                with smtplib.SMTP(host="smtp.gmail.com") as connection:
                    connection.starttls()
                    connection.login(user=USER, password=PASSWORD)
                    connection.sendmail(
                        from_addr=USER,
                        to_addrs="mattmaymadjitey@gmail.com",
                        msg="Subject:ISS Satellite Is Passing By\n\nHey There!\nRaise "
                            "up your head and watch ISS Satellite pass by\n\n"
                            "Your boy Matthew"
                    )
                print("Mail Sent!")
            except TimeoutError:
                print("Connection Timeout! \nConnection failed")
        print("ISS is passing by\nBut you can't see because it's day")
    else:
        print("ISS not close to your location")
        print("ISS location", iss_latitude, iss_longitude)
        print("Your location", MY_LAT, MY_LONG, "\n")
    sleep(60)
# BONUS: run the code every 60 seconds.
