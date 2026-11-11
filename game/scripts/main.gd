class_name Main
extends Node2D
## Omega Island: the Lantern Woods, for one to four players on one screen, online, or both.
## One machine is the host: it runs the enemies, damage and progress, and tells the others what happened.
## Every machine moves its own players' heroes and tells the host where they are.

const PORT := 24565
# The world is measured in screen pixels at 640 x 360. The walkable wood runs east between TOP and BOT.
const FIELD_W := 3904.0
const TOP := 128.0
const BOT := 448.0
const ZONES := [
	{"start": 512.0, "gate": 1344.0, "spawn": {"lantern": 7}, "goal": "Clear the Arachno-Lanterns",
		"who": "leo", "line": "Lanterns in the trees. Stay behind me, Emma."},
	{"start": 1344.0, "gate": 2176.0, "spawn": {"lantern": 7, "stalker": 3}, "goal": "Survive the Stalkers",
		"who": "emma", "line": "Stalkers hunt whoever is weakest. Keep together."},
	{"start": 2176.0, "gate": 3008.0, "spawn": {"lantern": 3, "sac": 6}, "goal": "Destroy the egg sacs",
		"who": "emma", "line": "Egg sacs! Break them before they hatch."},
	{"start": 3008.0, "gate": -1.0, "spawn": {"boss": 1}, "goal": "Defeat the Brood Lantern", "who": "", "line": ""},
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
var paused := false           # the menu is open in a game on this computer only
var frozen: bool:             # nothing moves: the game is over, a cutscene is playing, or it is paused
	get:
		return over or cut or paused
var pads: Array = []          # one entry per input device: 0 is the keyboard, 1 to 4 are controllers
var level_node: Level
var hud: Hud

var _lobby: Lobby
var _zone := 0
var _zone_active := false
var _boss: Enemy
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
var _cut_label: Label
var _bark_t := 0.0
# automated playtests
var _shots_dir := ""
var _shot_t := 0.0
var _shot_n := 0
var _net_test := ""
var _log_t := 0.0
var _test_t := 0.0
var _peek := Vector2.INF       # automated screenshots of one spot: --peek=x,y with --shots=<folder>

func _ready() -> void:
	randomize()
	for a: String in OS.get_cmdline_user_args():
		if a.begins_with("--shots="):
			_shots_dir = a.trim_prefix("--shots=")
			autopilot = true
		if a.begins_with("--net-test="):
			_net_test = a.trim_prefix("--net-test=")
			autopilot = true
		if a.begins_with("--peek="):
			var xy := a.trim_prefix("--peek=").split(",")
			_peek = Vector2(float(xy[0]), float(xy[1]))
		if a.begins_with("--fast="):       # automated playtests can run the clock faster
			Engine.time_scale = float(a.trim_prefix("--fast="))
			Engine.max_physics_steps_per_frame = 32
	_setup_input()
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
	level_node = Level.new()
	add_child(level_node)
	level_node.build(self)
	_build_party()
	hud = Hud.new()
	add_child(hud)
	hud.build(self)
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

# ---------------------------------------------------------------- the party

func _build_party() -> void:
	for i in Session.party.size():
		var h := Hero.new()
		level_node.world.add_child(h)
		h.setup(self, i)
		h.position = Vector2(372 - i * 30, level_node.mid + (i - (Session.party.size() - 1) / 2.0) * 30.0)
		h.net_pos = h.position
		h.facing = Vector2.RIGHT
		heroes.append(h)

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
	if not over and not cut:
		for d: Dictionary in pads:
			if d["back_just"]:
				set_menu(not hud.menu_open())
	level_node.tick(delta)
	if _bark_t > 0.0:
		_bark_t -= delta
		if _bark_t <= 0.0 and not cut:
			level_node.hush()
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
		level_node.camera.position = focus / n + Vector2(0, -16)
	if cut:
		_cut_frame(delta)
	elif not over and not paused:
		for h in mine:
			var pad: Dictionary = pads[h.seat()["dev"]]
			if pad["next_just"] or pad["prev_just"]:
				to_host("req_switch", [h.idx, 1 if pad["next_just"] else -1])
		if is_host:
			_host_frame(delta)
	hud.tick(delta)
	_playtest_frame(delta)

func _host_frame(delta: float) -> void:
	if _intro_t > 0.0:
		_intro_t -= delta
		if _intro_t <= 0.0:
			play_cutscene(Cutscenes.intro(_party_centre()), func() -> void: emit_fx("card", ["The Lantern Woods", "Omega Island"]))
		return
	if not _zone_active and _zone < ZONES.size():
		for h in heroes:
			if not h.down and h.is_player() and h.global_position.x > ZONES[_zone]["start"] + 110.0:
				_start_zone()
				break
	if _end_t > 0.0:
		_end_t -= delta
		if _end_t <= 0.0:
			play_cutscene(Cutscenes.ending(_party_centre(), level_node.palace), func() -> void: emit_fx("finish", [true, level, embers, _clock]))
	if networked:
		_snap_t -= delta
		if _snap_t <= 0.0:
			_snap_t = 0.05
			snapshot.rpc(_pack())

## Players sharing a screen can't walk off it.
func keep_on_screen(p: Vector2) -> Vector2:
	if _my_heroes().size() < 2:
		return p
	var c := level_node.camera.get_screen_center_position()
	return Vector2(clampf(p.x, c.x - 300.0, c.x + 300.0), clampf(p.y, c.y - 130.0, c.y + 164.0))

## The menu over the game. On one computer it also stops the clock; online, the game carries on behind it.
func set_menu(on: bool) -> void:
	hud.show_menu(on)
	paused = on and not networked

func boss() -> Enemy:
	return _boss if _boss != null and is_instance_valid(_boss) and not _boss.dead else null

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
			float_text(heroes[j].global_position + Vector2(0, -56), heroes[j].display_name, Color(0.8, 0.9, 1.0))
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
			level_node.float_text(a[0], a[1], a[2])
			if a[3] > 0:
				level_node.burst(a[0] + Vector2(0, 10), Color(1, 1, 0.85) if a[3] == 1 else Color(1, 0.45, 0.4), 6, 46.0, 0.3)
				if a[3] == 2:
					level_node.shake(2.0)
					for h in heroes:       # the screen's edge flashes red when it was one of this machine's players
						if h.is_mine() and h.global_position.distance_to(a[0]) < 60.0:
							hud.hurt()
		"toast":
			hud.toast(a[0], a[1])
		"goal":
			hud.set_goal(a[0])
		"card":
			hud.card(a[0], a[1])
		"bark":
			# a line spoken during play, over the speaker's head; a plain message if they aren't here
			var idx := Session.party.find(a[0])
			if idx >= 0 and not heroes[idx].down:
				hud.card_hide()
				level_node.say(heroes[idx], heroes[idx].display_name, a[1]).visible_characters = -1
				_bark_t = a[2]
			else:
				hud.toast(a[1], a[2])
		"slash":
			level_node.slash(a[0], a[1], a[2], a[3], a[4])
		"tele":
			level_node.lane(a[0], a[1], a[2], a[3])
		"shake":
			level_node.shake(a[0])
		"proj":
			var p := Projectile.new()
			p.game = self
			p.position = a[0]
			p.dir = a[1].normalized()
			p.team = a[2]
			p.dmg = a[3]
			p.kind = a[4]
			level_node.fx.add_child(p)
		"drop":
			var pk := Pickup.new()
			pk.game = self
			pk.id = a[0]
			pk.kind = a[1]
			pk.position = a[2]
			pk.vel = a[3]
			_pickups[pk.id] = pk
			level_node.fx.add_child(pk)
		"pick":
			var got: Pickup = _pickups.get(a[0])
			_pickups.erase(a[0])
			if got != null and is_instance_valid(got):
				level_node.burst(got.global_position, Color(0.6, 0.9, 1.0) if got.kind == "ember" else Color(1, 0.4, 0.5), 4, 30.0, 0.3)
				got.queue_free()
		"gate":
			level_node.open_gate(a[0])
		"die":
			var big: bool = a[2] == "boss"
			level_node.burst(a[1] + Vector2(0, -10), Color(1.0, 0.6, 0.2), 40 if big else 12, 120.0 if big else 60.0, 1.0 if big else 0.5)
			if big:
				level_node.shake(7.0)
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
					if a[3]:
						b.play_anim(false, "attack")
		"cut_on":
			cut = true
			_bark_t = 0.0
			level_node.hush()
			hud.show_menu(false)
			paused = false
			hud.cut_on()
		"cut_off":
			cut = false
			_cut_cam = null
			_cut_label = null
			level_node.hush()
			for h in heroes:
				h.cut_anim = ""
				if h.cut_target != Vector2.INF:
					h.global_position = h.cut_target
				h.cut_target = Vector2.INF
				h.net_pos = h.global_position
			hud.cut_off()
		"cut_step":
			var st: Dictionary = a[0]
			if st.has("cam"):
				_cut_cam = st["cam"]
			for pair: Array in st.get("acts", []):
				heroes[pair[0]].cut_anim = pair[1]
				heroes[pair[0]].sprite.stop()
			for w: Array in st.get("walks", []):
				heroes[w[0]].cut_target = w[1]
			_cut_chars = 0.0
			_cut_label = null
			level_node.hush()
			if st.has("text"):
				# a hero in the party speaks from a bubble over their head; anyone else, and narration, from the box
				var who: String = st.get("who", "")
				var speaker := Session.party.find(who.to_lower())
				if speaker >= 0:
					_cut_label = level_node.say(heroes[speaker], who, st["text"])
				else:
					_cut_label = hud.narrate(who, st["text"])
				hud.cut_line(true, speaker < 0)
			else:
				hud.cut_line(false, false)
		"finish":
			over = true
			level_node.hush()
			hud.finish(a[0], a[1], a[2], a[3])

## A floating number or word. `spark` adds a hit flash: 1 for a blow on an enemy, 2 for one on a hero.
func float_text(pos: Vector2, text: String, colour: Color, spark := 0) -> void:
	emit_fx("float", [pos, text, colour, spark])

func add_light(target: Node2D, colour: Color, tex_scale: float, energy: float, offset := Vector2.ZERO) -> void:
	level_node.add_light(target, colour, tex_scale, energy, offset)

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
	for raw: Dictionary in steps:
		if raw.has("needs") and not Session.party.has(raw["needs"]):
			continue
		if raw.has("unless") and Session.party.has(raw["unless"]):
			continue
		# turn hero names into places in the party, and relative moves into spots on the map
		var st := raw.duplicate()
		var acts: Array = []
		for pair: Array in raw.get("acts", []):
			if Session.party.has(pair[0]):
				acts.append([Session.party.find(pair[0]), pair[1]])
		st["acts"] = acts
		var walks: Array = []
		for w: Array in raw.get("walks", []):       # [who, offset] or [who, offset, beside whom]
			if not Session.party.has(w[0]) or (w.size() > 2 and not Session.party.has(w[2])):
				continue
			var base: Hero = heroes[Session.party.find(w[2] if w.size() > 2 else w[0])]
			walks.append([Session.party.find(w[0]), base.global_position + w[1]])
		st["walks"] = walks
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
	_cut_wait = st.get("wait", -1.0) if not st.has("text") else (1.4 + str(st["text"]).length() / 45.0 if autopilot else -1.0)
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
		level_node.camera.position = _cut_cam
	var total := 0
	if _cut_label != null:
		total = _cut_label.text.length()
		_cut_chars += delta * 45.0
		_cut_label.visible_characters = int(_cut_chars) if _cut_chars < total else -1
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
	if z["line"] != "":
		emit_fx("bark", [z["who"], z["line"], 4.5])
	emit_fx("goal", [z["goal"]])
	var x0: float = z["start"] + 300.0
	var x1: float = (z["gate"] if z["gate"] > 0 else FIELD_W - 60.0) - 90.0
	var sac_i := 0
	for kind: String in z["spawn"]:
		var count := int(z["spawn"][kind])
		if kind != "boss" and Session.party.size() < 4:
			count = int(ceil(count * 0.72))      # a party of three meets fewer of them
		for i in count:
			var px := randf_range(x0, x1)
			var pos := Vector2(px, level_node.path_y(px) + randf_range(-80.0, 80.0))
			if kind == "sac":
				pos.y = level_node.path_y(px) + randf_range(-34.0, 34.0)
			if kind == "boss":
				pos = level_node.arena + Vector2(110.0, 0.0)
			var e := spawn_enemy(kind, pos)
			if kind == "sac":
				e.hatch_in = 5.0 + sac_i * 3.5
				sac_i += 1
			if kind == "boss":
				_boss = e
				play_cutscene(Cutscenes.boss(e.position + Vector2(0, -30), _party_centre()), func() -> void: emit_fx("card", ["The Brood Lantern", "Mother of the nest"]))

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
	emit_fx("shake", [2.0])
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
		var gx: float = ZONES[_zone]["start"] + 200.0
		return Vector2(gx, level_node.path_y(gx) + (me.idx - 1.0) * 26.0)
	return Vector2(FIELD_W - 260.0, level_node.mid)

## Where the boss is about to charge: [origin, direction], or empty.
func charge_lane() -> Array:
	if _boss != null and is_instance_valid(_boss) and not _boss.dead and not _boss.puppet and (_boss.state == "wind_charge" or _boss.state == "charge"):
		return [_boss.global_position, _boss.charge_dir]
	return []

func in_bounds(p: Vector2) -> bool:
	return p.x > 100 and p.x < FIELD_W - 90 and p.y > TOP - 40 and p.y < BOT + 14

func _make_enemy(kind: String, pos: Vector2, id: int, puppet: bool) -> Enemy:
	var e := Enemy.new()
	level_node.world.add_child(e)
	e.setup(self, kind, id, puppet)
	e.position = pos
	e.net_pos = pos
	# they rise out of the dark rather than popping in
	e.modulate = Color(0.2, 0.1, 0.3, 0.0)
	create_tween().tween_property(e, "modulate", Color.WHITE, 0.5)
	level_node.burst(pos + Vector2(0, -8), Color(0.6, 0.4, 0.9), 8, 40.0, 0.5)
	enemies.append(e)
	_by_id[id] = e
	return e

func spawn_enemy(kind: String, pos: Vector2) -> Enemy:
	_next_id += 1
	return _make_enemy(kind, Vector2(clampf(pos.x, 130, FIELD_W - 120), clampf(pos.y, TOP + 22, BOT - 14)), _next_id, false)

func enemy_gone(e: Enemy, killed: bool) -> void:
	enemies.erase(e)
	_by_id.erase(e.id)
	if killed:
		emit_fx("die", [e.id, e.global_position, e.kind])
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
	emit_fx("drop", [_next_pick, kind, pos + Vector2(0, -6), Vector2.from_angle(randf() * TAU) * randf_range(40, 100)])

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
		float_text(weakest.global_position + Vector2(0, -50), "+", Color(0.5, 1, 0.6))
	emit_fx("pick", [p.id])

func xp_need() -> int:
	return 60 * level

func _gain_xp(n: int) -> void:
	xp += n
	while xp >= xp_need():
		xp -= xp_need()
		level += 1
		for h in heroes:
			h.apply_level(true)

# ---------------------------------------------------------------- automated playtests

func _net_test_lobby(delta: float) -> void:
	if _net_test == "host" and Session.humans() >= 2:
		_test_t += delta
		if _test_t > 1.0:
			start_from_lobby()

func _playtest_frame(delta: float) -> void:
	if _peek != Vector2.INF:
		# look at one place, take a picture, and stop
		level_node.camera.position_smoothing_enabled = false
		level_node.camera.position = _peek
		paused = true
		_intro_t = -1.0
		_test_t += delta
		if _test_t > 1.5 and _shot_n == 0:
			_save_shot()
		if _test_t > 2.5:
			get_tree().quit()
		return
	if _shots_dir != "":
		_shot_t -= delta
		if _shot_t <= 0.0:
			_shot_t = 3.0
			_save_shot()
	if _shots_dir == "" and _net_test == "":
		return
	_log_t -= delta
	if _net_test != "" and _log_t <= 0.0:
		_log_t = 10.0
		print("STATE t=%.0f zone=%d level=%d embers=%d enemies=%d heroes=%s" % [_clock, _zone, level, embers, enemies.size(), _hero_report()])
	if over:
		_test_t += delta
	if (over and _test_t > 2.5) or _clock > 260.0:
		if _shots_dir != "":
			_save_shot()
		print("RESULT over=%s zone=%d level=%d embers=%d clock=%.0f heroes=%s" % [over, _zone, level, embers, _clock, _hero_report()])
		get_tree().quit()

func _save_shot() -> void:
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png("%s/shot_%02d.png" % [_shots_dir, _shot_n])
	_shot_n += 1
