

# Example implementation for funky cards
# Subclassing would be better and would allow for grouping of similar effects
# (eg breakers that break "up to X" subroutines rather than exactly X
# (which actually turns out to be the case for most multi-sub breakers).
# this has a certain interaction with so-called "optional" subroutines.)
# another, better, simpler, example might be advanceable ice :P

# http://i.imgur.com/vxB2kXD.png
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
