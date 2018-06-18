Open Data Server
================

This repository contains a working template for an Open Data Server that receives data from a hive monitor configured through the [OSBeehives app](https://www.osbeehives.com/pages/osbeehives-app).

## Install requirements

`sudo apt update`

`sudo apt install python python-pip`

`sudo pip install -r requirements.txt --no-cache-dir --upgrade`

## Setup

* Change host, port and configure SSL (if needed) on config.py
* Use staging = False to run CherryPy on production mode

## Run

`sudo nohup python open_data_server.py &`

## Endpoints

### measurements

* Type: `POST`
* Sample Body:
  `{
    "measurement":{ 
      "published_at": "2018-06-18 17:12:47.158",
      "device_id": "000000000000000000000000",
      "temp_c_in": 27.4,
      "temp_c_out": 18.05,
      "pressure_out": 762,
      "rhumidity_out": 72,
      "rhumidity_in": 27,
      "battery_charge": 100,
      "battery_health": 100,
      "solar_charge": 3,
      "rssi": -5,
      "wifi_packet_loss": 1,
      "audio_packet_loss": 1,
      "lat": 0,
      "lon": 0,
      "weather_main": "Scattered Clouds",
      "wind_speed": 3,
      "wind_angle": 30 
    }
  }`

### audioevents

* Type: `POST`
* Sample Body:
  `{
    "audioevent":{ 
      "published_at": "2018-06-18 17:12:47.158",
      "device_id": "000000000000000000000000",
      "event_type": "Active",
      "s3_url": "https://s3-us-west-2.amazonaws.com/osbhbuzzboxrecordings/0000.mp3"
    }
  }`

## Functions to edit

### process_measurement()

* Defines what happens when a measurement is received. By default, it appends the data into a different .csv file for each device_id and day.

### process_audioevent()

* Defines what happens when an audioevent is received. By default, it downloads the file and appends the metadata into a different .csv file for each device_id and day.

License
=======

**This software is released under the [MIT License](http://opensource.org/licenses/MIT).**

  The MIT License (MIT)

  Copyright (c) OSBeehives, Inc.

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.