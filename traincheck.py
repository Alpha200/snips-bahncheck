import requests


class TrainCheck:
    ARTICLE_MAP = dict(
        ABR="der",
        S="die",
        RE="der",
        RB="die",
        EC="der",
        IC="der",
        ICE="der",
        U="die"
    )

    def __init__(self, station_from, station_via):
        self.station_from = station_from
        self.station_via = station_via

    def get_article(self, train):
        transport_type = train[:train.index(" ")]

        if transport_type not in self.ARTICLE_MAP:
            return ""
        else:
            return self.ARTICLE_MAP[transport_type]

    def fix_one(self, train):
        splitted = train.split(' ')
        number = "eins" if splitted[1] == "1" else splitted[1]

        return "{} {}".format(splitted[0], number)

    def check_train(self):
        url = 'https://dbf.finalrewind.org/${0}'.format(self.station_from)

        params = dict(
            via=self.station_via,
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
            result += "{} {} um {} Uhr ".format(
                self.get_article(departure['train']),
                self.fix_one(departure['train']),
                departure['scheduledDeparture']
            )

            if departure['isCancelled'] == 0:
                if departure['delayDeparture'] < 3:
                    result += "ist pünktlich. "
                else:
                    result += "hat {} Minuten Verspätung. ".format(
                        departure['delayDeparture']
                    )
                for qos_message in departure['messages']['qos']:
                    result += qos_message['text']
            else:
                result += "fällt aus. "

        return result
