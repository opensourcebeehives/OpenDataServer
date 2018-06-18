import cherrypy
import json
import csv
import os
import config


def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"


class OpenDataServer(object):

    def __init__(self):
        if not os.path.isdir(config.data_dir):
            os.mkdir(config.data_dir)
        self.measurement_headers = ["published_at", "device_id", "temp_c_in",
                                    "temp_c_out", "pressure_out", "rhumidity_out",
                                    "rhumidity_in", "battery_charge",
                                    "battery_health", "solar_charge", "rssi",
                                    "wifi_packet_loss", "audio_packet_loss",
                                    "lat", "lon", "weather_main", "wind_speed", "wind_angle"]
        self.audioevent_headers = ["published_at",
                                   "device_id", "event_type", "s3_url"]

    @cherrypy.expose
    def measurements(self):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        body = json.loads(rawbody)
        try:
            measurement = body['measurement']
            self.process_measurement(measurement)
        except KeyError:
            raise cherrypy.HTTPError(400, 'Bad request')

        return json.dumps({'status': 'ok'})

    @cherrypy.expose
    def audioevents(self):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        body = json.loads(rawbody)
        try:
            audioevent = body['audioevent']
            self.process_audioevent(audioevent)
        except KeyError:
            raise cherrypy.HTTPError(400, 'Bad request')

        return json.dumps({'status': 'ok'})

    def process_measurement(self, measurement):
        folder = config.data_dir + '/' + \
            measurement['device_id'] + '/measurements/'
        if not os.path.isdir(folder):
            os.makedirs(folder)
        path = folder + measurement['published_at'].split()[0] + '.csv'
        write_headers = True
        if os.path.isfile(path):
            write_headers = False
        with open(path, 'a') as out_file:
            writer = csv.writer(out_file)
            if write_headers:
                writer.writerow(self.measurement_headers)
            writer.writerow([measurement[header]
                             for header in self.measurement_headers])

    def process_audioevent(self, audioevent):
        folder = config.data_dir + '/' + \
            audioevent['device_id'] + '/audioevents/'
        if not os.path.isdir(folder):
            os.makedirs(folder)
        path = folder + audioevent['published_at'].split()[0] + '.csv'
        write_headers = True
        if os.path.isfile(path):
            write_headers = False
        with open(path, 'a') as out_file:
            writer = csv.writer(out_file)
            if write_headers:
                writer.writerow(self.audioevent_headers)
            writer.writerow([audioevent[header]
                             for header in self.audioevent_headers])


def load_http_server():
    # extra server instance to dispatch HTTP
    server = cherrypy._cpserver.Server()
    server.socket_host = config.api_host
    server.socket_port = 80
    server.subscribe()


def force_tls():
    if cherrypy.request.scheme == "http":
        # see https://support.google.com/webmasters/answer/6073543?hl=en
        raise cherrypy.HTTPRedirect(
            cherrypy.url().replace("http:", "https:"),
            status=301)


cherrypy.tools.force_tls = cherrypy.Tool("before_handler", force_tls)

if __name__ == '__main__':
    cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)
    cherrypy.config.update({
        'server.socket_host': config.api_host,
        'server.socket_port': config.api_port
    })
    # Change this option if you want SSL and HTTP to HTTPS redirects
    if config.use_ssl:
        cherrypy.config.update({
            'tools.force_tls.on': True,
            'server.ssl_module': 'pyopenssl',
            'server.ssl_certificate': config.ssl_certificate,
            'server.ssl_private_key': config.private_key,
            'server.ssl_certificate_chain': config.certificate_chain
        })
        load_http_server()
    if not config.staging:
        cherrypy.config.update({'environment': 'production'})
    cherrypy.quickstart(OpenDataServer(), config={
                        '/': {'tools.CORS.on': True}})
