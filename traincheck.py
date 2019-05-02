import requests


class TrainCheck:
    def __init__(self):
        pass

    def check_train(self, conf):
        url = 'https://dbf.finalrewind.org/${0}'.format(conf['secret']['station_from'])

        params = dict(
            via=conf['secret']['station_via'],
            mode="json",
            version="3"
        )

        resp = requests.get(url=url, params=params)

        data = resp.json()

        departures = data['departures']

        if len(departures) == 0:
            return 'In nächster Zeit fahren keine Bahnen.'

        result = ""

        for departure in departures[:2]:
            if departure['isCancelled'] == 0:
                if departure['delayDeparture'] < 3:
                    result += "Die Bahn um {0} Uhr is pünktlich. ".format(departure['scheduledDeparture'])
                else:
                    result += "Die Bahn um {0} Uhr hat {1} Minuten Verspätung. ".format(departure['scheduledDeparture'], departure['delayDeparture'])
                for qos_message in departure['messages']['qos']:
                    result += qos_message['text']
            else:
                result += "Die Bahn um {0} Uhr fällt aus. ".format(departure['scheduledDeparture'])

        return result
