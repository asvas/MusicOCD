import mutagen.mp3
import musicbrainzngs
import time
from pprint import pprint

def opener(filepath):
	metadata = mutagen.mp3.Open(filepath)
	m_artist = metadata['TPE1']
	m_song = metadata['TIT2']
	m_album = metadata['TALB']
	m_date = metadata['TDRC']
	return {'artist':m_artist,
			'song':m_song,
			'album':m_album,
			'date':m_date}

def search(song, artist):
	musicbrainzngs.set_useragent("MusicOCD", "0.1", "https://github.com/asvas/MusicOCD")
	s = musicbrainzngs.search_recordings(song, artist=artist, country='US')
	artist = s['recording-list'][0]['artist-credit-phrase']
	s_id = s['recording-list'][0]['id']
	song = musicbrainzngs.get_recording_by_id(s_id)['recording']['title']
	album = ''
	date = 0
	for i in s['recording-list']:
		if i['artist-credit-phrase'] == artist:
			for j in i['release-list']:
				if 'release-group' in j and 'type' in j['release-group'] and 'date' in j:
					if j['release-group']['type'] == 'Album':
						for k in j['medium-list']:
							if k != {} and k['track-list'][0]['title'] == song:
								if date == 0:
									date = eval(j['date'][0:4])
									album = j['title']
								else:
									if eval(j['date'][0:4]) < date:
										album = j['title']
										date = eval(j['date'][0:4])
	return {'artist':artist,
			'song':song,
			'album':album,
			'date':date}

def evaluate(path):
	info_file = opener(path)
	info_web = search(info_file['song'],info_file['artist'])
	print(info_file['song'], '-->', info_web['song'])
	print(info_file['artist'], '-->', info_web['artist'])
	print(info_file['album'], '-->', info_web['album'])
	print(info_file['date'], '-->', info_web['date'])
	return [info_file, info_web]



def backup_info(info):
	info_back = info
	back_up = open('MusicOCD_BackUp.txt', 'a')
	back_up.write('o Edit date:\n')
	back_up.write(str(time.time()) + ' / ' + str(time.asctime()) + '\n')
	back_up.write('o Change:\n')
	back_up.write(str(info_back) + '\n')
	back_up.close()



def editor(path):
	l = evaluate(path)
	print(l)
	l[0]['date']=l[1]['date']
	print(l)
