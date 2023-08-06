#!/usr/bin/env python3.7
from datetime import datetime

class Buzzsprout:
    """
    An object that contains all episodes that match the parameters.
    """

    def __init__(self):
        pass

    class __Episode:
        """
        An episode class that contains all of the required properties of a podcast episode.
        """
        def __init__(self, json, customurl):
            self.title = json['title']
            self.audio_url = json['audio_url']
            self.episode_url = json['audio_url'].rsplit('.', 1)[0]
            if customurl is not None:
                self.episode_url = self.episode_url.replace('www.buzzsprout.com', customurl)
            self.description = json['description']
            self.summary = json['summary']
            self.artist = json['artist']
            self.tags = json['tags']
            self.published_at = datetime.strptime(json['published_at'].split('T')[0], '%Y-%m-%d')
            self.episode_number = json['episode_number']
            self.season_number = json['season_number']

        def __repr__(self):
            return self.title

    def get(self, profileid, token, datefilter=None, tagfilter=None, random=False, customurl=None):
        """
        Get episodes from a given Buzzsprout profile and create Episode objects for them.
        """
        
        url = self.__build_url(profileid, token, 'episodes.json')
        response = self.__get_request(url)

        episodes = []
        for json in response:
            # Filter for given tag if present.
            if tagfilter is not None:
                result = self.__find_tag(tagfilter, json['tags'])
                if result == False:
                    continue

            # Filter for given date-time if present.
            if datefilter is not None:
                result = self.__compare_datetime(datefilter, json['published_at'])
                if result == False:
                    continue
                
            episodes.append(self.__Episode(json, customurl))

        # Error if no results
        if len(episodes) is 0:
            raise ValueError('No episodes returned for this query')

        # Return only a single random episode, if the switch is set
        self.episodes = self.__random_check(random, episodes)

    def __build_url(self, profileid, token, json):
        """
        Builds the Buzzsprout API URL to query.
        """
        base_url = 'https://www.buzzsprout.com/api'
        self.url = f"{base_url}/{profileid}/{json}?api_token={token}"
        return self.url

    def __get_request(self, url):
        import json
        import requests

        return json.loads(requests.get(url).content)

    def __compare_datetime(self, datefilter, json):
        """
        Compares two date-time values to determine if an episode was published before or after the given date-time.
        """

        publish_date = datetime.strptime(json.split('T')[0], '%Y-%m-%d')
        filter_date = datetime.strptime(datefilter, '%Y-%m-%d')
        result = publish_date > filter_date
        return result

    def __find_tag(self, tagfilter, tags):
        """
        Check for a tag in the episode tag values.
        """
        result = tagfilter in tags
        return result

    def __random_episode(self, episodes):
        """
        Return a random episode from a list of episodes.
        """
        import random

        count = 0
        for episode in episodes:
            count += 1

        randomint = random.randint(0,(count - 1))

        return episodes[randomint]

    def __random_check(self, random, episodes):
        if random is True:
            return self.__random_episode(episodes)
        else:
            return episodes