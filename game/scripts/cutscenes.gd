class_name Cutscenes
## The demo's scripted scenes, as plain data so they are easy to rewrite.
## Each step can move the camera ("cam"), show a line ("who" + "text"), or just hold for a moment ("wait").
## A step with "needs" or "unless" is skipped depending on whether that hero is in the party.

static func intro(party_at: Vector2) -> Array:
	return [
		{"cam": party_at + Vector2(-60, 0), "wait": 1.2},
		{"who": "", "text": "Omega Island.\nThe smugglers' ship lies broken on the rocks. Beyond the beach the woods are black, and something in them is glowing."},
		{"who": "Leo", "text": "Emma, your arm. Hold still, I'll bind it."},
		{"who": "Emma", "text": "You're bleeding worse than I am."},
		{"who": "Leo", "text": "I'll manage. We need shelter before dark."},
		{"who": "Bender", "text": "Woof.", "needs": "bender"},
		{"who": "Emma", "text": "Bones held the Sawshark off for as long as he could. We can't waste it. East, through the trees."},
		{"cam": party_at + Vector2(260, 0), "wait": 1.0},
	]

static func boss(boss_at: Vector2, party_at: Vector2) -> Array:
	return [
		{"cam": boss_at, "wait": 1.4},
		{"who": "", "text": "Something vast shifts in the webbing."},
		{"who": "Emma", "text": "That's the nest. All of those lanterns came from her."},
		{"who": "Leo", "text": "Then she's the last thing between us and the far side. Behind me."},
		{"cam": party_at, "wait": 0.6},
	]

static func ending(party_at: Vector2) -> Array:
	return [
		{"cam": party_at, "wait": 1.0},
		{"who": "", "text": "The nest falls silent."},
		{"who": "Emma", "text": "Leo, look. A light, through the trees."},
		{"cam": party_at + Vector2(240, -40), "wait": 1.2},
		{"who": "Leo", "text": "A palace? Out here?"},
		{"who": "A voice", "text": "Two children wearing THAT insignia, trampling through my woods. Wonderful.", "unless": "cecil"},
		{"who": "Cecil", "text": "Omega Palace. Try not to touch anything.", "needs": "cecil"},
	]
