import configparser
import requests as r

from wowapi import WowApi


class Pythia:
    def __init__(self):
        self.config = self.read_config()
        self.api = WowApi(
            client_id=self.config['API']['id'],
            client_secret=self.config['API']['key']
        )

        # Game data
        # self.regions = self.get_regions()
        # self.realms = self.get_realms()
        self.auctions = self.get_auctions()

    @staticmethod
    def read_config():
        cfg = configparser.ConfigParser()
        cfg.read('./settings.cfg')

        return cfg

    def get_regions(self):
        url = self.api.get_regions(region='eu', namespace='dynamic-eu')
        regions = self.api.get_data_resource(url['regions'][0]['href'], region='eu')

        return regions

    def get_realms(self):
        results = []
        urls = self.api.get_connected_realms(region='eu', namespace='dynamic-eu')

        for url in urls['connected_realms']:
            data = self.api.get_data_resource(url['href'], region='eu')

            for realm in data['realms']:
                results.append(
                    {
                        'id': realm['id'],
                        'name': realm['name']['en_US']
                    }
                )

        return results

    def get_auctions(self):
        results = {}

        slug = self.find_realm_slug('Kazzak')

        url = self.api.get_auctions(region='eu', realm_slug=slug, locale='en_US')

        auctions = self.api.get_data_resource(url=url['files'][0]['url'], region='eu')

        auctions = auctions['auctions']

        for auction in auctions:
            # print(auctions.index(auction)+1, len(auctions))
            # item_data = self.find_item_name(auction['item'])

            # if auction['item'] not in results.keys():
                # results[auction['item']] = item_data

            # if 'auction' not in results[auction['item']].keys():
            #     results[auction['item']]['auction'] = []
            # else:
            #     results[auction['item']]['auction'].append(auction)

            if auction['item'] not in results.keys():
                results[auction['item']] = []

            results[auction['item']].append(auction)

        print('pass')


    def find_item_name(self, item_id):
        return self.api.get_item(region='eu', id=item_id)


    def find_realm_slug(self, realm_name):
        realms = self.api.get_realm_status(region='eu', realm_name='Ashbringer')

        try:
            for realm in realms['realms']:
                if realm_name == realm['name']:
                    return realm['slug']
        except Exception as e:
            raise e


if __name__ == "__main__":
    Pythia = Pythia()
    print('debug')
