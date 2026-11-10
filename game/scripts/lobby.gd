class_name Lobby
extends Control
## The main menu, and the room where players pick their heroes before the game starts.

var game: Main
var _menu: Control
var _room: Control
var _msg: Label
var _ip: LineEdit
var _cards: Array = []
var _info: Label
var _start: Button

func build(game_: Main) -> void:
	game = game_
	size = Vector2(960, 540)
	var bg := ColorRect.new()
	bg.color = Color(0.05, 0.05, 0.1)
	bg.size = size
	add_child(bg)
	var title := game.label(self, Vector2(0, 40), "ETHERAVA", 44, Color(1, 0.9, 0.6))
	title.size = Vector2(960, 60)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	var sub := game.label(self, Vector2(0, 96), "Omega Island: the Lantern Woods  ·  demo", 16, Color(0.75, 0.8, 1.0))
	sub.size = Vector2(960, 24)
	sub.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER

	_menu = Control.new()
	add_child(_menu)
	_button(_menu, Vector2(330, 170), Vector2(300, 44), "Play on this computer", game.play_local)
	game.label(_menu, Vector2(330, 216), "1 to 4 players, sharing the screen", 12, Color(0.7, 0.7, 0.8))
	_button(_menu, Vector2(330, 256), Vector2(300, 44), "Host an online game", game.host_game)
	game.label(_menu, Vector2(330, 302), "Friends join you over the internet or your home network", 12, Color(0.7, 0.7, 0.8))
	_ip = LineEdit.new()
	_ip.position = Vector2(330, 342)
	_ip.size = Vector2(200, 44)
	_ip.placeholder_text = "Host's IP address"
	_menu.add_child(_ip)
	_button(_menu, Vector2(540, 342), Vector2(90, 44), "Join", func() -> void: game.join_game(_ip.text))
	_msg = game.label(_menu, Vector2(130, 410), "", 14, Color(1, 0.7, 0.5))
	_msg.size = Vector2(700, 60)
	_msg.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_msg.autowrap_mode = TextServer.AUTOWRAP_WORD

	_room = Control.new()
	add_child(_room)
	for i in Session.KINDS.size():
		var kind: String = Session.KINDS[i]
		var card := ColorRect.new()
		card.position = Vector2(52 + i * 218, 140)
		card.size = Vector2(200, 240)
		_room.add_child(card)
		var face := TextureRect.new()
		face.texture = load("res://assets/chars/%s/idle_south/0.png" % kind)
		face.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		face.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		face.position = Vector2(36, 8)
		face.size = Vector2(128, 128)
		card.add_child(face)
		var name_l := game.label(card, Vector2(0, 140), Hero.STATS[kind]["name"], 18)
		name_l.size = Vector2(200, 24)
		name_l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		var role := game.label(card, Vector2(0, 166), Hero.STATS[kind]["role"], 12, Color(0.75, 0.8, 0.95))
		role.size = Vector2(200, 20)
		role.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		var who := game.label(card, Vector2(0, 200), "", 14, Color(1, 0.9, 0.5))
		who.size = Vector2(200, 24)
		who.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		_cards.append({"card": card, "who": who})
	_info = game.label(_room, Vector2(80, 396), "", 13, Color(0.85, 0.85, 0.95))
	_info.size = Vector2(800, 70)
	_info.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_info.autowrap_mode = TextServer.AUTOWRAP_WORD
	_start = _button(_room, Vector2(380, 474), Vector2(200, 44), "Start", game.start_from_lobby)
	_button(_room, Vector2(20, 486), Vector2(100, 34), "Leave", func() -> void: game.leave())
	show_menu("")

func _button(parent: Control, pos: Vector2, size_: Vector2, text: String, action: Callable) -> Button:
	var b := Button.new()
	b.position = pos
	b.size = size_
	b.text = text
	b.focus_mode = Control.FOCUS_NONE
	b.pressed.connect(action)
	parent.add_child(b)
	return b

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
		if s["peer"] == 0:
			c["who"].text = "Computer"
			c["who"].add_theme_color_override("font_color", Color(0.6, 0.6, 0.7))
			c["card"].color = Color(0.11, 0.11, 0.18)
		elif s["peer"] == game.my_id:
			c["who"].text = "You" if mine == 1 else "Player on " + Session.dev_name(s["dev"])
			c["who"].add_theme_color_override("font_color", Color(1, 0.9, 0.5))
			c["card"].color = Color(0.22, 0.27, 0.5)
		else:
			c["who"].text = "Online player"
			c["who"].add_theme_color_override("font_color", Color(0.6, 1, 0.7))
			c["card"].color = Color(0.14, 0.26, 0.24)
	var text := "Join: press Space on the keyboard or A on a controller.   Change hero: left / right.   Step out: Esc or B.\nThe party is three heroes, or four with four players. The computer plays whoever isn't picked."
	if Session.mode == "host":
		var ips: Array = []
		for a: String in IP.get_local_addresses():
			if a.count(".") == 3 and not a.begins_with("127.") and not a.begins_with("169.254."):
				ips.append(a)
		text += "\nOn your home network, friends join with: %s" % ("  or  ".join(ips) if ips.size() > 0 else "this computer's IP address")
	elif Session.mode == "client":
		text += "\nThe host starts the game."
	_info.text = text
	_start.visible = game.is_host
	_start.disabled = Session.humans() == 0

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
