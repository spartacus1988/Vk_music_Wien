import vk_api
from vk_api.audio import VkAudio
from vk_api.execute import VkFunction
import collections
import time
import sys


def extract_credentials(pathfile):
	login = None
	password = None
	with open(pathfile, 'r') as f:
		for line in f:
			login, password = line.strip().split(':')
		return login, password

def main():

	file_name = "%s_%s.txt" % (str(time.strftime("%Y-%m-%d")),str(time.strftime("%H%M%S")))	
	sys.stdout=open(file_name,"w")
	print(file_name)



	login, password = extract_credentials('credentials.txt')
	vk_session = vk_api.VkApi(login, password)

	try:
		vk_session.auth()
	except vk_api.AuthError as error_msg:
		print(error_msg)
		return

	vkaudio = VkAudio(vk_session)
	audios = None
	artists_by_people = collections.Counter()
	artists_by_tracks = collections.Counter()
	vk = vk_session.get_api()

	age_from=17
	age_to=17
	len_of_response = 0
	while True:
		response = vk.users.search(city = 198, count=1000, age_from = age_from, age_to = age_to)  
		time.sleep(0.33)
		
		if response['items']:
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
				sys.stdout.flush()
				#print(response['items'][0])
				try:
					audios = vkaudio.get(owner_id=item['id'])

					#определяем самого популярного исполнителя и юзера
					local_artists = collections.Counter()
					for audio in audios:
						local_artists[audio['artist']] += 1

					local_most_common_artist = local_artists.most_common(1)[0][0]
					print("local_most_common_artist " + local_most_common_artist)
					artists_by_people[local_most_common_artist] += 1

					#делаем срез последних 15 треков юзера и добавляем в общий список по исполнителям
					audios = audios[:15]
					for audio in audios:
						artists_by_tracks[audio['artist']] += 1
						#print(audio)
				except:
					pass


		# Составляем рейтинг первых 30 артистов по фанатам
		print('\nTop 30:')
		#print(artists_by_people)
		print("for users in age from 17 to " + str(age_from))
		for artist, tracks in artists_by_people.most_common(30):		
			print('{} - {} peoples'.format(artist, tracks))


		# Составляем рейтинг первых 30 артистов по количеству добавленных треков в 15 последних у юзеров
		print('\nTop 30:')
		#print(artists_by_tracks)
		print("for users in age from 17 to " + str(age_from))
		for artist, tracks in artists_by_tracks.most_common(30):		
			print('{} - {} tracks'.format(artist, tracks))

		
		print(str(time.strftime("%Y-%m-%d"))+"_"+str(time.strftime("%H%M%S")))
		sys.stdout.flush()
		age_from+=1
		age_to+=1
		if age_from > 35:
			sys.stdout.close()
			break


if __name__ == '__main__':
	main()