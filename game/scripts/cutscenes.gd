class_name Cutscenes
## The demo's scripted scenes, as plain data so they are easy to rewrite. Each step can:
##   "cam":   move the camera to a point
##   "who" + "text": show a line. A hero in the party speaks from a bubble over their head; narration ("who" empty)
##            and anyone off screen use the box at the foot of the screen
##   "acts":  [[hero, pose], ...] have heroes strike a pose (cheer, cry, scared, angry, think, hurt, guard, kneel, salute,
##            bark, whine, scoff, rage); "" goes back to standing
##   "walks": [[hero, offset], ...] walk a hero by an offset, or [[hero, offset, other hero]] to a spot beside someone
##   "wait":  hold for a moment (steps without text move on by themselves)
## A step with "needs" or "unless" is skipped depending on whether that hero is in the party.

static func intro(party_at: Vector2) -> Array:
	return [
		{"cam": party_at + Vector2(-70, 0), "wait": 1.4},
		{"who": "", "text": "Omega Island. The smugglers' ship lies broken on the rocks. Beyond the beach the woods are black, and something in them is glowing."},
		{"acts": [["emma", "hurt"]], "wait": 1.0},
		{"walks": [["leo", Vector2(-20, 3), "emma"]], "wait": 1.2},
		{"who": "Leo", "text": "Emma, your arm. Hold still, I'll bind it.", "acts": [["leo", "kneel"]]},
		{"who": "Emma", "text": "You're bleeding worse than I am."},
		{"who": "Leo", "text": "I'll manage. We need shelter before dark.", "acts": [["leo", ""]]},
		{"who": "Bender", "text": "Woof!", "needs": "bender", "acts": [["bender", "bark"]]},
		{"who": "Emma", "text": "Bones held the Sawshark off for as long as he could. We can't waste it. East, through the trees.", "acts": [["emma", "think"]]},
		{"cam": party_at + Vector2(130, 0), "acts": [["emma", ""], ["bender", ""]], "wait": 1.2},
	]

static func boss(boss_at: Vector2, party_at: Vector2) -> Array:
	return [
		{"cam": boss_at, "wait": 1.4},
		{"who": "", "text": "Something vast shifts in the webbing."},
		{"cam": party_at, "acts": [["emma", "scared"]], "wait": 0.8},
		{"who": "Emma", "text": "That's the nest. All of those lanterns came from her."},
		{"who": "Leo", "text": "Then she's the last thing between us and the far side. Behind me.", "acts": [["leo", "guard"]]},
		{"who": "Bender", "text": "Grrr...", "needs": "bender", "acts": [["bender", "bark"]]},
		{"wait": 0.4},
	]

static func ending(party_at: Vector2, palace: Vector2) -> Array:
	return [
		{"cam": party_at, "wait": 1.0},
		{"who": "", "text": "The nest falls silent."},
		{"cam": palace + Vector2(-150, -30), "wait": 1.6},
		{"who": "", "text": "Through the trees to the east, lanterns burn at a great iron gate."},
		{"cam": party_at, "wait": 0.6},
		{"who": "Emma", "text": "Leo, look! A light. Someone lives here.", "acts": [["emma", "cheer"]]},
		{"who": "Leo", "text": "A palace? Out here?", "acts": [["leo", "salute"]]},
		{"who": "A voice", "text": "Two children wearing THAT insignia, trampling through my woods. Wonderful.", "unless": "cecil", "acts": [["emma", "scared"], ["leo", "guard"]]},
		{"who": "Cecil", "text": "Omega Palace. Try not to touch anything.", "needs": "cecil", "acts": [["cecil", "scoff"]]},
	]
