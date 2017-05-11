import requests
import sys
import re

breakername = '.*{}.*'.format(sys.argv[1])
icename = '.*{}.*'.format(sys.argv[2])

icebreaker = []
ice = []

cards = requests.get('https://netrunnerdb.com/api/2.0/public/cards')

card_arr = cards.json()['data']

for x in card_arr:
	if x['type_code'] == 'program':
		# if this program is a breaker
		if 'keywords' in x and re.search('Icebreaker', x['keywords']):

			# filter by name
			if re.search(breakername, x['title'], re.I):
				icebreaker.append(x)

	if x['type_code'] == 'ice':

		# filter by name
		if re.search(icename, x['title'], re.I):
			ice.append(x)

fail = False

if icebreaker == []:
	print('No icebreaker found.')
	fail = True
if ice == []:
	print('No ICE found.')
	fail = True

# TODO: instead allow user to select?
if len(icebreaker) > 1:
	print('Found more than one icebreaker:')
	print(', '.join([x['title'] for x in icebreaker]))
	fail = True
if len(ice) > 1:
	print('Found more than one ICE:')
	print(', '.join([x['title'] for x in ice]))
	fail = True

if fail:
	print('\nUsage: python {} icebreaker ice'.format(sys.argv[0]))
	sys.exit(1)

ice = ice[0]
icebreaker = icebreaker[0]
print(ice)

# The hard part now is turning rules text paragraphs into code :P
# For now, slapping a big todo here.
# TODO: Parse rules text!