extends Node2D
## Omega Island: the Lantern Woods. Builds the level, runs the zones, the party, the HUD and the win/lose flow.

const FIELD_W := 5400.0
const TOP := 170.0
const BOT := 830.0
const ZONES := [
	{"start": 600.0, "gate": 1700.0, "spawn": {"lantern": 6},
		"line": "Leo: \"Lanterns in the trees. Stay behind me, Emma.\"", "goal": "Clear the Arachno-Lanterns"},
	{"start": 1700.0, "gate": 2900.0, "spawn": {"lantern": 6, "stalker": 3},
		"line": "Emma: \"Stalkers hunt whoever is weakest. Keep together.\"", "goal": "Survive the Stalkers"},
	{"start": 2900.0, "gate": 4200.0, "spawn": {"lantern": 2, "sac": 5},
		"line": "Emma: \"Egg sacs! Break them before they hatch.\"", "goal": "Destroy the egg sacs"},
	{"start": 4200.0, "gate": -1.0, "spawn": {"boss": 1},
		"line": "The Brood Lantern wakes.", "goal": "Defeat the Brood Lantern"},
]

var heroes: Array[Hero] = []
var enemies: Array[Actor] = []
var level := 1
var xp := 0
var embers := 0
var over := false
var autopilot := false
var light_tex: GradientTexture2D

var _world: Node2D
var _fx: Node2D
var _ground_fx: Node2D
var _lights: Node2D
var _tracked: Array = []
var _camera: Camera2D
var _lead := 0
var _zone := 0
var _zone_active := false
var _gates: Array = []
var _boss: Enemy
var _hud := {}
var _toast_t := 0.0
var _shots_dir := ""
var _shot_t := 0.0
var _shot_n := 0
var _clock := 0.0
var _end_t := -1.0

func _ready() -> void:
	randomize()
	for a: String in OS.get_cmdline_user_args():
		if a.begins_with("--shots="):
			_shots_dir = a.trim_prefix("--shots=")
			autopilot = true
			seed(7)
	_setup_input()
	_build_light()
	_build_level()
	_build_party()
	_build_hud()
	toast("Omega Island. The wreck is behind you. Find a way through the woods.", 6.0)

# ---------------------------------------------------------------- setup

func _setup_input() -> void:
	var keys := {
		"move_left": [KEY_A, KEY_LEFT], "move_right": [KEY_D, KEY_RIGHT], "move_up": [KEY_W, KEY_UP], "move_down": [KEY_S, KEY_DOWN],
		"attack": [KEY_SPACE, KEY_J], "switch_next": [KEY_TAB, KEY_E], "switch_prev": [KEY_Q], "restart": [KEY_R],
	}
	for action: String in keys:
		if InputMap.has_action(action):
			continue
		InputMap.add_action(action)
		for k: int in keys[action]:
			var ev := InputEventKey.new()
			ev.physical_keycode = k
			InputMap.action_add_event(action, ev)
	var click := InputEventMouseButton.new()
	click.button_index = MOUSE_BUTTON_LEFT
	InputMap.action_add_event("attack", click)

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
	rng.seed = 2026
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
	var i := 0
	for kind: String in ["emma", "leo", "bender"]:
		var h := Hero.new()
		_world.add_child(h)
		h.setup(self, kind, i)
		h.position = Vector2(220 - i * 50, (TOP + BOT) / 2.0 + (i - 1) * 40)
		h.facing = Vector2.RIGHT
		heroes.append(h)
		i += 1
	_set_leader(0)

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

func _label(parent: Node, pos: Vector2, text: String, size := 14, colour := Color.WHITE) -> Label:
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
	_hud["panels"] = []
	for i in heroes.size():
		var h := heroes[i]
		var panel := ColorRect.new()
		panel.position = Vector2(10, 10 + i * 46)
		panel.size = Vector2(190, 40)
		layer.add_child(panel)
		var face := TextureRect.new()
		face.texture = load("res://assets/chars/%s/idle_south/0.png" % h.kind)
		face.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		face.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		face.position = Vector2(2, 2)
		face.size = Vector2(36, 36)
		panel.add_child(face)
		var name_l := _label(panel, Vector2(42, 0), h.display_name, 13)
		var bar := _bar(panel, Vector2(42, 22), Vector2(140, 12), Color(0.35, 0.85, 0.45))
		_hud["panels"].append({"panel": panel, "bar": bar, "name": name_l})
	_hud["level"] = _label(layer, Vector2(770, 8), "Level 1", 14, Color(1, 0.9, 0.5))
	_hud["xp"] = _bar(layer, Vector2(770, 31), Vector2(180, 7), Color(0.55, 0.5, 1.0))
	_hud["embers"] = _label(layer, Vector2(770, 44), "Soul embers: 0", 13, Color(0.7, 0.9, 1.0))
	_hud["goal"] = _label(layer, Vector2(230, 10), "Head east through the woods", 14, Color(1, 0.95, 0.8))
	_hud["goal"].size = Vector2(500, 20)
	_hud["goal"].horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_hud["toast"] = _label(layer, Vector2(130, 440), "", 15)
	_hud["toast"].size = Vector2(700, 50)
	_hud["toast"].horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_hud["toast"].autowrap_mode = TextServer.AUTOWRAP_WORD
	_hud["hint"] = _label(layer, Vector2(10, 516), "Move: WASD / arrows    Attack: Space or click    Switch hero: Tab or Q / E", 11, Color(0.8, 0.8, 0.9))
	_hud["boss_name"] = _label(layer, Vector2(280, 478), "The Brood Lantern", 14, Color(1, 0.7, 0.4))
	_hud["boss_name"].size = Vector2(400, 20)
	_hud["boss_name"].horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_hud["boss"] = _bar(layer, Vector2(280, 500), Vector2(400, 12), Color(0.95, 0.45, 0.15))
	_hud["boss"].visible = false
	_hud["boss_name"].visible = false
	var shade := ColorRect.new()
	shade.color = Color(0, 0, 0, 0.7)
	shade.size = Vector2(960, 540)
	shade.visible = false
	layer.add_child(shade)
	_hud["shade"] = shade
	_hud["end_title"] = _label(shade, Vector2(0, 190), "", 34, Color(1, 0.9, 0.6))
	_hud["end_title"].size = Vector2(960, 50)
	_hud["end_title"].horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_hud["end_text"] = _label(shade, Vector2(130, 250), "", 15)
	_hud["end_text"].size = Vector2(700, 120)
	_hud["end_text"].horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_hud["end_text"].autowrap_mode = TextServer.AUTOWRAP_WORD

func _update_hud() -> void:
	for i in heroes.size():
		var h := heroes[i]
		var p: Dictionary = _hud["panels"][i]
		p["bar"].max_value = h.max_hp
		p["bar"].value = h.hp
		p["panel"].color = Color(0.25, 0.3, 0.55, 0.9) if h.controlled else Color(0.1, 0.1, 0.16, 0.75)
		p["name"].text = h.display_name + ("  (down)" if h.down else "")
	_hud["level"].text = "Level %d" % level
	_hud["xp"].max_value = _xp_need()
	_hud["xp"].value = xp
	_hud["embers"].text = "Soul embers: %d" % embers
	if _boss != null and is_instance_valid(_boss):
		_hud["boss"].max_value = _boss.max_hp
		_hud["boss"].value = _boss.hp

# ---------------------------------------------------------------- game flow

func _process(delta: float) -> void:
	_clock += delta
	if Input.is_action_just_pressed("restart") and over:
		get_tree().reload_current_scene()
		return
	if _toast_t > 0.0:
		_toast_t -= delta
		_hud["toast"].modulate.a = clampf(_toast_t, 0.0, 1.0)
	for pair: Array in _tracked.duplicate():
		if is_instance_valid(pair[0]) and not (pair[0] is Actor and pair[0].dead and pair[0].team == 1):
			pair[1].position = pair[0].global_position + pair[2]
		else:
			pair[1].queue_free()
			_tracked.erase(pair)
	var lead := leader()
	if lead != null:
		_camera.position = lead.global_position + Vector2(0, -30)
	if not over:
		if Input.is_action_just_pressed("switch_next"):
			_switch(1)
		if Input.is_action_just_pressed("switch_prev"):
			_switch(-1)
		if lead != null and not _zone_active and _zone < ZONES.size() and lead.global_position.x > ZONES[_zone]["start"] + 160.0:
			_start_zone()
	if _end_t > 0.0:
		_end_t -= delta
		if _end_t <= 0.0:
			_finish(true)
	_update_hud()
	if _shots_dir != "":
		_shot_t -= delta
		if _shot_t <= 0.0:
			_shot_t = 5.0
			_save_shot()
		if (over and _shot_t < 3.0) or _clock > 170.0:
			_save_shot()
			print("RESULT over=%s zone=%d level=%d embers=%d clock=%.0f heroes=%s" % [over, _zone, level, embers, _clock,
				heroes.map(func(h: Hero) -> String: return "%s:%d" % [h.kind, int(h.hp)])])
			get_tree().quit()

func _save_shot() -> void:
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png("%s/shot_%02d.png" % [_shots_dir, _shot_n])
	_shot_n += 1

func _start_zone() -> void:
	_zone_active = true
	if autopilot:
		print("zone %d starts at %.0fs" % [_zone, _clock])
	var z: Dictionary = ZONES[_zone]
	toast(z["line"], 5.0)
	_hud["goal"].text = z["goal"]
	var x0: float = z["start"] + 420.0
	var x1: float = (z["gate"] if z["gate"] > 0 else FIELD_W - 60.0) - 120.0
	var sac_i := 0
	for kind: String in z["spawn"]:
		for i in int(z["spawn"][kind]):
			var pos := Vector2(randf_range(x0, x1), randf_range(TOP + 60, BOT - 60))
			if kind == "boss":
				pos = Vector2((x0 + x1) / 2.0 + 150.0, (TOP + BOT) / 2.0)
			var e := spawn_enemy(kind, pos)
			if kind == "sac":
				e.hatch_in = 5.0 + sac_i * 3.5
				sac_i += 1
			if kind == "boss":
				_boss = e
				_hud["boss"].visible = true
				_hud["boss_name"].visible = true

func _zone_cleared() -> void:
	_zone_active = false
	if autopilot:
		print("zone %d cleared at %.0fs, heroes %s" % [_zone, _clock, heroes.map(func(h: Hero) -> String: return "%s:%d%s" % [h.kind, int(h.hp), "(down)" if h.down else ""])])
	var z: Dictionary = ZONES[_zone]
	for h in heroes:
		if h.down:
			h.revive()
		else:
			h.hp = minf(h.max_hp, h.hp + h.max_hp * 0.35)     # a breather between fights
	if z["gate"] < 0:
		_hud["boss"].visible = false
		_hud["boss_name"].visible = false
		toast("The nest falls silent.", 3.0)
		_end_t = 2.2
		_zone += 1
		return
	var gate: StaticBody2D = _gates[_zone]
	gate.collision_layer = 0
	var t := create_tween()
	t.tween_property(gate, "modulate:a", 0.0, 0.8)
	t.tween_callback(gate.queue_free)
	toast("The webs give way. Press on.", 3.0)
	_hud["goal"].text = "Head east through the woods"
	_zone += 1

func _finish(won: bool) -> void:
	over = true
	_hud["shade"].visible = true
	if won:
		_hud["end_title"].text = "The Lantern Woods are clear"
		_hud["end_text"].text = "Through the trees, a light: Omega Palace.\n\nLevel %d  ·  %d soul embers  ·  %d:%02d\n\nPress R to play again" % [level, embers, int(_clock) / 60, int(_clock) % 60]
	else:
		_hud["end_title"].text = "The woods take you"
		_hud["end_text"].text = "All three of you are down.\n\nPress R to try again"

# ---------------------------------------------------------------- services used by actors

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

func leader() -> Hero:
	return heroes[_lead] if heroes.size() > 0 else null

func _set_leader(i: int) -> void:
	_lead = i
	var s := 1
	for j in heroes.size():
		heroes[j].controlled = j == i
		if j != i:
			heroes[j].slot = s
			s += 1

func _switch(step: int) -> void:
	for n in range(1, heroes.size() + 1):
		var j := (_lead + step * n + heroes.size() * 2) % heroes.size()
		if not heroes[j].down:
			_set_leader(j)
			float_text(heroes[j].global_position + Vector2(0, -90), heroes[j].display_name, Color(0.8, 0.9, 1.0))
			return

func hero_down(h: Hero) -> void:
	if autopilot:
		print("%s down at %.0fs" % [h.kind, _clock])
	toast("%s is down! Clear the area to get them back up." % h.display_name, 3.0)
	for other in heroes:
		if not other.down:
			if h.controlled:
				_switch(1)
			return
	_finish(false)

func nearest_enemy(pos: Vector2, max_range: float, prefer := Vector2.ZERO) -> Actor:
	var best: Actor = null
	var best_d := max_range
	var best_any: Actor = null
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

func objective_point() -> Vector2:
	var lead := leader()
	if _zone_active:
		var e := nearest_enemy(lead.global_position, 99999.0)
		return e.global_position if e != null else lead.global_position
	if _zone < ZONES.size():
		return Vector2(ZONES[_zone]["start"] + 300.0, (TOP + BOT) / 2.0)
	return Vector2(FIELD_W - 200.0, (TOP + BOT) / 2.0)

## Where the boss is about to charge: [origin, direction], or empty.
func charge_lane() -> Array:
	if _boss != null and is_instance_valid(_boss) and not _boss.dead and (_boss.state == "wind_charge" or _boss.state == "charge"):
		return [_boss.global_position, _boss.charge_dir]
	return []

func in_bounds(p: Vector2) -> bool:
	return p.x > 0 and p.x < FIELD_W and p.y > TOP - 60 and p.y < BOT + 20

func spawn_enemy(kind: String, pos: Vector2) -> Enemy:
	var e := Enemy.new()
	_world.add_child(e)
	e.setup(self, kind)
	e.position = Vector2(clampf(pos.x, 80, FIELD_W - 80), clampf(pos.y, TOP + 30, BOT - 20))
	enemies.append(e)
	return e

func enemy_gone(e: Enemy, killed: bool) -> void:
	enemies.erase(e)
	if killed:
		_gain_xp(e.xp)
		for i in e.embers:
			_drop("ember", e.global_position)
		if randf() < (1.0 if e.kind == "boss" else 0.18):
			for i in (4 if e.kind == "boss" else 1):
				_drop("heart", e.global_position)
	if _zone_active and enemies.is_empty():
		_zone_cleared()

func _drop(kind: String, pos: Vector2) -> void:
	var p := Pickup.new()
	p.game = self
	p.kind = kind
	p.position = pos + Vector2(0, -10)
	_fx.add_child(p)

func collect(p: Pickup, h: Hero) -> void:
	if p.kind == "ember":
		embers += 1
	else:
		var weakest := h
		for other in heroes:
			if not other.down and other.hp / other.max_hp < weakest.hp / weakest.max_hp:
				weakest = other
		weakest.hp = minf(weakest.max_hp, weakest.hp + weakest.max_hp * 0.3)
		float_text(weakest.global_position + Vector2(0, -80), "+", Color(0.5, 1, 0.6))

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

func spawn_projectile(pos: Vector2, dir: Vector2, team: int, dmg: float, kind: String) -> void:
	var p := Projectile.new()
	p.game = self
	p.dir = dir.normalized()
	p.team = team
	p.dmg = dmg
	p.kind = kind
	p.position = pos
	_fx.add_child(p)

func slash(pos: Vector2, dir: Vector2, reach: float, colour: Color, thrust: bool) -> void:
	var poly := Polygon2D.new()
	if thrust:
		poly.polygon = PackedVector2Array([Vector2(-reach * 0.6, -3), Vector2(reach * 0.5, 0), Vector2(-reach * 0.6, 3)])
	else:
		poly.polygon = PackedVector2Array([Vector2(-8, -16), Vector2(14, 0), Vector2(-8, 16), Vector2(2, 0)])
	poly.color = colour
	poly.position = pos
	poly.rotation = dir.angle()
	_fx.add_child(poly)
	var t := create_tween()
	t.tween_property(poly, "modulate:a", 0.0, 0.16)
	t.tween_callback(poly.queue_free)

func telegraph(pos: Vector2, dir: Vector2, length: float) -> void:
	var poly := Polygon2D.new()
	poly.polygon = PackedVector2Array([Vector2(0, -44), Vector2(length, -44), Vector2(length, 44), Vector2(0, 44)])
	poly.color = Color(1, 0.2, 0.15, 0.3)
	poly.position = pos
	poly.rotation = dir.angle()
	_ground_fx.add_child(poly)
	var t := create_tween()
	t.tween_property(poly, "modulate:a", 0.0, 1.5)
	t.tween_callback(poly.queue_free)

func float_text(pos: Vector2, text: String, colour: Color) -> void:
	var l := _label(_fx, pos + Vector2(randf_range(-8, 8) - 10, 0), text, 13, colour)
	var t := create_tween()
	t.tween_property(l, "position:y", l.position.y - 28.0, 0.6)
	t.parallel().tween_property(l, "modulate:a", 0.0, 0.6)
	t.tween_callback(l.queue_free)

func toast(text: String, seconds := 3.0) -> void:
	_hud["toast"].text = text
	_hud["toast"].modulate.a = 1.0
	_toast_t = seconds
