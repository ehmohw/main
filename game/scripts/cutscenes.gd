class_name Cutscenes
## The demo's scripted scenes, as plain data so they are easy to rewrite. Each step can:
##   "cam":   move the camera to a point
##   "who" + "text": show a line, with "face" choosing the speaker's portrait (neutral, happy, sad, angry, scared, determined)
##   "acts":  [[hero, pose], ...] have heroes strike a pose (cheer, cry, scared, angry, think, hurt, guard, kneel, salute, ...); "" goes back to standing
##   "walks": [[hero, offset], ...] walk a hero by an offset, or [[hero, offset, other hero]] to a spot beside someone
##   "wait":  hold for a moment (steps without text move on by themselves)
## A step with "needs" or "unless" is skipped depending on whether that hero is in the party.

static func intro(party_at: Vector2) -> Array:
	return [
		{"cam": party_at + Vector2(-60, 0), "wait": 1.2},
		{"who": "", "text": "Omega Island.\nThe smugglers' ship lies broken on the rocks. Beyond the beach the woods are black, and something in them is glowing."},
		{"acts": [["emma", "hurt"]], "wait": 1.0},
		{"walks": [["leo", Vector2(-30, 4), "emma"]], "wait": 1.2},
		{"who": "Leo", "face": "scared", "text": "Emma, your arm. Hold still, I'll bind it.", "acts": [["leo", "kneel"]]},
		{"who": "Emma", "face": "sad", "text": "You're bleeding worse than I am."},
		{"who": "Leo", "face": "determined", "text": "I'll manage. We need shelter before dark.", "acts": [["leo", ""]]},
		{"who": "Bender", "text": "Woof.", "needs": "bender", "acts": [["bender", "bark"]]},
		{"who": "Emma", "face": "determined", "text": "Bones held the Sawshark off for as long as he could. We can't waste it. East, through the trees.", "acts": [["emma", "think"]]},
		{"cam": party_at + Vector2(260, 0), "wait": 1.0},
	]

static func boss(boss_at: Vector2, party_at: Vector2) -> Array:
	return [
		{"cam": boss_at, "wait": 1.4},
		{"who": "", "text": "Something vast shifts in the webbing."},
		{"cam": party_at, "acts": [["emma", "scared"]], "wait": 0.8},
		{"who": "Emma", "face": "scared", "text": "That's the nest. All of those lanterns came from her."},
		{"who": "Leo", "face": "determined", "text": "Then she's the last thing between us and the far side. Behind me.", "acts": [["leo", "guard"]]},
		{"wait": 0.5},
	]

static func ending(party_at: Vector2) -> Array:
	return [
		{"cam": party_at, "wait": 1.0},
		{"who": "", "text": "The nest falls silent."},
		{"who": "Emma", "face": "happy", "text": "Leo, look! A light, through the trees.", "acts": [["emma", "cheer"]]},
		{"cam": party_at + Vector2(240, -40), "wait": 1.2},
		{"who": "Leo", "face": "happy", "text": "A palace? Out here?", "acts": [["leo", "salute"]]},
		{"who": "A voice", "text": "Two children wearing THAT insignia, trampling through my woods. Wonderful.", "unless": "cecil", "acts": [["emma", "scared"], ["leo", "guard"]]},
		{"who": "Cecil", "face": "angry", "text": "Omega Palace. Try not to touch anything.", "needs": "cecil", "acts": [["cecil", "scoff"]]},
	]
