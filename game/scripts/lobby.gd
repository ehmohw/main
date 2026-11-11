class_name Lobby
extends Control
## The main menu, and the room where players pick their heroes before the game starts. Laid out for 640 x 360.

var game: Main
var _menu: Control
var _room: Control
var _msg: Label
var _ip: LineEdit
var _cards: Array = []
var _info: Label
var _room_title: Label
var _start: Button

func build(game_: Main) -> void:
	game = game_
	theme = UI.theme()
	size = UI.SCREEN
	_backdrop()
	UI.centred(self, Vector2(0, 24), 640, "ETHERAVA", 32, UI.GOLD)
	var rule := ColorRect.new()
	rule.color = Color(UI.GOLD, 0.6)
	rule.position = Vector2(250, 64)
	rule.size = Vector2(140, 1)
	add_child(rule)
	UI.centred(self, Vector2(0, 68), 640, "Omega Island: the Lantern Woods  ·  demo", 8, UI.TEAL)

	_menu = Control.new()
	add_child(_menu)
	UI.panel(_menu, Rect2(210, 100, 220, 182))
	UI.button(_menu, Rect2(226, 114, 188, 24), "Play on this computer", game.play_local)
	UI.centred(_menu, Vector2(226, 139), 188, "1 to 4 players sharing the screen", 8, UI.DIM)
	UI.button(_menu, Rect2(226, 160, 188, 24), "Host an online game", game.host_game)
	UI.centred(_menu, Vector2(226, 185), 188, "Friends join you over the network", 8, UI.DIM)
	_ip = LineEdit.new()
	_ip.position = Vector2(226, 206)
	_ip.custom_minimum_size = Vector2(126, 24)
	_ip.size = Vector2(126, 24)
	_ip.add_theme_font_size_override("font_size", 8)
	_ip.placeholder_text = "Host's IP address"
	_menu.add_child(_ip)
	UI.button(_menu, Rect2(356, 206, 58, 24), "Join", func() -> void: game.join_game(_ip.text))
	UI.centred(_menu, Vector2(226, 236), 188, "Join a friend who is hosting", 8, UI.DIM)
	UI.button(_menu, Rect2(226, 254, 188, 20), "Quit", func() -> void: get_tree().quit())
	_msg = UI.centred(_menu, Vector2(100, 290), 440, "", 8, Color("#ffb080"))
	_msg.size = Vector2(440, 30)
	_msg.autowrap_mode = TextServer.AUTOWRAP_WORD

	_room = Control.new()
	add_child(_room)
	_room_title = UI.centred(_room, Vector2(0, 84), 640, "Choose your heroes", 8, UI.TEXT, true)
	for i in Session.KINDS.size():
		var kind: String = Session.KINDS[i]
		var card := UI.panel(_room, Rect2(26 + i * 150, 100, 138, 148))
		var sprite := TextureRect.new()
		sprite.texture = load("res://assets/chars/%s/idle_south/0.png" % kind)
		sprite.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		sprite.stretch_mode = TextureRect.STRETCH_KEEP_CENTERED
		sprite.scale = Vector2(2, 2)
		sprite.size = Vector2(64, 48)
		sprite.position = Vector2(5, 2)
		sprite.mouse_filter = Control.MOUSE_FILTER_IGNORE
		card.add_child(sprite)
		UI.centred(card, Vector2(0, 100), 138, Hero.STATS[kind]["name"], 16, UI.TEXT, true)
		UI.centred(card, Vector2(0, 120), 138, Hero.STATS[kind]["role"], 8, UI.DIM)
		var who := UI.centred(card, Vector2(0, 133), 138, "", 8, UI.GOLD, true)
		_cards.append({"card": card, "who": who})
	_info = UI.centred(_room, Vector2(40, 254), 560, "", 8, UI.DIM)
	_info.size = Vector2(560, 50)
	_info.autowrap_mode = TextServer.AUTOWRAP_WORD
	_info.add_theme_constant_override("line_spacing", 3)
	_start = UI.button(_room, Rect2(250, 316, 140, 26), "Start", game.start_from_lobby)
	UI.button(_room, Rect2(14, 324, 64, 20), "Leave", func() -> void: game.leave())
	show_menu("")

## A dusk sky, a glow on the horizon and a row of dark trees.
func _backdrop() -> void:
	var sky := TextureRect.new()
	var g := Gradient.new()
	g.set_color(0, Color("#0a0918"))
	g.add_point(0.6, Color("#1b1840"))
	g.set_color(g.get_point_count() - 1, Color("#3a2450"))
	var gt := GradientTexture2D.new()
	gt.gradient = g
	gt.fill_from = Vector2(0, 0)
	gt.fill_to = Vector2(0, 1)
	gt.width = 4
	gt.height = 90
	sky.texture = gt
	sky.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	sky.size = UI.SCREEN
	add_child(sky)
	var glow := TextureRect.new()
	glow.texture = UI.glow(128, Color(1.0, 0.6, 0.25, 0.35), Color(1.0, 0.6, 0.25, 0.0))
	glow.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	glow.position = Vector2(170, 250)
	glow.size = Vector2(300, 200)
	add_child(glow)
	var rng := RandomNumberGenerator.new()
	rng.seed = 11
	var x := -30.0
	while x < 660.0:
		var t := Sprite2D.new()
		t.texture = load("res://assets/props/%s.png" % ["tree_a", "tree_b", "tree_c"][rng.randi() % 3])
		t.position = Vector2(x, 372.0 - t.texture.get_height() / 2.0 + rng.randf_range(0, 26))
		t.modulate = Color(0.16, 0.14, 0.3)
		t.flip_h = rng.randf() < 0.5
		add_child(t)
		x += rng.randf_range(34, 58)
	var flies := CPUParticles2D.new()
	flies.amount = 18
	flies.lifetime = 6.0
	flies.preprocess = 6.0
	flies.position = Vector2(320, 250)
	flies.emission_shape = CPUParticles2D.EMISSION_SHAPE_RECTANGLE
	flies.emission_rect_extents = Vector2(320, 100)
	flies.spread = 180.0
	flies.gravity = Vector2.ZERO
	flies.initial_velocity_min = 2.0
	flies.initial_velocity_max = 7.0
	flies.scale_amount_max = 2.0
	var ramp := Gradient.new()
	ramp.set_color(0, Color(1, 0.9, 0.5, 0))
	ramp.add_point(0.5, Color(1, 0.9, 0.5, 0.8))
	ramp.set_color(ramp.get_point_count() - 1, Color(1, 0.9, 0.5, 0))
	flies.color_ramp = ramp
	add_child(flies)

func show_menu(message: String) -> void:
	visible = true
	_menu.visible = true
	_room.visible = false
	_msg.text = message

func show_room() -> void:
	visible = true
	_menu.visible = false
	_room.visible = true
	refresh()

func refresh() -> void:
	if _room == null or Session.seats.size() != _cards.size():
		return
	var mine := 0
	for s: Dictionary in Session.seats:
		if s["peer"] == game.my_id:
			mine += 1
	for i in _cards.size():
		var s: Dictionary = Session.seats[i]
		var c: Dictionary = _cards[i]
		var who: Label = c["who"]
		var edge := UI.EDGE
		var bg := UI.PANEL
		if s["peer"] == 0:
			who.text = "Computer"
			who.add_theme_color_override("font_color", Color("#6a6888"))
		elif s["peer"] == game.my_id:
			edge = UI.PLAYER[clampi(s["dev"], 0, 3)]
			bg = UI.PANEL_LIT
			who.text = "You" if mine == 1 else "Player on " + Session.dev_name(s["dev"])
			who.add_theme_color_override("font_color", edge)
		else:
			edge = UI.TEAL
			bg = Color("#17322f")
			who.text = "Online player"
			who.add_theme_color_override("font_color", UI.TEAL)
		c["card"].add_theme_stylebox_override("panel", UI.box(Color(bg, 0.92), edge, 3))
	var text := "Join: Space on the keyboard, or A on a controller.     Change hero: left / right.     Step out: Esc or B.\nA run takes three heroes, or four with four players. The computer plays whoever isn't picked."
	if Session.mode == "host":
		var ips: Array = []
		for a: String in IP.get_local_addresses():
			if a.count(".") == 3 and not a.begins_with("127.") and not a.begins_with("169.254."):
				ips.append(a)
		text += "\nOn your home network, friends join with:  %s" % ("  or  ".join(ips) if ips.size() > 0 else "this computer's IP address")
		_room_title.text = "Hosting: choose your heroes"
	elif Session.mode == "client":
		text += "\nThe host starts the game."
		_room_title.text = "Joined: choose your heroes"
	else:
		_room_title.text = "Choose your heroes"
	_info.text = text
	_start.visible = game.is_host
	_start.disabled = Session.humans() == 0
	_start.text = "Start" if Session.humans() > 0 else "Join to start"

func _process(_delta: float) -> void:
	if not visible or not _room.visible:
		return
	for dev in game.pads.size():
		var pad: Dictionary = game.pads[dev]
		if pad["attack_just"]:
			game.to_host("claim", [dev, 0])
		elif pad["right_just"]:
			game.to_host("claim", [dev, 1])
		elif pad["left_just"]:
			game.to_host("claim", [dev, -1])
		elif pad["back_just"]:
			game.to_host("claim", [dev, 2])
		if game.is_host and pad["restart_just"] and dev > 0:
			game.start_from_lobby()       # Start button on a controller
