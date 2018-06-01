
# import vk

# def extract_credentials(pathfile):
# 	access_token = None
# 	expires_in = None
# 	user_id = None
# 	with open(pathfile, 'r') as f:
# 		for line in f:
# 			#print(str(line))
# 			a, b = line.strip().split(':')
# 			#print(a)
# 			if a == 'access_token':
# 				#print("aaaaaaa")
# 				access_token = b
# 			if a == 'expires_in':
# 				expires_in = b
# 			if a == 'user_id':
# 				user_id = b
# 	#print(access_token)
# 	if int(expires_in) > 0:
# 		return access_token, expires_in, user_id
# 	else:
# 		return None, None, None




# access_token, expires_in, user_id = extract_credentials('credentials.txt')

# print("access_token_is " + str(access_token))
# print("user_id_is " + str(user_id))





import vk_api
from vk_api.audio import VkAudio
import collections



def extract_credentials(pathfile):
	login = None
	password = None
	with open(pathfile, 'r') as f:
		for line in f:
			#print(str(line))
			login, password = line.strip().split(':')
		return login, password




def main():
	""" Пример отображения 5 последних альбомов пользователя """

	login, password = extract_credentials('credentials.txt')
	vk_session = vk_api.VkApi(login, password)

	try:
		vk_session.auth()
	except vk_api.AuthError as error_msg:
		print(error_msg)
		return
		
	vkaudio = VkAudio(vk_session)

	artists = collections.Counter()


	while True:
		audios = vkaudio.get(owner_id=490446883)
		if not audios:
			print("break_was")
			break

		for audio in audios:
			artists[audio['artist']] += 1
			print(audio)
			print("audio")
		break


	# Составляем рейтинг первых 15
	print('\nTop 15:')
	print(artists)
	for artist, tracks in artists.most_common(15):
		print('{} - {} tracks'.format(artist, tracks))

	# Ищем треки самого популярного
	most_common_artist = artists.most_common(1)[0][0]

	print('\nSearch for', most_common_artist)

	tracks = vkaudio.search(q=most_common_artist)[:10]

	for n, track in enumerate(tracks, 1):
		print('{}. {} {}'.format(n, track['title'], track['url']))


if __name__ == '__main__':
	main()