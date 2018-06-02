

import vk_api
from vk_api.audio import VkAudio
from vk_api.execute import VkFunction
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
		response = vk.users.search(city = 198, count=10, age_from = age_from, age_to = age_to)  
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

		


		if response['items']:
			for item in response['items']:
				print(item)
				print(item['id'])
				#print(response['items'][0])
				try:
					audios = vkaudio.get(owner_id=item['id'])
					local_artists = collections.Counter()
					for audio in audios:
						local_artists[audio['artist']] += 1
					local_most_common_artist = local_artists.most_common(1)[0][0]

					print("local_most_common_artist " + local_most_common_artist)

					artists[local_most_common_artist] += 1




					# for word in ['red', 'blue', 'red', 'green', 'blue', 'blue']:
					# cnt[word] += 1


					# >>> cnt
					# Counter({'blue': 3, 'red': 2, 'green': 1})


					# audios = audios[:10]
					# print(audios)
					#print("audios")
					#print(audios[:1])
				except:
					pass


				# if not audios:
				# 	print("break_was")
				# 	#break
				# 	pass
				# else:
				# 	artists[local_most_common_artist] += 1

				# 	# for audio in audios:
				# 	# 	artists[audio['artist']] += 1
				# 	# 	#print(artists)	




		


		# Составляем рейтинг первых 15
		print('\nTop 20:')
		#print(artists)
		print("for users in age from 17 to " + str(age_from))
		for artist, tracks in artists.most_common(20):		
			print('{} - {} peoples'.format(artist, tracks))


		#break
		age_from+=1
		age_to+=1
		if age_from > 28:
			break




	# Ищем треки самого популярного
	# most_common_artist = artists.most_common(1)[0][0]
	# print('\nSearch for', most_common_artist)
	# tracks = vkaudio.search(q=most_common_artist)[:10]
	# for n, track in enumerate(tracks, 1):
	# 	print('{}. {} {}'.format(n, track['title'], track['url']))





if __name__ == '__main__':
	main()