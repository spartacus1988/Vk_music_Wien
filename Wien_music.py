

import vk_api
from vk_api.audio import VkAudio
import collections
import time



def extract_credentials(pathfile):
	login = None
	password = None
	with open(pathfile, 'r') as f:
		for line in f:
			login, password = line.strip().split(':')
		return login, password




def main():
	

	login, password = extract_credentials('credentials.txt')
	vk_session = vk_api.VkApi(login, password)

	try:
		vk_session.auth()
	except vk_api.AuthError as error_msg:
		print(error_msg)
		return



	vkaudio = VkAudio(vk_session)
	audios = None
	artists = collections.Counter()

	vk = vk_session.get_api()


	#offset =0
	age_from=17
	age_to=17
	len_of_response = 0
	while True:
		response = vk.users.search(city = 198, count=1000, age_from = age_from, age_to = age_to)  
		time.sleep(1)
		#offset=100
		

		if response['items']:
			#print(response)

			print("age_is " + str(age_from))
			print("\r\n")

			print("len_of_current_age_is " + str(len(response['items'])))
			print("\r\n")



			len_of_response+=len(response['items'])
			print("summ_len_of_response_is " + str(len_of_response))
			print("\r\n")


		else:
			print("breaking.......")
			print(len(response['items']))
			break

		break
		#age_from+=1
		#age_to+=1


	if response['items']:
		for item in response['items']:
			print(item)
			print(item['id'])
			#print(response['items'][0])
			try:
				audios = vkaudio.get(owner_id=item['id'])
			except:
				pass


			if not audios:
				print("break_was")
				#break
				pass
			else:
				for audio in audios:
					artists[audio['artist']] += 1	




	


	# Составляем рейтинг первых 15
	print('\nTop 15:')
	#print(artists)
	print("for users in age " + str(age_from))
	for artist, tracks in artists.most_common(15):		
		print('{} - {} tracks'.format(artist, tracks))




	# Ищем треки самого популярного
	# most_common_artist = artists.most_common(1)[0][0]
	# print('\nSearch for', most_common_artist)
	# tracks = vkaudio.search(q=most_common_artist)[:10]
	# for n, track in enumerate(tracks, 1):
	# 	print('{}. {} {}'.format(n, track['title'], track['url']))





if __name__ == '__main__':
	main()