class_name Main
extends Node2D
## Omega Island: the Lantern Woods, for one to four players on one screen, online, or both.
## One machine is the host: it runs the enemies, damage and progress, and tells the others what happened.
## Every machine moves its own players' heroes and tells the host where they are.

const PORT := 24565
const FIELD_W := 5400.0
const TOP := 170.0
const BOT := 830.0
const ZONES := [
	{"start": 600.0, "gate": 1700.0, "spawn": {"lantern": 7},
		"line": "Leo: \"Lanterns in the trees. Stay behind me, Emma.\"", "goal": "Clear the Arachno-Lanterns"},
	{"start": 1700.0, "gate": 2900.0, "spawn": {"lantern": 7, "stalker": 3},
		"line": "Emma: \"Stalkers hunt whoever is weakest. Keep together.\"", "goal": "Survive the Stalkers"},
	{"start": 2900.0, "gate": 4200.0, "spawn": {"lantern": 3, "sac": 6},
		"line": "Emma: \"Egg sacs! Break them before they hatch.\"", "goal": "Destroy the egg sacs"},
	{"start": 4200.0, "gate": -1.0, "spawn": {"boss": 1},
		"line": "The Brood Lantern wakes.", "goal": "Defeat the Brood Lantern"},
]

var heroes: Array[Hero] = []
var enemies: Array[Enemy] = []
var level := 1
var xp := 0
var embers := 0
var over := false
var autopilot := false
var started := false
var is_host := true
var my_id := 1
var networked := false
var light_tex: GradientTexture2D
var pads: Array = []          # one entry per input device: 0 is the keyboard, 1 to 4 are controllers

var _world: Node2D
var _fx: Node2D
var _ground_fx: Node2D
var _lights: Node2D
var _tracked: Array = []
var _camera: Camera2D
var _lobby: Lobby
var _zone := 0
var _zone_active := false
var _gates: Array = []
var _boss: Enemy
var _hud := {}
var _toast_t := 0.0
var _clock := 0.0
var _end_t := -1.0
var _by_id := {}
var _next_id := 1
var _pickups := {}
var _next_pick := 1
var _snap_t := 0.0
var _prev_keys := {}
# cutscenes
var cut := false
var _intro_t := -1.0
var _cut_steps: Array = []
var _cut_i := 0
var _cut_done := Callable()
var _cut_cam: Variant = null
var _cut_wait := -1.0
var _cut_chars := 0.0
# automated playtests
var _shots_dir := ""
var _shot_t := 0.0
var _shot_n := 0
var _net_test := ""
var _log_t := 0.0
var _test_t := 0.0

func _ready() -> void:
	randomize()
	for a: String in OS.get_cmdline_user_args():
		if a.begins_with("--shots="):
			_shots_dir = a.trim_prefix("--shots=")
			autopilot = true
		if a.begins_with("--net-test="):
			_net_test = a.trim_prefix("--net-test=")
			autopilot = true
	_setup_input()
	_build_light()
	_poll()
	multiplayer.connected_to_server.connect(_on_connected)
	multiplayer.connection_failed.connect(_on_failed)
	multiplayer.server_disconnected.connect(_on_host_left)
	multiplayer.peer_connected.connect(_on_peer_joined)
	multiplayer.peer_disconnected.connect(_on_peer_left)
	var layer := CanvasLayer.new()
	layer.layer = 20
	add_child(layer)
	_lobby = Lobby.new()
	layer.add_child(_lobby)
	_lobby.build(self)
	_refresh_ids()
	if Session.in_game:
		_begin_game()
	elif _shots_dir != "" and _net_test == "":
		play_local()
		Session.seats[0] = {"peer": 1, "dev": 0}
		start_from_lobby()
	elif _net_test == "host":
		host_game()
		claim(0, 0)
	elif _net_test == "client":
		join_game("127.0.0.1")
	else:
		_lobby.show_menu(Session.message)
		Session.message = ""

# ---------------------------------------------------------------- connecting

func _refresh_ids() -> void:
	my_id = multiplayer.get_unique_id()
	is_host = multiplayer.is_server()
	networked = Session.mode == "host" or Session.mode == "client"

func play_local() -> void:
	multiplayer.multiplayer_peer = OfflineMultiplayerPeer.new()
	Session.mode = "local"
	Session.reset_seats()
	_refresh_ids()
	_lobby.show_room()

func host_game() -> void:
	var peer := ENetMultiplayerPeer.new()
	if peer.create_server(PORT, 3) != OK:
		_lobby.show_menu("Couldn't host: port %d is already in use on this computer." % PORT)
		return
	multiplayer.multiplayer_peer = peer
	Session.mode = "host"
	Session.reset_seats()
	_refresh_ids()
	_lobby.show_room()

func join_game(address: String) -> void:
	var peer := ENetMultiplayerPeer.new()
	if address.strip_edges() == "" or peer.create_client(address.strip_edges(), PORT) != OK:
		_lobby.show_menu("That address didn't work. Enter the host's IP address.")
		return
	multiplayer.multiplayer_peer = peer
	Session.mode = "client"
	Session.reset_seats()
	_lobby.show_menu("Connecting to %s..." % address.strip_edges())

func leave(message := "") -> void:
	multiplayer.multiplayer_peer = OfflineMultiplayerPeer.new()
	Session.mode = ""
	Session.in_game = false
	Session.message = message
	get_tree().reload_current_scene()

func _on_connected() -> void:
	_refresh_ids()
	_lobby.show_room()
	if _net_test == "client":
		to_host("claim", [0, 0])

func _on_failed() -> void:
	leave("Couldn't reach the host. Check the address, and that the host has started hosting.")

func _on_host_left() -> void:
	if _net_test != "":
		print("RESULT host left; over=%s" % over)
		get_tree().quit()
		return
	leave("The host left the game.")

func _on_peer_joined(id: int) -> void:
	if is_host:
		sync_seats.rpc_id(id, Session.seats)

func _on_peer_left(id: int) -> void:
	if not is_host:
		return
	for s: Dictionary in Session.seats:
		if s["peer"] == id:      # the computer takes over their hero
			s["peer"] = 0
			s["dev"] = -1
	_share_seats()

## Run something on the host: directly if that's us, over the network if not.
func to_host(method: String, args: Array) -> void:
	if is_host:
		callv(method, args)
	else:
		callv("rpc_id", [1, method] + args)

func _sender() -> int:
	var id := multiplayer.get_remote_sender_id()
	return my_id if id == 0 else id

func _share_seats() -> void:
	sync_seats(Session.seats)
	if networked:
		sync_seats.rpc(Session.seats)

func _seat_of(peer: int, dev: int) -> int:
	for i in Session.seats.size():
		if Session.seats[i]["peer"] == peer and Session.seats[i]["dev"] == dev:
			return i
	return -1

## Lobby: join (0), move to the next free hero (+1 / -1), or leave (2).
@rpc("any_peer", "call_remote", "reliable")
func claim(dev: int, action: int) -> void:
	if not is_host or started:
		return
	var peer := _sender()
	var cur := _seat_of(peer, dev)
	var n := Session.seats.size()
	if cur == -1:
		if action == 0:
			for i in n:
				if Session.seats[i]["peer"] == 0:
					Session.seats[i] = {"peer": peer, "dev": dev}
					break
	elif action == 2:
		Session.seats[cur] = {"peer": 0, "dev": -1}
	elif action == 1 or action == -1:
		for k in range(1, n):
			var j := (cur + action * k + n * 2) % n
			if Session.seats[j]["peer"] == 0:
				Session.seats[j] = Session.seats[cur]
				Session.seats[cur] = {"peer": 0, "dev": -1}
				break
	_share_seats()

@rpc("authority", "call_remote", "reliable")
func sync_seats(seats: Array) -> void:
	Session.seats = seats
	_lobby.refresh()
	var s := 1
	for h in heroes:
		if not h.is_player():
			h.slot = s
			s += 1

func start_from_lobby() -> void:
	if not is_host or started or Session.humans() == 0:
		return
	# the party is three heroes, or four when four people play: every player's pick, then the computer's in roster order
	var chosen: Array = []
	for i in Session.KINDS.size():
		if Session.seats[i]["peer"] != 0:
			chosen.append(i)
	for i in Session.KINDS.size():
		if chosen.size() < 3 and not chosen.has(i):
			chosen.append(i)
	chosen.sort()
	var party: Array = []
	var seats: Array = []
	for i: int in chosen:
		party.append(Session.KINDS[i])
		seats.append(Session.seats[i])
	if networked:
		begin.rpc(party, seats)
	begin(party, seats)

@rpc("authority", "call_remote", "reliable")
func begin(party: Array, seats: Array) -> void:
	Session.party = party
	Session.seats = seats
	Session.in_game = true
	_begin_game()

func _begin_game() -> void:
	started = true
	_refresh_ids()
	_lobby.visible = false
	_build_level()
	_build_party()
	_build_hud()
	sync_seats(Session.seats)
	_intro_t = 0.8

@rpc("authority", "call_remote", "reliable")
func restart() -> void:
	get_tree().reload_current_scene()

# ---------------------------------------------------------------- input

func _setup_input() -> void:
	var keys := {
		"move_left": [KEY_A, KEY_LEFT], "move_right": [KEY_D, KEY_RIGHT], "move_up": [KEY_W, KEY_UP], "move_down": [KEY_S, KEY_DOWN],
		"attack": [KEY_SPACE, KEY_J], "switch_next": [KEY_TAB, KEY_E], "switch_prev": [KEY_Q], "restart": [KEY_R], "back": [KEY_ESCAPE],
	}
	for action: String in keys:
		if InputMap.has_action(action):
			continue
		InputMap.add_action(action)
		for k: int in keys[action]:
			var ev := InputEventKey.new()
			ev.physical_keycode = k
			InputMap.action_add_event(action, ev)
		if action == "attack":
			var click := InputEventMouseButton.new()
			click.button_index = MOUSE_BUTTON_LEFT
			InputMap.action_add_event("attack", click)

## Reads every device once a frame, so heroes and the lobby all see the same thing.
func _poll() -> void:
	var out: Array = []
	for dev in 5:
		var d := {"move": Vector2.ZERO, "attack": false, "next": false, "prev": false, "left": false, "right": false, "restart": false, "back": false, "there": dev == 0}
		var raw := {}
		if dev == 0:
			d["move"] = Input.get_vector("move_left", "move_right", "move_up", "move_down")
			raw = {"attack": Input.is_action_pressed("attack") and (started or not Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT)),
				"next": Input.is_action_pressed("switch_next"), "prev": Input.is_action_pressed("switch_prev"),
				"left": Input.is_action_pressed("move_left"), "right": Input.is_action_pressed("move_right"),
				"restart": Input.is_action_pressed("restart"), "back": Input.is_action_pressed("back")}
		elif Input.get_connected_joypads().has(dev - 1):
			var j := dev - 1
			d["there"] = true
			var stick := Vector2(Input.get_joy_axis(j, JOY_AXIS_LEFT_X), Input.get_joy_axis(j, JOY_AXIS_LEFT_Y))
			if stick.length() < 0.25:
				stick = Vector2.ZERO
			stick.x += float(Input.is_joy_button_pressed(j, JOY_BUTTON_DPAD_RIGHT)) - float(Input.is_joy_button_pressed(j, JOY_BUTTON_DPAD_LEFT))
			stick.y += float(Input.is_joy_button_pressed(j, JOY_BUTTON_DPAD_DOWN)) - float(Input.is_joy_button_pressed(j, JOY_BUTTON_DPAD_UP))
			d["move"] = stick.limit_length(1.0)
			raw = {"attack": Input.is_joy_button_pressed(j, JOY_BUTTON_A) or Input.is_joy_button_pressed(j, JOY_BUTTON_X) or Input.get_joy_axis(j, JOY_AXIS_TRIGGER_RIGHT) > 0.5,
				"next": Input.is_joy_button_pressed(j, JOY_BUTTON_RIGHT_SHOULDER), "prev": Input.is_joy_button_pressed(j, JOY_BUTTON_LEFT_SHOULDER),
				"left": stick.x < -0.6, "right": stick.x > 0.6,
				"restart": Input.is_joy_button_pressed(j, JOY_BUTTON_START), "back": Input.is_joy_button_pressed(j, JOY_BUTTON_B)}
		for k: String in raw:
			var key := "%d%s" % [dev, k]
			d[k] = raw[k]
			d[k + "_just"] = raw[k] and not _prev_keys.get(key, false)
			_prev_keys[key] = raw[k]
		for k: String in ["attack", "next", "prev", "left", "right", "restart", "back"]:
			if not d.has(k + "_just"):
				d[k + "_just"] = false
		out.append(d)
	pads = out

# ---------------------------------------------------------------- building the level

func _build_light() -> void:
	var g := Gradient.new()
	g.set_color(0, Color(1, 1, 1, 1))
	g.set_color(1, Color(1, 1, 1, 0))
	light_tex = GradientTexture2D.new()
	light_tex.gradient = g
	light_tex.fill = GradientTexture2D.FILL_RADIAL
	light_tex.fill_from = Vector2(0.5, 0.5)
	light_tex.fill_to = Vector2(1.0, 0.5)
	light_tex.width = 256
	light_tex.height = 256

func _wall(rect: Rect2) -> StaticBody2D:
	var body := StaticBody2D.new()
	body.collision_layer = 4
	body.collision_mask = 0
	var shape := CollisionShape2D.new()
	var r := RectangleShape2D.new()
	r.size = rect.size
	shape.shape = r
	body.position = rect.get_center()
	body.add_child(shape)
	add_child(body)
	return body

func _prop(tex_name: String, pos: Vector2, light := Color(0, 0, 0, 0), solid := 0.0) -> Sprite2D:
	var s := Sprite2D.new()
	s.texture = load("res://assets/props/%s.png" % tex_name)
	s.offset = Vector2(0, -s.texture.get_height() / 2.0 + 8)
	s.position = pos
	_world.add_child(s)
	if light.a > 0.0:
		add_light(null, light, 1.6, 0.9, pos + Vector2(0, -14))
	if solid > 0.0:
		var body := StaticBody2D.new()
		body.collision_layer = 4
		body.collision_mask = 0
		var shape := CollisionShape2D.new()
		var c := CircleShape2D.new()
		c.radius = solid
		shape.shape = c
		body.add_child(shape)
		s.add_child(body)
	return s

func _build_level() -> void:
	var rng := RandomNumberGenerator.new()
	rng.seed = 2026      # the same wood on every machine
	var ground := Sprite2D.new()
	ground.texture = load("res://assets/props/ground.png")
	ground.centered = false
	ground.region_enabled = true
	ground.region_rect = Rect2(0, 0, FIELD_W + 400, BOT + 500)
	ground.texture_repeat = CanvasItem.TEXTURE_REPEAT_ENABLED
	ground.position = Vector2(-200, -100)
	ground.z_index = -10
	add_child(ground)
	var dark := CanvasModulate.new()
	dark.color = Color(0.36, 0.34, 0.52)
	add_child(dark)
	_ground_fx = Node2D.new()
	_ground_fx.z_index = -5
	add_child(_ground_fx)
	_lights = Node2D.new()
	add_child(_lights)
	# characters and scenery sit on their own layer with an even dusk tint, so the ground's lights never wash them out
	var world_layer := CanvasLayer.new()
	world_layer.layer = 1
	world_layer.follow_viewport_enabled = true
	add_child(world_layer)
	var dusk := CanvasModulate.new()
	dusk.color = Color(0.72, 0.72, 0.9)
	world_layer.add_child(dusk)
	_world = Node2D.new()
	_world.y_sort_enabled = true
	world_layer.add_child(_world)
	var fx_layer := CanvasLayer.new()
	fx_layer.layer = 2
	fx_layer.follow_viewport_enabled = true
	add_child(fx_layer)
	_fx = Node2D.new()
	fx_layer.add_child(_fx)
	# the edges of the wood
	_wall(Rect2(-200, TOP - 200, FIELD_W + 400, 200))
	_wall(Rect2(-200, BOT, FIELD_W + 400, 200))
	_wall(Rect2(-160, TOP, 200, BOT - TOP))
	_wall(Rect2(FIELD_W - 40, TOP, 200, BOT - TOP))
	var x := -60.0
	while x < FIELD_W + 100:
		for row in 2:
			_prop("tree1" if rng.randf() < 0.5 else "tree2", Vector2(x + rng.randf_range(-25, 25), TOP - 10 - row * 60 - rng.randf_range(0, 30)))
			_prop("tree1" if rng.randf() < 0.5 else "tree2", Vector2(x + rng.randf_range(-25, 25), BOT + 150 + row * 70 + rng.randf_range(0, 30)))
		x += rng.randf_range(70, 105)
	# rocks, lanterns of the dead, webs
	for i in 22:
		var p := Vector2(rng.randf_range(300, FIELD_W - 500), rng.randf_range(TOP + 60, BOT - 40))
		if _near_gate(p.x, 120.0) or p.x < 420:
			continue
		_prop("rock", p, Color(0, 0, 0, 0), 20.0)
	x = 260.0
	while x < FIELD_W - 100:
		_prop("pumpkin", Vector2(x, TOP + 26 if int(x / 380.0) % 2 == 0 else BOT - 14), Color(1.0, 0.6, 0.2))
		x += 380.0
	for i in 26:
		var w := Sprite2D.new()
		w.texture = load("res://assets/props/web.png")
		w.position = Vector2(rng.randf_range(700, FIELD_W - 100), rng.randf_range(TOP + 40, BOT - 40))
		w.modulate = Color(1, 1, 1, 0.35)
		w.rotation = rng.randf() * TAU
		_ground_fx.add_child(w)
	# web gates between the zones
	for z: Dictionary in ZONES:
		if z["gate"] < 0:
			_gates.append(null)
			continue
		var gate := _wall(Rect2(z["gate"] - 20, TOP, 40, BOT - TOP))
		var y := TOP + 30
		while y < BOT:
			var w := Sprite2D.new()
			w.texture = load("res://assets/props/web.png")
			w.position = Vector2(0, y - (TOP + BOT) / 2.0)
			w.scale = Vector2(0.8, 1.0)
			gate.add_child(w)
			y += 80.0
		_gates.append(gate)
	_camera = Camera2D.new()
	_camera.limit_left = 0
	_camera.limit_right = int(FIELD_W)
	_camera.limit_top = int(TOP - 150)
	_camera.limit_bottom = int(BOT + 130)
	_camera.position_smoothing_enabled = true
	_camera.position_smoothing_speed = 6.0
	add_child(_camera)
	_camera.make_current()

func _near_gate(x: float, margin: float) -> bool:
	for z: Dictionary in ZONES:
		if absf(x - z["gate"]) < margin or absf(x - z["start"]) < margin:
			return true
	return false

func _build_party() -> void:
	for i in Session.party.size():
		var h := Hero.new()
		_world.add_child(h)
		h.setup(self, i)
		h.position = Vector2(240 - i * 46, (TOP + BOT) / 2.0 + (i - 1.5) * 44)
		h.net_pos = h.position
		h.facing = Vector2.RIGHT
		heroes.append(h)

# ---------------------------------------------------------------- HUD

func _bar(parent: Node, pos: Vector2, size: Vector2, fill: Color) -> Bar:
	var b := Bar.new()
	b.position = pos
	b.size = size
	b.color = Color(0.05, 0.04, 0.09, 0.95)
	b.fill = ColorRect.new()
	b.fill.color = fill
	b.fill.position = Vector2(1, 1)
	b.add_child(b.fill)
	parent.add_child(b)
	return b

func label(parent: Node, pos: Vector2, text: String, size := 14, colour := Color.WHITE) -> Label:
	var l := Label.new()
	l.position = pos
	l.text = text
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_color_override("font_color", colour)
	l.add_theme_color_override("font_outline_color", Color(0, 0, 0))
	l.add_theme_constant_override("outline_size", 4)
	parent.add_child(l)
	return l

func _build_hud() -> void:
	var layer := CanvasLayer.new()
	layer.layer = 10
	add_child(layer)
	var root := Control.new()
	layer.add_child(root)
	_hud["play"] = root
	_hud["panels"] = []
	for i in heroes.size():
		var h := heroes[i]
		var panel := ColorRect.new()
		panel.position = Vector2(10, 10 + i * 44)
		panel.size = Vector2(200, 40)
		root.add_child(panel)
		var face := TextureRect.new()
		face.texture = load("res://assets/chars/%s/idle_south/0.png" % h.kind)
		face.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		face.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		face.position = Vector2(2, 2)
		face.size = Vector2(36, 36)
		panel.add_child(face)
		var name_l := label(panel, Vector2(42, 0), h.display_name, 13)
		var bar := _bar(panel, Vector2(42, 22), Vector2(150, 12), Color(0.35, 0.85, 0.45))
		_hud["panels"].append({"panel": panel, "bar": bar, "name": name_l})
	_hud["level"] = label(root, Vector2(770, 8), "Level 1", 14, Color(1, 0.9, 0.5))
	_hud["xp"] = _bar(root, Vector2(770, 31), Vector2(180, 7), Color(0.55, 0.5, 1.0))
	_hud["embers"] = label(root, Vector2(770, 44), "Soul embers: 0", 13, Color(0.7, 0.9, 1.0))
	_hud["goal"] = label(root, Vector2(230, 10), "Head east through the woods", 14, Color(1, 0.95, 0.8))
	_hud["goal"].size = Vector2(500, 20)
	_hud["goal"].horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_hud["toast"] = label(root, Vector2(130, 440), "", 15)
	_hud["toast"].size = Vector2(700, 50)
	_hud["toast"].horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_hud["toast"].autowrap_mode = TextServer.AUTOWRAP_WORD
	_hud["hint"] = label(root, Vector2(10, 516), "Move: WASD / arrows / stick    Attack: Space, click or A    Switch hero: Tab, Q / E or bumpers", 11, Color(0.8, 0.8, 0.9))
	_hud["boss_name"] = label(root, Vector2(280, 478), "The Brood Lantern", 14, Color(1, 0.7, 0.4))
	_hud["boss_name"].size = Vector2(400, 20)
	_hud["boss_name"].horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_hud["boss"] = _bar(root, Vector2(280, 500), Vector2(400, 12), Color(0.95, 0.45, 0.15))
	# cutscenes: letterbox bars and a dialogue box
	var cutbox := Control.new()
	cutbox.visible = false
	layer.add_child(cutbox)
	_hud["cut"] = cutbox
	for r: Rect2 in [Rect2(0, 0, 960, 50), Rect2(0, 396, 960, 144)]:
		var band := ColorRect.new()
		band.color = Color(0.02, 0.02, 0.04)
		band.position = r.position
		band.size = r.size
		cutbox.add_child(band)
	var face2 := TextureRect.new()
	face2.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	face2.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	face2.position = Vector2(24, 408)
	face2.size = Vector2(120, 120)
	cutbox.add_child(face2)
	_hud["cut_face"] = face2
	_hud["cut_who"] = label(cutbox, Vector2(160, 404), "", 16, Color(1, 0.9, 0.5))
	_hud["cut_text"] = label(cutbox, Vector2(160, 430), "", 15)
	_hud["cut_text"].size = Vector2(760, 84)
	_hud["cut_text"].autowrap_mode = TextServer.AUTOWRAP_WORD
	_hud["cut_hint"] = label(cutbox, Vector2(660, 516), "Space / A: next      Esc / B: skip scene", 11, Color(0.7, 0.7, 0.8))
	var shade := ColorRect.new()
	shade.color = Color(0, 0, 0, 0.7)
	shade.size = Vector2(960, 540)
	shade.visible = false
	layer.add_child(shade)
	_hud["shade"] = shade
	_hud["end_title"] = label(shade, Vector2(0, 190), "", 34, Color(1, 0.9, 0.6))
	_hud["end_title"].size = Vector2(960, 50)
	_hud["end_title"].horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_hud["end_text"] = label(shade, Vector2(130, 250), "", 15)
	_hud["end_text"].size = Vector2(700, 140)
	_hud["end_text"].horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_hud["end_text"].autowrap_mode = TextServer.AUTOWRAP_WORD

func _update_hud() -> void:
	for i in heroes.size():
		var h := heroes[i]
		var p: Dictionary = _hud["panels"][i]
		p["bar"].max_value = h.max_hp
		p["bar"].value = h.hp
		p["panel"].color = Color(0.25, 0.3, 0.55, 0.9) if h.is_mine() else Color(0.1, 0.1, 0.16, 0.75)
		var who := ""
		if h.is_mine():
			who = "  · you" if _my_heroes().size() == 1 else "  · " + Session.dev_name(h.seat()["dev"])
		elif h.is_player():
			who = "  · online"
		p["name"].text = h.display_name + who + ("  (down)" if h.down else "")
	_hud["level"].text = "Level %d" % level
	_hud["xp"].max_value = _xp_need()
	_hud["xp"].value = xp
	_hud["embers"].text = "Soul embers: %d" % embers
	var boss_up := _boss != null and is_instance_valid(_boss) and not _boss.dead
	_hud["boss"].visible = boss_up
	_hud["boss_name"].visible = boss_up
	if boss_up:
		_hud["boss"].max_value = _boss.max_hp
		_hud["boss"].value = _boss.hp

# ---------------------------------------------------------------- the frame

func _my_heroes() -> Array[Hero]:
	var mine: Array[Hero] = []
	for h in heroes:
		if h.is_mine():
			mine.append(h)
	return mine

func _process(delta: float) -> void:
	_poll()
	_clock += delta
	if not started:
		_net_test_lobby(delta)
		return
	if over and is_host:
		for d: Dictionary in pads:
			if d["restart_just"]:
				if networked:
					restart.rpc()
				restart()
				return
	if pads[0]["back_just"] and over:
		leave()
		return
	if _toast_t > 0.0:
		_toast_t -= delta
		_hud["toast"].modulate.a = clampf(_toast_t, 0.0, 1.0)
	for pair: Array in _tracked.duplicate():
		if is_instance_valid(pair[0]) and not (pair[0] is Enemy and pair[0].dead):
			pair[1].position = pair[0].global_position + pair[2]
		else:
			pair[1].queue_free()
			_tracked.erase(pair)
	# the camera stays on this machine's players
	var mine := _my_heroes()
	var focus := Vector2.ZERO
	var n := 0
	for h in mine:
		if not h.down or mine.size() == 1:
			focus += h.global_position
			n += 1
	if n == 0:
		for h in heroes:
			if not h.down:
				focus += h.global_position
				n += 1
	if n > 0:
		_camera.position = focus / n + Vector2(0, -30)
	if cut:
		_cut_frame(delta)
	elif not over:
		for h in mine:
			var pad: Dictionary = pads[h.seat()["dev"]]
			if pad["next_just"] or pad["prev_just"]:
				to_host("req_switch", [h.idx, 1 if pad["next_just"] else -1])
		if is_host:
			_host_frame(delta)
	_update_hud()
	_playtest_frame(delta)

func _host_frame(delta: float) -> void:
	if _intro_t > 0.0:
		_intro_t -= delta
		if _intro_t <= 0.0:
			play_cutscene(Cutscenes.intro(_party_centre()))
		return
	if not _zone_active and _zone < ZONES.size():
		for h in heroes:
			if not h.down and h.is_player() and h.global_position.x > ZONES[_zone]["start"] + 160.0:
				_start_zone()
				break
	if _end_t > 0.0:
		_end_t -= delta
		if _end_t <= 0.0:
			play_cutscene(Cutscenes.ending(_party_centre()), func() -> void: emit_fx("finish", [true, level, embers, _clock]))
	if networked:
		_snap_t -= delta
		if _snap_t <= 0.0:
			_snap_t = 0.05
			snapshot.rpc(_pack())

## Players sharing a screen can't walk off it.
func keep_on_screen(p: Vector2) -> Vector2:
	if _my_heroes().size() < 2:
		return p
	var c := _camera.get_screen_center_position()
	return Vector2(clampf(p.x, c.x - 450.0, c.x + 450.0), clampf(p.y, c.y - 200.0, c.y + 250.0))

# ---------------------------------------------------------------- keeping machines in step

func _pack() -> Array:
	var hs: Array = []
	for h in heroes:
		hs.append([h.net_pos if not h.has_control() else h.global_position, h.facing, h.hp, h.max_hp,
			(1 if h.net_moving else 0) | (2 if h.down else 0) | (4 if h.stun > 0.0 else 0)])
	var es: Array = []
	for e in enemies:
		if not e.dead:
			es.append([e.id, Enemy.KINDS.find(e.kind), e.global_position, e.facing, e.hp,
				(1 if e.net_moving else 0) | (2 if e.stun > 0.0 else 0) | (4 if e.shaking else 0)])
	return [_clock, level, xp, embers, _zone, _zone_active, _boss.id if _boss != null and is_instance_valid(_boss) and not _boss.dead else 0, hs, es]

@rpc("authority", "call_remote", "unreliable_ordered")
func snapshot(s: Array) -> void:
	if not started or heroes.is_empty():
		return
	_clock = s[0]
	if s[1] != level:
		level = s[1]
	xp = s[2]
	embers = s[3]
	_zone = s[4]
	_zone_active = s[5]
	for i in heroes.size():
		var h := heroes[i]
		var d: Array = s[7][i]
		h.hp = d[2]
		h.max_hp = d[3]
		h.set_down(d[4] & 2 != 0)
		if not h.has_control():
			h.net_pos = d[0]
			h.facing = d[1]
			h.net_moving = d[4] & 1 != 0
			h.show_stun(d[4] & 4 != 0)
		elif h.down and not h.is_mine():
			h.global_position = d[0]
	var seen := {}
	for d: Array in s[8]:
		seen[d[0]] = true
		var e: Enemy = _by_id.get(d[0])
		if e == null:
			e = _make_enemy(Enemy.KINDS[d[1]], d[2], d[0], true)
		e.net_pos = d[2]
		e.facing = d[3]
		if d[4] < e.hp:
			e._flash = 0.09
		e.hp = d[4]
		e.net_moving = d[5] & 1 != 0
		e.shaking = d[5] & 4 != 0
		if e.kind != "sac":
			e.show_stun(d[5] & 2 != 0)
	for id: int in _by_id.keys():
		if not seen.has(id):
			var gone: Enemy = _by_id[id]
			_by_id.erase(id)
			enemies.erase(gone)
			if is_instance_valid(gone) and not gone.dead:
				gone.queue_free()
	_boss = _by_id.get(s[6])

@rpc("any_peer", "call_remote", "unreliable_ordered")
func hero_input(idx: int, pos: Vector2, facing: Vector2, moving: bool) -> void:
	if not is_host or idx < 0 or idx >= heroes.size() or Session.seats[idx]["peer"] != _sender():
		return
	var h := heroes[idx]
	h.net_pos = pos
	h.facing = facing
	h.net_moving = moving

@rpc("any_peer", "call_remote", "reliable")
func req_attack(idx: int, facing: Vector2) -> void:
	if not is_host or idx < 0 or idx >= heroes.size() or Session.seats[idx]["peer"] != _sender() and Session.seats[idx]["peer"] != 0:
		return
	heroes[idx].facing = facing.normalized() if facing.length() > 0.1 else heroes[idx].facing
	heroes[idx].host_attack()

## A player takes over a computer ally; the computer takes their old hero.
@rpc("any_peer", "call_remote", "reliable")
func req_switch(idx: int, step: int) -> void:
	if not is_host or idx < 0 or idx >= heroes.size() or Session.seats[idx]["peer"] != _sender():
		return
	_swap_to_ally(idx, step)

func _swap_to_ally(idx: int, step: int) -> bool:
	var n := heroes.size()
	for k in range(1, n):
		var j := (idx + step * k + n * 2) % n
		if Session.seats[j]["peer"] == 0 and not heroes[j].down:
			Session.seats[j] = Session.seats[idx]
			Session.seats[idx] = {"peer": 0, "dev": -1}
			_share_seats()
			float_text(heroes[j].global_position + Vector2(0, -90), heroes[j].display_name, Color(0.8, 0.9, 1.0))
			return true
	return false

@rpc("authority", "call_remote", "reliable")
func hero_hit(idx: int, k: Vector2, stun_time: float) -> void:
	heroes[idx].knock = k
	if stun_time > 0.0:
		heroes[idx].stun = stun_time

## Something everyone should see. The host does it, and tells the others to do the same.
func emit_fx(kind: String, args: Array) -> void:
	_do_fx(kind, args)
	if networked and is_host:
		fx_rpc.rpc(kind, args)

@rpc("authority", "call_remote", "reliable")
func fx_rpc(kind: String, args: Array) -> void:
	if started:
		_do_fx(kind, args)

func _do_fx(kind: String, a: Array) -> void:
	match kind:
		"float":
			var l := label(_fx, a[0] + Vector2(randf_range(-8, 8) - 10, 0), a[1], 13, a[2])
			var t := create_tween()
			t.tween_property(l, "position:y", l.position.y - 28.0, 0.6)
			t.parallel().tween_property(l, "modulate:a", 0.0, 0.6)
			t.tween_callback(l.queue_free)
		"toast":
			_hud["toast"].text = a[0]
			_hud["toast"].modulate.a = 1.0
			_toast_t = a[1]
		"goal":
			_hud["goal"].text = a[0]
		"slash":
			var poly := Polygon2D.new()
			if a[4]:
				poly.polygon = PackedVector2Array([Vector2(-a[2] * 0.6, -3), Vector2(a[2] * 0.5, 0), Vector2(-a[2] * 0.6, 3)])
			else:
				poly.polygon = PackedVector2Array([Vector2(-8, -16), Vector2(14, 0), Vector2(-8, 16), Vector2(2, 0)])
			poly.color = a[3]
			poly.position = a[0]
			poly.rotation = a[1].angle()
			_fx.add_child(poly)
			var t2 := create_tween()
			t2.tween_property(poly, "modulate:a", 0.0, 0.16)
			t2.tween_callback(poly.queue_free)
		"tele":
			var lane := Polygon2D.new()
			lane.polygon = PackedVector2Array([Vector2(0, -44), Vector2(a[2], -44), Vector2(a[2], 44), Vector2(0, 44)])
			lane.color = Color(1, 0.2, 0.15, 0.3)
			lane.position = a[0]
			lane.rotation = a[1].angle()
			_ground_fx.add_child(lane)
			var t3 := create_tween()
			t3.tween_property(lane, "modulate:a", 0.0, 1.5)
			t3.tween_callback(lane.queue_free)
		"proj":
			var p := Projectile.new()
			p.game = self
			p.position = a[0]
			p.dir = a[1].normalized()
			p.team = a[2]
			p.dmg = a[3]
			p.kind = a[4]
			_fx.add_child(p)
		"drop":
			var pk := Pickup.new()
			pk.game = self
			pk.id = a[0]
			pk.kind = a[1]
			pk.position = a[2]
			pk.vel = a[3]
			_pickups[pk.id] = pk
			_fx.add_child(pk)
		"pick":
			var got: Pickup = _pickups.get(a[0])
			_pickups.erase(a[0])
			if got != null and is_instance_valid(got):
				got.queue_free()
		"gate":
			var gate: StaticBody2D = _gates[a[0]]
			if gate != null and is_instance_valid(gate):
				gate.collision_layer = 0
				var t4 := create_tween()
				t4.tween_property(gate, "modulate:a", 0.0, 0.8)
				t4.tween_callback(gate.queue_free)
		"die":
			var e: Enemy = _by_id.get(a[0])
			if e != null and e.puppet:
				_by_id.erase(a[0])
				enemies.erase(e)
				e.fade_out()
		"lunge_h":
			heroes[a[0]].lunge(a[1], a[2])
		"lunge_e":
			var b: Enemy = _by_id.get(a[0])
			if b != null and is_instance_valid(b):
				if b.kind == "sac":
					b.squash()
				else:
					b.lunge(a[1], a[2])
					b.play_anim(false, "attack")
		"cut_on":
			cut = true
			_hud["cut"].visible = true
			_hud["play"].visible = false
		"cut_off":
			cut = false
			_cut_cam = null
			_hud["cut"].visible = false
			_hud["play"].visible = true
		"cut_step":
			var st: Dictionary = a[0]
			if st.has("cam"):
				_cut_cam = st["cam"]
			var has_text: bool = st.has("text")
			_hud["cut_who"].text = st.get("who", "")
			_hud["cut_text"].text = st.get("text", "")
			_hud["cut_text"].visible_characters = 0
			_hud["cut_hint"].visible = has_text
			_cut_chars = 0.0
			var face_path := "res://assets/chars/%s/idle_south/0.png" % str(st.get("who", "")).to_lower()
			_hud["cut_face"].texture = load(face_path) if has_text and ResourceLoader.exists(face_path) else null
		"finish":
			over = true
			_hud["shade"].visible = true
			var again := "Press R to play again" if is_host else "Waiting for the host to restart"
			if a[0]:
				_hud["end_title"].text = "The Lantern Woods are clear"
				_hud["end_text"].text = "Through the trees, a light: Omega Palace.\n\nLevel %d  ·  %d soul embers  ·  %d:%02d\n\n%s  ·  Esc: main menu" % [a[1], a[2], int(a[3]) / 60, int(a[3]) % 60, again]
			else:
				_hud["end_title"].text = "The woods take you"
				_hud["end_text"].text = "Everyone is down.\n\n%s  ·  Esc: main menu" % again

func float_text(pos: Vector2, text: String, colour: Color) -> void:
	emit_fx("float", [pos, text, colour])

func toast(text: String, seconds := 3.0) -> void:
	emit_fx("toast", [text, seconds])

# ---------------------------------------------------------------- cutscenes

func _party_centre() -> Vector2:
	var c := Vector2.ZERO
	for h in heroes:
		c += h.global_position
	return c / maxf(1.0, heroes.size())

## Host: freeze the fight and play a scripted scene on every machine, then call `done`.
func play_cutscene(steps: Array, done := Callable()) -> void:
	_cut_steps = []
	for st: Dictionary in steps:
		if st.has("needs") and not Session.party.has(st["needs"]):
			continue
		if st.has("unless") and Session.party.has(st["unless"]):
			continue
		_cut_steps.append(st)
	_cut_i = -1
	_cut_done = done
	emit_fx("cut_on", [])
	_cut_advance()

func _cut_advance() -> void:
	_cut_i += 1
	if _cut_i >= _cut_steps.size():
		emit_fx("cut_off", [])
		var done := _cut_done
		_cut_done = Callable()
		if done.is_valid():
			done.call()
		return
	var st: Dictionary = _cut_steps[_cut_i]
	_cut_wait = st.get("wait", -1.0) if not st.has("text") else (1.2 if autopilot else -1.0)
	emit_fx("cut_step", [st])

## Any player can move the scene on, or skip it.
@rpc("any_peer", "call_remote", "reliable")
func req_advance(skip: bool) -> void:
	if not is_host or not cut:
		return
	if skip:
		_cut_i = _cut_steps.size()
	_cut_advance()

func _cut_frame(delta: float) -> void:
	if _cut_cam != null:
		_camera.position = _cut_cam
	var text_l: Label = _hud["cut_text"]
	var total := text_l.text.length()
	_cut_chars += delta * 45.0
	text_l.visible_characters = int(_cut_chars) if _cut_chars < total else -1
	for d: Dictionary in pads:
		if d["back_just"]:
			to_host("req_advance", [true])
			return
		if d["attack_just"] and total > 0:
			if _cut_chars < total:
				_cut_chars = total       # first press shows the whole line
			else:
				to_host("req_advance", [false])
			return
	if is_host and _cut_wait > 0.0:
		_cut_wait -= delta
		if _cut_wait <= 0.0:
			_cut_advance()
	if is_host and networked:
		_snap_t -= delta
		if _snap_t <= 0.0:
			_snap_t = 0.05
			snapshot.rpc(_pack())

# ---------------------------------------------------------------- the host's game

func _start_zone() -> void:
	_zone_active = true
	if autopilot:
		print("zone %d starts at %.0fs" % [_zone, _clock])
	var z: Dictionary = ZONES[_zone]
	toast(z["line"], 5.0)
	emit_fx("goal", [z["goal"]])
	var x0: float = z["start"] + 420.0
	var x1: float = (z["gate"] if z["gate"] > 0 else FIELD_W - 60.0) - 120.0
	var sac_i := 0
	for kind: String in z["spawn"]:
		var count := int(z["spawn"][kind])
		if kind != "boss" and Session.party.size() < 4:
			count = int(ceil(count * 0.72))      # a party of three meets fewer of them
		for i in count:
			var pos := Vector2(randf_range(x0, x1), randf_range(TOP + 60, BOT - 60))
			if kind == "boss":
				pos = Vector2((x0 + x1) / 2.0 + 150.0, (TOP + BOT) / 2.0)
			var e := spawn_enemy(kind, pos)
			if kind == "sac":
				e.hatch_in = 5.0 + sac_i * 3.5
				sac_i += 1
			if kind == "boss":
				_boss = e
				play_cutscene(Cutscenes.boss(e.position + Vector2(0, -40), _party_centre()))

func _zone_cleared() -> void:
	_zone_active = false
	if autopilot:
		print("zone %d cleared at %.0fs, heroes %s" % [_zone, _clock, _hero_report()])
	var z: Dictionary = ZONES[_zone]
	for h in heroes:
		if h.down:
			h.revive()
		else:
			h.hp = minf(h.max_hp, h.hp + h.max_hp * 0.35)     # a breather between fights
	if z["gate"] < 0:
		_end_t = 2.2
		_zone += 1
		return
	emit_fx("gate", [_zone])
	toast("The webs give way. Press on.", 3.0)
	emit_fx("goal", ["Head east through the woods"])
	_zone += 1

func _hero_report() -> Array:
	return heroes.map(func(h: Hero) -> String: return "%s:%d%s@%d" % [h.kind, int(h.hp), "(down)" if h.down else "", int(h.global_position.x)])

func hero_down(h: Hero) -> void:
	if autopilot:
		print("%s down at %.0fs" % [h.kind, _clock])
	toast("%s is down! Clear the area to get them back up." % h.display_name, 3.0)
	for other in heroes:
		if not other.down:
			if h.is_player():
				_swap_to_ally(h.idx, 1)      # their player carries on as a computer ally, if one is standing
			return
	emit_fx("finish", [false, level, embers, _clock])

## Who a computer ally follows: the nearest standing player.
func leader_for(me: Hero) -> Hero:
	var best: Hero = null
	var best_d := INF
	for h in heroes:
		if h == me or h.down or not h.is_player():
			continue
		var d := h.global_position.distance_to(me.global_position)
		if d < best_d:
			best_d = d
			best = h
	if best == null:
		for h in heroes:
			if h != me and not h.down:
				return h
	return best

func nearest_enemy(pos: Vector2, max_range: float, prefer := Vector2.ZERO) -> Enemy:
	var best: Enemy = null
	var best_d := max_range
	var best_any: Enemy = null
	var best_any_d := max_range
	for e in enemies:
		if e.dead:
			continue
		var off := e.global_position - pos
		var d := off.length()
		if d < best_any_d:
			best_any_d = d
			best_any = e
		if prefer != Vector2.ZERO and off.normalized().dot(prefer) > 0.3 and d < best_d:
			best_d = d
			best = e
	return best if best != null else best_any

func objective_point(me: Hero) -> Vector2:
	if _zone_active:
		var e := nearest_enemy(me.global_position, 99999.0)
		return e.global_position if e != null else me.global_position
	if _zone < ZONES.size():
		return Vector2(ZONES[_zone]["start"] + 300.0, (TOP + BOT) / 2.0 + (me.idx - 1.5) * 50.0)
	return Vector2(FIELD_W - 200.0, (TOP + BOT) / 2.0)

## Where the boss is about to charge: [origin, direction], or empty.
func charge_lane() -> Array:
	if _boss != null and is_instance_valid(_boss) and not _boss.dead and not _boss.puppet and (_boss.state == "wind_charge" or _boss.state == "charge"):
		return [_boss.global_position, _boss.charge_dir]
	return []

func in_bounds(p: Vector2) -> bool:
	return p.x > 0 and p.x < FIELD_W and p.y > TOP - 60 and p.y < BOT + 20

func _make_enemy(kind: String, pos: Vector2, id: int, puppet: bool) -> Enemy:
	var e := Enemy.new()
	_world.add_child(e)
	e.setup(self, kind, id, puppet)
	e.position = pos
	e.net_pos = pos
	enemies.append(e)
	_by_id[id] = e
	return e

func spawn_enemy(kind: String, pos: Vector2) -> Enemy:
	_next_id += 1
	return _make_enemy(kind, Vector2(clampf(pos.x, 80, FIELD_W - 80), clampf(pos.y, TOP + 30, BOT - 20)), _next_id, false)

func enemy_gone(e: Enemy, killed: bool) -> void:
	enemies.erase(e)
	_by_id.erase(e.id)
	if killed:
		emit_fx("die", [e.id])
		_gain_xp(e.xp)
		for i in e.embers:
			_drop("ember", e.global_position)
		if randf() < (1.0 if e.kind == "boss" else 0.18):
			for i in (4 if e.kind == "boss" else 1):
				_drop("heart", e.global_position)
	if _zone_active and enemies.is_empty():
		_zone_cleared()

func _drop(kind: String, pos: Vector2) -> void:
	_next_pick += 1
	emit_fx("drop", [_next_pick, kind, pos + Vector2(0, -10), Vector2.from_angle(randf() * TAU) * randf_range(60, 140)])

func collect(p: Pickup, h: Hero) -> void:
	if not _pickups.has(p.id):
		return
	if p.kind == "ember":
		embers += 1
	else:
		var weakest := h
		for other in heroes:
			if not other.down and other.hp / other.max_hp < weakest.hp / weakest.max_hp:
				weakest = other
		weakest.hp = minf(weakest.max_hp, weakest.hp + weakest.max_hp * 0.3)
		float_text(weakest.global_position + Vector2(0, -80), "+", Color(0.5, 1, 0.6))
	emit_fx("pick", [p.id])

func _xp_need() -> int:
	return 60 * level

func _gain_xp(n: int) -> void:
	xp += n
	while xp >= _xp_need():
		xp -= _xp_need()
		level += 1
		for h in heroes:
			h.apply_level(true)
		toast("Level %d! The party grows stronger." % level, 2.5)

## A light on the ground canvas. With a target it follows that node and is freed with it.
func add_light(target: Node2D, colour: Color, tex_scale: float, energy: float, offset := Vector2.ZERO) -> void:
	var l := PointLight2D.new()
	l.texture = light_tex
	l.texture_scale = tex_scale
	l.energy = energy
	l.color = colour
	l.position = offset
	_lights.add_child(l)
	if target != null:
		_tracked.append([target, l, offset])

# ---------------------------------------------------------------- automated playtests

func _net_test_lobby(delta: float) -> void:
	if _net_test == "host" and Session.humans() >= 2:
		_test_t += delta
		if _test_t > 1.0:
			start_from_lobby()

func _playtest_frame(delta: float) -> void:
	if _shots_dir != "":
		_shot_t -= delta
		if _shot_t <= 0.0:
			_shot_t = 5.0
			_save_shot()
	if _shots_dir == "" and _net_test == "":
		return
	_log_t -= delta
	if _net_test != "" and _log_t <= 0.0:
		_log_t = 10.0
		print("STATE t=%.0f zone=%d level=%d embers=%d enemies=%d heroes=%s" % [_clock, _zone, level, embers, enemies.size(), _hero_report()])
	if over:
		_test_t += delta
	if (over and _test_t > 2.5) or _clock > 200.0:
		if _shots_dir != "":
			_save_shot()
		print("RESULT over=%s zone=%d level=%d embers=%d clock=%.0f heroes=%s" % [over, _zone, level, embers, _clock, _hero_report()])
		get_tree().quit()

func _save_shot() -> void:
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png("%s/shot_%02d.png" % [_shots_dir, _shot_n])
	_shot_n += 1
