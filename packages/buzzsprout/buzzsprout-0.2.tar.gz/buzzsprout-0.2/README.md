A Python BuzzsproutPodcasts class.
=======
## Prerequisites
* Python 3.7 and above
* A Buzzsprout account (and your API token)

## Summary
Provide an API Token and a Profile ID, to create a BuzzsproutPodcasts object containing all episodes for that profile matching the given parameters. 

## Installation
```
pip install buzzsprout
```

## Getting started
Instantiate the Buzzsprout class.
```
$ from buzzsprout import Buzzsprout
$ buzzsprout = Buzzsprout()
```

You then pass your profile id and token into the **get** method. By default, this will pull all episodes:
```
$ buzzsprout.get('profileid='PROFILEID', token='TOKEN')
```

## Attributes
- title
- audio_url
- episode_url
- description
- summary
- artist
- tags
- published_at
- episode_number
- season_number

## Filtering
You can currently filter by:
- Date
- Tag
- Random

(and these can be used in combination).

To return only episodes newer than 2019-03-01
```
$ recent_episodes = buzzsprout.get(profileid='PROFILEID', token='TOKEN', datefilter='2019-03-01')
```
To return only episodes that contain the tag "Interviews"
```
$ interview_episodes = buzzsprout.get(profileid='PROFILEID', token='TOKEN', tagfilter='Interviews')
```
To return one random episode from the results, use the random switch
```
$ random_episode = buzzsprout.get(profileid='PROFILEID', token='TOKEN', random=True)
```

## Things to note
Weirdly, Buzzsprout's API does not return an episode URL. I have therefore implemented a *slightly* hacky solution which modifies the audio URL.
By default this URL will not use any custom URL's you have set. I have therefore implemented a workaround. If you pass in your custom URL, the **episode_url** property will be updated:
```
$ custom_url_episode = buzzsprout.get(profileid='PROFILEID', token='TOKEN', random=True, customurl='subdomain.example.com')
```