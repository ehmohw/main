class_name SpriteLib
## Builds SpriteFrames for a character from the frame folders listed in Manifest.

static var _cache: Dictionary = {}

static func frames(who: String) -> SpriteFrames:
	if _cache.has(who):
		return _cache[who]
	var sf := SpriteFrames.new()
	sf.remove_animation("default")
	var anims: Dictionary = Manifest.DATA[who]["anims"]
	for anim: String in anims:
		sf.add_animation(anim)
		var cycle := anim.begins_with("walk") or anim.begins_with("idle")
		sf.set_animation_speed(anim, 10.0 if anim.begins_with("walk") or anim.begins_with("attack") else (5.0 if cycle else 8.0))
		sf.set_animation_loop(anim, cycle)      # attacks and cutscene emotes play once and hold
		for i in int(anims[anim]):
			sf.add_frame(anim, load("res://assets/chars/%s/%s/%d.png" % [who, anim, i]))
	_cache[who] = sf
	return sf

## Distance in pixels from the image centre down to the character's feet.
static func foot(who: String) -> float:
	return float(Manifest.DATA[who]["foot"])

static func has_anim(who: String, anim: String) -> bool:
	return Manifest.DATA[who]["anims"].has(anim)
