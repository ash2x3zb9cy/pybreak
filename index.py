from enum import Enum

# TODO: turn to dict bleh
RunnerFactions = Enum('RunnerFactions', 'Neutral Shaper Anarch Criminal SunnyLebeau Adam Apex')
CorpFactions = Enum('CorpFactions', 'Neutral Jinteki HaasBioroid NBN Weyland CorpMiniFactionsWhenFFGPls')

# The Breaker and Ice classes represent "Generic" base behaviour for icebreakers and ICE respectively.
# Anything that "Pumps X for Y" and "Breaks Z for W" is in the former,
# and anything that has A strength and B subroutines that could be considered generic is in the latter.
# This is much more frequent in ICE, as it's generally the breakers that have the fun breaking-related text,
# whereas the "generic" subroutines are where all the fun is on the Corp side,
# and modelling that is outside of scope.
# Ice examples: almost anything you can name: Wall of Static, Enigma, Neural Katana.
# Icebreaker examples: Corroder, Cyber-Cypher, Femme Fatale (without bypass).
# Note that the current implementation does, to some extent, support fixed-strength breakers (think Mimic, Yog.0),
# as well as "on encounter" costs (Tollbooth), though neither of these are very well implemented.

# This is the generic icebreaker's actual profile ftsoc:
"""
Generic breaker
Program: Icebreaker - AI
0 Install cost
0 MU
0 Strength
1[c]: Break ice subroutine.
1[c]: +1 strength.
"""
class Breaker():
	name = 'Generic breaker'
	# card subtypes eg "Fracter"
	subtype = ('Icebreaker', 'AI')

	# ICE subtypes that this hits eg "Barrier"
	# Note that some breakers (notably AIs) can break ANY ice
	# so empty subtype represents "ANY ice", not "NO ice"!
	target_subtype = ()

	# for conditional breakers such as D4v1d,
	# this will need to change
	def can_break(self, ice):
		# default behaviour: if the ice subtype is one we target,
		# or if our target list is empty
		if len(self.target_subtype) == 0:
			# This card targets 'ice subroutine'
			return True

		# if any subtype of target ice is in our range of breakable types
		for itype in ice.subtype:
			for btype in self.target_subtype:
				if itype == btype:
					return True

		return False

	# possibility of doing this part automatically??
	rules_text = '1[c]: break ice subroutine.\n1[c]: +1 strength.'
	flavour_text = ''

	faction = RunnerFactions.Neutral
	# regular influence cost - doesn't count for in-faction
	influence_cost = 0
	# universal influence - from MWL - costs regardless of in-faction-ness
	universal_influence_cost = 0

	# base strength
	strength = 0

	# creds
	install_cost = 0
	# MU requirement
	memory_cost = 0

	# cost to pump
	boost_cost = 0
	# strength gain per pump
	boost_amount = 1

	# cost to break subs
	break_cost = 0
	# amount of subs broken per use
	break_amount = 1

	# modifiable behaviour for weird cards like Paperclip
	def break_ice(self, ice, ignore_optional_subs=False):
		print('Using {} to break {}.'.format(self.name, ice.name))

		strength = get_or_call(self.strength, ice)
		cost = 0
		cost += get_or_call(ice.encounter_cost, self)

		target_strength = get_or_call(ice.strength, self)
		subs_remaining = get_or_call(ice.subroutine_count, self)
		if not ignore_optional_subs:
			subs_remaining += get_or_call(ice.optional_subroutine_count)

		print('{} has {} strength and {} subroutines.'.format(ice.name, target_strength, subs_remaining))

		# Pump
		while strength < target_strength:
			# fixed strength - can't boost :(
			# TODO: D A T A S U C K E R ?
			if get_or_call(self.boost_amount) == 0:
				# Todo: More informative error
				return -1

			pumpcost = get_or_call(self.boost_cost, ice)
			cost += pumpcost
			strength += get_or_call(self.boost_amount, ice)

			print('Pumped to {} for {} creds (total {})'.format(strength, pumpcost, cost))

		# Break
		while subs_remaining > 0:
			break_cost = get_or_call(self.break_cost, ice)
			break_amount = get_or_call(self.break_amount, ice)
			cost += break_cost
			subs_remaining -= break_amount
			print('Broke {} subroutine(s) for {} creds (total {}).'.format(break_amount, break_cost, cost))
		return cost

# If sth is a function, calls it with args, otherwise returns it
def get_or_call(sth, *args):
	# function or lambda or callable class
	if hasattr(sth, '__call__'):
		return sth(*args)
	else:
		return sth

class Ice():
	# Format for functions: attrname(self, breaker) -> int
	name = 'Vanilla ICE'
	flavour_text = ''
	subtype = ()
	strength = 0
	rez_cost = 0
	# I mean, implementing subroutine effects is somewhat out of scope.
	# Problem: Some ICE have beneficial subroutines (Little Engine's "The runner gains 5[c]."),
	# or ambiguous subroutines (Chetana's "Each player gains 2[c].").
	# Initial solution: Divide subs into "standard" subs and "optional" subs.
	# Additional problem: How to decide "optional" subs?
	# Is, for example, a trace optional?
	# For now, I guess the solution is to mark any subroutine that MAY do nothing as optional
	# trace, psi games, conditionally targetted effects ("Trash 1 AI program."), conditional effects ("End the run if the runner is tagged.")
	# are all examples of these
	subroutine_count = 0
	optional_subroutine_count = 0

	# crude implementation of eg. Tollbooth
	encounter_cost = 0

	# eg Swordsman can use this to check for AIs.
	# by default the ICE itself has no additional checks or rules
	def can_be_broken_by(self, breaker):
		return True


# Example implementation for funky cards
# Subclassing would be better and would allow for grouping of similar effects
# (eg breakers that break "up to X" subroutines rather than exactly X
# (which actually turns out to be the case for most multi-sub breakers).
# this has a certain interaction with so-called "optional" subroutines.)
# another, better, simpler, example might be advanceable ice :P

#https://scontent.xx.fbcdn.net/v/t34.0-12/18337296_1700113830004849_811033531_n.png?oh=c02427db1366bb13726a98b7707cd531&oe=5914181C
icet = Ice()
icet.subtype = ('Barrier', 'Tracer')
icet.name = 'Ice-T'

# rather than subclass and add an "advancements" field here's a hack
icet_advancements = 4

# X strength
icet.strength = lambda *args: icet_advancements
# X rez cost
icet.rez_cost = lambda *args: icet_advancements
# X subroutines (with trace x)
icet.subroutine_count = lambda *args: icet_advancements

# note that these *args are a lazy way of circumventing the expected format,
# because we don't care about anything except this hack variable.
# The correct form would be lambda self, breaker

bread = Breaker()
bread.name = "Gingerbread"
bread.subtype = ('Icebreaker')
bread.target_subtype = ('Tracer')
bread.boost_cost = 2
bread.boost_amount = 3
bread.break_cost = 1
bread.break_amount = 1
bread.strength = 2

print(
	"Gingerbread breaks a {}-advanced Ice-T for {} credits.".format(
		icet_advancements, bread.break_ice(icet)))
