# -*- coding: utf-8 -*-

import requests
from datetime import datetime
import time
from igraph import Graph, plot
import numpy as np


domain = "https://api.vk.com/method"
access_token = 'f5de6aceb0fec3736d5a6b3288cc869c2937cd11bdbcd0f81e4f21ee08e1b3a0a914a98a58c179f01fd4b'  
user_id = int(input('Введите id пользователя: '))

query_params = {
    'domain' : domain,
    'access_token': access_token,
    'user_id': user_id,
    'fields': 'bdate'
}

query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v=5.53".format(**query_params)
response = requests.get(query)

def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
	delay = 0    
	query = url.format(**params)
	response = requests.get(query)
	print(response.status_code)
	for i in range(0, max_retries):
		if(response.status_code != 200):
			response = requests.get(query)
			delay = min(delay * backoff_factor, 5*3600)
			delay = delay + delay*random.normalvariate(0, 1)
			time.sleep(delay)
		else:
			break
	return response

def get_mutual_friends(params):

	url = "{domain}/friends.getMutual?access_token={access_token}&source_uid={source_uid}&target_uid={target_uid}&v=5.53"
	# query = url.format(**params)
	response = get(url, params)
	print(response.json())
	return get(url, params).json()['response']
	

def get_friends(user_id, fields):
    """ Returns a list of user IDs or detailed information about a user's friends """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    url = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v=5.53"
    response = get(url = url, params = query_params)
    
    return response.json()['response']['items'] #список словарей по каждому пользователю

def age_predict(user_id):

    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    friends_list = get_friends(user_id,'bdate')
    dates = []
    today = datetime.today()
    sum = 0
    for i in friends_list:
        if i.get("bdate") != None:
            if i['bdate'].count('.') == 2:
                dates.append(i['bdate'])
    for i in dates:
        dt = datetime.strptime(i,'%d.%m.%Y') #преобразуем строку в datetime
        sum += int((str(today - dt).split()[0]))/ 365.2425
    return round(sum/len(dates))

def get_users_ids_list():
	ids = []
	all_ids = []
	
	ids_pairs = []
	friends = get_friends(user_id,'id')[1:4]

	
	for i in friends:
		ids.append(i['id'])

	ids.sort()
	all_ids.extend(ids)

	print(ids)
	for i in ids:
		print(i)
		my_query_params = {
		    'domain' : domain,
		    'access_token': access_token,
		    'source_uid': user_id,
		    'target_uid': i
		}

		mutual_friends = get_mutual_friends(my_query_params)[:5]
		mutual_friends.sort()
		for friend in mutual_friends:
			ids_pairs.append((friend, user_id))
			ids_pairs.append((user_id, friend))
			ids_pairs.append((i, friend))
			ids_pairs.append((user_id, i))
			ids_pairs.append((i, user_id))
			ids_pairs.append((friend, i))
			all_ids.append(friend)
		time.sleep(1)

	keys = list(set(all_ids))
	ids_pairs = list(set(ids_pairs))
	keys.sort()
	ids_pairs.sort()

	print(keys)
	print(ids_pairs)
	return keys, ids_pairs


def get_network(user_ids, vertices, as_edgelist=True):

	g = Graph(vertex_attrs={"label":vertices},
    edges=user_ids, directed=False)

	N = len(vertices)
	print(N)
	visual_style = {}
	visual_style["layout"] = g.layout_fruchterman_reingold(
	    maxiter=1000,
	    area=N**3,
	    repulserad=N**3)

	g.simplify(multiple=True, loops=True)

	plot(g, **visual_style)


print(age_predict(user_id))

vertices, edges = get_users_ids_list()

get_network(edges, vertices)