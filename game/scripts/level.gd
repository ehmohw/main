class_name Level
extends Node2D
## Builds the Lantern Woods: the beach and the wreck, the tiled ground and its path, trees, props, web gates,
## lights and weather. It also owns the passing effects: sparks, floating numbers, slashes, speech bubbles, screen shake.
## The layout comes from one fixed seed, so every machine in a game sees the same wood.

var game: Main
var ground: Ground
var world: Node2D          # everything sorted by depth: heroes, enemies, trees, props
var fx: Node2D             # above the world: projectiles, pickups, numbers, bubbles
var ground_fx: Node2D      # flat on the ground: webs, decals, warning lanes
var camera: Camera2D
var gates: Array = []      # one per zone: {"body", "parts"} or null
var mid := 0.0
var arena := Vector2.ZERO
var palace := Vector2.ZERO
var light_tex: GradientTexture2D

var _lights: Node2D
var _tracked: Array = []
var _flies: CPUParticles2D
var _fog: Sprite2D
var _shake := 0.0
var _rng := RandomNumberGenerator.new()
var _solids: Array[Vector2] = []
var _bubble: Node2D
var _bubble_panel: PanelContainer
var _bubble_who: Label
var _bubble_text: Label
var _bubble_on: Node2D

func build(game_: Main) -> void:
	game = game_
	_rng.seed = 2026
	light_tex = UI.glow()
	mid = (Main.TOP + Main.BOT) / 2.0
	arena = Vector2((Main.ZONES[3]["start"] + Main.FIELD_W) / 2.0 - 30.0, mid)
	palace = Vector2(Main.FIELD_W - 44.0, mid + 6.0)
	ground = Ground.new()
	ground.z_index = -10
	add_child(ground)
	ground.setup(Main.FIELD_W + 64.0, Main.BOT + 160.0, terrain_at)
	var dark := CanvasModulate.new()
	dark.color = Color(0.46, 0.44, 0.64)
	add_child(dark)
	ground_fx = Node2D.new()
	ground_fx.z_index = -5
	add_child(ground_fx)
	_lights = Node2D.new()
	add_child(_lights)
	# characters and scenery sit on their own layer with an even dusk tint, so the ground's lights never wash them out
	var world_layer := CanvasLayer.new()
	world_layer.layer = 1
	world_layer.follow_viewport_enabled = true
	add_child(world_layer)
	var dusk := CanvasModulate.new()
	dusk.color = Color(0.74, 0.74, 0.92)
	world_layer.add_child(dusk)
	world = Node2D.new()
	world.y_sort_enabled = true
	world_layer.add_child(world)
	var fx_layer := CanvasLayer.new()
	fx_layer.layer = 2
	fx_layer.follow_viewport_enabled = true
	add_child(fx_layer)
	fx = Node2D.new()
	fx_layer.add_child(fx)
	# the edges of the wood
	_wall(Rect2(-200, Main.TOP - 200, Main.FIELD_W + 400, 200))
	_wall(Rect2(-200, Main.BOT, Main.FIELD_W + 400, 200))
	_wall(Rect2(-100, Main.TOP, 214, Main.BOT - Main.TOP))
	_wall(Rect2(Main.FIELD_W - 96, Main.TOP, 200, Main.BOT - Main.TOP))
	_beach()
	_gates()
	_arena_and_palace()
	_trees()
	_scatter()
	_weather(fx_layer)
	_build_bubble()
	camera = Camera2D.new()
	camera.limit_left = 0
	camera.limit_right = int(Main.FIELD_W + 16)
	camera.limit_top = int(Main.TOP - 104)
	camera.limit_bottom = int(Main.BOT + 84)
	camera.position_smoothing_enabled = true
	camera.position_smoothing_speed = 6.0
	add_child(camera)
	camera.make_current()

# ---------------------------------------------------------------- the lie of the land

## The path's centre line as it winds east.
func path_y(x: float) -> float:
	return mid + 40.0 * sin(x / 230.0) + 18.0 * sin(x / 97.0 + 1.3)

func terrain_at(p: Vector2) -> int:
	var shore := 100.0 + 12.0 * sin(p.y / 61.0)
	if p.x < shore:
		return Ground.SEA
	var woods := 470.0 + 22.0 * sin(p.y / 83.0 + 0.7)
	var cove := p.x >= 200.0 and (p.y < Main.TOP - 20.0 + 10.0 * sin(p.x / 70.0) or p.y > Main.BOT + 26.0 + 10.0 * sin(p.x / 55.0))
	if p.x < woods and not cove:
		return Ground.SAND
	if p.y > Main.TOP + 10.0 and p.y < Main.BOT - 10.0:
		if ((p - arena) / Vector2(310.0, 150.0)).length() < 1.0:
			return Ground.PATH
		# the path fans out from nothing at the edge of the wood
		var reach := clampf((p.x - woods - 30.0) / 110.0, 0.0, 1.0) * 42.0
		if reach > 14.0 and absf(p.y - path_y(p.x)) < reach:
			return Ground.PATH
	return Ground.FOREST

func on_path(p: Vector2) -> bool:
	return ground.terrain(p) == Ground.PATH

func _near_gate(x: float, margin: float) -> bool:
	for z: Dictionary in Main.ZONES:
		if absf(x - z["gate"]) < margin or absf(x - z["start"]) < margin:
			return true
	return false

func _in_arena(p: Vector2, grow := 1.0) -> bool:
	return ((p - arena) / (Vector2(310.0, 150.0) * grow)).length() < 1.0

# ---------------------------------------------------------------- building blocks

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

## A prop standing on the ground at `pos` (its base), sorted by depth with the characters.
func prop(tex_name: String, pos: Vector2, solid := 0.0, flip := false) -> Sprite2D:
	var s := Sprite2D.new()
	s.texture = load("res://assets/props/%s.png" % tex_name)
	s.offset = Vector2(0, -s.texture.get_height() / 2.0 + 3)
	s.position = pos
	s.flip_h = flip
	world.add_child(s)
	if solid > 0.0:
		var body := StaticBody2D.new()
		body.collision_layer = 4
		body.collision_mask = 0
		var shape := CollisionShape2D.new()
		var c := CircleShape2D.new()
		c.radius = solid
		shape.shape = c
		body.add_child(shape)
		body.position = Vector2(0, -2)
		s.add_child(body)
		_solids.append(pos)
	return s

## Something lying flat on the ground, under everyone's feet.
func decal(tex_name: String, pos: Vector2, alpha := 1.0, turn := 0.0) -> Sprite2D:
	var s := Sprite2D.new()
	s.texture = load("res://assets/props/%s.png" % tex_name)
	s.position = pos
	s.modulate.a = alpha
	s.rotation = turn
	s.flip_h = _rng.randf() < 0.5
	ground_fx.add_child(s)
	return s

func _clear_of_solids(p: Vector2, gap: float) -> bool:
	for q in _solids:
		if p.distance_to(q) < gap:
			return false
	return true

## A free spot in the walkable band, off the path and clear of gates and other solid things.
func _spot(x0: float, x1: float, gap := 36.0, allow_path := false) -> Vector2:
	for attempt in 30:
		var p := Vector2(_rng.randf_range(x0, x1), _rng.randf_range(Main.TOP + 24.0, Main.BOT - 12.0))
		if not allow_path and (on_path(p) or on_path(p + Vector2(0, -16)) or on_path(p + Vector2(0, 16))):
			continue
		if _near_gate(p.x, 60.0) or not _clear_of_solids(p, gap):
			continue
		return p
	return Vector2.INF

# ---------------------------------------------------------------- the pieces of the level

func _beach() -> void:
	prop("wreck_hull", Vector2(196, mid - 34), 30.0)
	prop("wreck_mast", Vector2(292, mid + 92), 0.0)
	prop("crate", Vector2(262, mid - 78), 9.0)
	prop("crate", Vector2(284, mid - 70), 9.0)
	prop("barrel", Vector2(236, mid + 44), 8.0)
	prop("barrel", Vector2(408, mid + 108), 8.0, true)
	prop("driftwood", Vector2(170, mid + 70))
	prop("driftwood", Vector2(388, mid - 104), 0.0, true)
	prop("rock_b", Vector2(150, Main.TOP + 14), 14.0)
	prop("rock_a", Vector2(176, Main.TOP + 26), 9.0)
	prop("rock_b", Vector2(158, Main.BOT - 6), 14.0, true)
	for i in 14:
		var p := Vector2(_rng.randf_range(130, 440), _rng.randf_range(Main.TOP + 10, Main.BOT - 10))
		decal("shell" if i % 3 == 0 else "pebbles", p, 0.9)
	add_light(null, Color(1.0, 0.8, 0.6), 2.0, 0.22, Vector2(300, mid))

func _gates() -> void:
	for z: Dictionary in Main.ZONES:
		if z["gate"] < 0:
			gates.append(null)
			continue
		var x: float = z["gate"]
		var body := _wall(Rect2(x - 10, Main.TOP, 20, Main.BOT - Main.TOP))
		var parts: Array = []
		var y := Main.TOP + 18.0
		var i := 0
		while y < Main.BOT + 8.0:
			if i % 3 == 0:
				parts.append(prop("web_post", Vector2(x, y + 6.0)))
			var w := prop("web", Vector2(x + _rng.randf_range(-3, 3), y + 20.0), 0.0, _rng.randf() < 0.5)
			w.scale = Vector2(0.7, 1.0)
			parts.append(w)
			y += 28.0
			i += 1
		gates.append({"body": body, "parts": parts})
		for side: float in [-1.0, 1.0]:
			var lp := Vector2(x - 34.0, path_y(x - 34.0) + side * 64.0)
			prop("lamp_post", lp, 5.0)
			add_light(null, Color(1.0, 0.7, 0.35), 1.3, 0.8, lp + Vector2(0, -40))

func _arena_and_palace() -> void:
	for i in 9:
		var a := TAU * i / 9.0 + 0.3
		var p := arena + Vector2(cos(a) * 250.0, sin(a) * 112.0)
		decal("web", p, 0.5, _rng.randf() * TAU)
		if i % 3 == 0:
			prop("bones", p + Vector2(_rng.randf_range(-30, 30), _rng.randf_range(-16, 16)))
	for i in 4:
		var a2 := TAU * i / 4.0 + 0.8
		var p2 := arena + Vector2(cos(a2) * 318.0, sin(a2) * 138.0)
		prop("pumpkin", p2, 7.0)
		add_light(null, Color(1.0, 0.55, 0.2), 1.2, 0.9, p2 + Vector2(0, -8))
	decal("web", arena, 0.35).scale = Vector2(2, 2)
	# the palace gate, glimpsed through the trees at the far east
	prop("gate", palace)
	for side: float in [-1.0, 1.0]:
		prop("lamp_post", palace + Vector2(-70.0, side * 66.0 + 8.0), 5.0)
		add_light(null, Color(1.0, 0.8, 0.5), 1.4, 0.9, palace + Vector2(-70.0, side * 66.0 - 34.0))
	add_light(null, Color(1.0, 0.85, 0.6), 2.6, 0.8, palace + Vector2(-10, -40))

func _trees() -> void:
	var kinds := ["tree_a", "tree_b", "tree_c"]
	var x := 190.0
	while x < Main.FIELD_W + 80.0:
		for row in 2:
			prop(kinds[_rng.randi() % 3], Vector2(x + _rng.randf_range(-16, 16), Main.TOP - 6.0 - row * 40.0 - _rng.randf_range(0, 16)), 0.0, _rng.randf() < 0.5)
		prop(kinds[_rng.randi() % 3], Vector2(x + _rng.randf_range(-16, 16), Main.BOT + 104.0 + _rng.randf_range(0, 18)), 0.0, _rng.randf() < 0.5)
		if _rng.randf() < 0.5:
			prop(kinds[_rng.randi() % 3], Vector2(x + 26.0, Main.BOT + 142.0), 0.0, _rng.randf() < 0.5)
		x += _rng.randf_range(44, 66)
	# a few trees standing in the wood itself
	for i in 12:
		var p := _spot(540.0, Main.ZONES[3]["start"] - 40.0, 60.0)
		if p != Vector2.INF and not _in_arena(p, 1.1):
			prop(kinds[_rng.randi() % 3], p, 8.0, _rng.randf() < 0.5)

func _scatter() -> void:
	var x1 := Main.FIELD_W - 130.0
	for i in 18:
		var p := _spot(520.0, x1)
		if p != Vector2.INF and not _in_arena(p):
			var big := _rng.randf() < 0.35
			prop("rock_b" if big else "rock_a", p, 13.0 if big else 9.0, _rng.randf() < 0.5)
	for i in 14:
		var p := _spot(520.0, x1)
		if p != Vector2.INF and not _in_arena(p):
			prop("stump" if i % 2 == 0 else "log", p, 9.0 if i % 2 == 0 else 12.0, _rng.randf() < 0.5)
	for i in 44:
		var p := _spot(480.0, x1, 20.0)
		if p != Vector2.INF and not _in_arena(p):
			prop("bush_a" if i % 3 != 0 else "bush_b", p, 0.0, _rng.randf() < 0.5)
	for i in 14:
		var p := _spot(520.0, x1, 20.0)
		if p != Vector2.INF and not _in_arena(p):
			prop("shrooms", p)
			add_light(null, Color(0.7, 0.4, 1.0), 0.6, 0.55, p + Vector2(0, -6))
	# lanterns of the dead along the path
	var x := 600.0
	var side := 1.0
	while x < Main.ZONES[3]["start"] - 60.0:
		if not _near_gate(x, 70.0):
			var p := Vector2(x, path_y(x) + side * 66.0)
			prop("pumpkin", p, 7.0)
			add_light(null, Color(1.0, 0.55, 0.2), 1.2, 0.9, p + Vector2(0, -8))
		x += _rng.randf_range(210, 290)
		side = -side
	# old webs, thicker toward the nest
	for i in 34:
		var p := Vector2(_rng.randf_range(900, x1), _rng.randf_range(Main.TOP + 20, Main.BOT - 20))
		if _rng.randf() < (p.x - 700.0) / (x1 - 700.0) + 0.15:
			decal("web", p, 0.3, _rng.randf() * TAU).scale = Vector2.ONE * (0.5 if _rng.randf() < 0.6 else 1.0)
	# small things underfoot
	for i in 300:
		var p := Vector2(_rng.randf_range(470, Main.FIELD_W), _rng.randf_range(Main.TOP - 20, Main.BOT + 30))
		var t := ground.terrain(p)
		if t == Ground.PATH:
			if i % 4 == 0:
				decal("pebbles", p, 0.8)
		elif t == Ground.FOREST:
			var d := decal(["tuft_a", "tuft_a", "tuft_a", "tuft_b", "leaves", "tuft_a"][i % 6], p, 0.9)
			if i % 6 == 4:
				d.modulate = Color(0.75, 0.6, 0.55, 0.8)       # fallen leaves, dulled so they sit in the ground

func _weather(fx_layer: CanvasLayer) -> void:
	# fireflies, wherever the camera is
	_flies = CPUParticles2D.new()
	_flies.amount = 26
	_flies.lifetime = 6.0
	_flies.preprocess = 6.0
	_flies.local_coords = false
	_flies.emission_shape = CPUParticles2D.EMISSION_SHAPE_RECTANGLE
	_flies.emission_rect_extents = Vector2(340, 200)
	_flies.direction = Vector2(1, -0.3)
	_flies.spread = 180.0
	_flies.gravity = Vector2.ZERO
	_flies.initial_velocity_min = 3.0
	_flies.initial_velocity_max = 9.0
	_flies.scale_amount_min = 1.0
	_flies.scale_amount_max = 2.0
	var ramp := Gradient.new()
	ramp.set_color(0, Color(0.8, 1.0, 0.5, 0.0))
	ramp.add_point(0.3, Color(0.8, 1.0, 0.5, 0.9))
	ramp.add_point(0.7, Color(1.0, 0.95, 0.5, 0.9))
	ramp.set_color(ramp.get_point_count() - 1, Color(1.0, 0.9, 0.4, 0.0))
	_flies.color_ramp = ramp
	fx.add_child(_flies)
	# low fog drifting through the trees
	var noise := FastNoiseLite.new()
	noise.seed = 7
	noise.frequency = 0.012
	noise.fractal_octaves = 3
	var tex := NoiseTexture2D.new()
	tex.width = 256
	tex.height = 256
	tex.seamless = true
	tex.noise = noise
	var grad := Gradient.new()
	grad.set_color(0, Color(1, 1, 1, 0))
	grad.set_color(1, Color(1, 1, 1, 1))
	tex.color_ramp = grad
	_fog = Sprite2D.new()
	_fog.texture = tex
	_fog.centered = false
	_fog.region_enabled = true
	_fog.region_rect = Rect2(0, 0, 1800, 400)
	_fog.texture_repeat = CanvasItem.TEXTURE_REPEAT_ENABLED
	_fog.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_fog.scale = Vector2(3, 2)
	_fog.position = Vector2(-300, -80)
	_fog.modulate = Color(0.62, 0.72, 1.0, 0.13)
	var fog_layer := CanvasLayer.new()
	fog_layer.layer = 3
	fog_layer.follow_viewport_enabled = true
	add_child(fog_layer)
	fog_layer.add_child(_fog)

# ---------------------------------------------------------------- every frame

func tick(delta: float) -> void:
	for pair: Array in _tracked.duplicate():
		if is_instance_valid(pair[0]) and not (pair[0] is Enemy and pair[0].dead):
			pair[1].position = pair[0].global_position + pair[2]
		else:
			pair[1].queue_free()
			_tracked.erase(pair)
	_flies.global_position = camera.get_screen_center_position()
	_fog.region_rect.position += Vector2(5.0, 1.5) * delta
	if _shake > 0.0:
		_shake = maxf(0.0, _shake - delta * 14.0)
		camera.offset = Vector2(randf_range(-_shake, _shake), randf_range(-_shake, _shake))
	else:
		camera.offset = Vector2.ZERO
	if _bubble.visible:
		_place_bubble()

## A light on the ground. With a target it follows that node and is freed with it.
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
	elif energy >= 0.6:
		# lamps and lanterns that stand still also get a soft halo you can see against the dark
		var halo := Sprite2D.new()
		halo.texture = light_tex
		halo.position = offset
		halo.scale = Vector2.ONE * tex_scale * 0.16
		halo.modulate = Color(colour, 0.5)
		var mat := CanvasItemMaterial.new()
		mat.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD
		halo.material = mat
		halo.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		fx.add_child(halo)

func open_gate(i: int) -> void:
	if i < 0 or i >= gates.size() or gates[i] == null:
		return
	var g: Dictionary = gates[i]
	gates[i] = null
	g["body"].queue_free()
	for part: Sprite2D in g["parts"]:
		var t := create_tween()
		t.tween_property(part, "modulate:a", 0.0, 0.5 + randf() * 0.5)
		t.tween_callback(part.queue_free)
		burst(part.global_position + Vector2(0, -20), Color(0.9, 0.9, 1.0), 6, 30.0, 0.8)

# ---------------------------------------------------------------- passing effects

func shake(amount: float) -> void:
	_shake = maxf(_shake, amount)

func float_text(pos: Vector2, text: String, colour: Color) -> void:
	var l := UI.label(fx, pos + Vector2(randf_range(-5, 5) - 6, 0), text, 8, colour, true)
	var t := create_tween()
	t.tween_property(l, "position:y", l.position.y - 18.0, 0.6).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_CUBIC)
	t.parallel().tween_property(l, "modulate:a", 0.0, 0.6).set_ease(Tween.EASE_IN)
	t.tween_callback(l.queue_free)

## A puff of sparks or dust.
func burst(pos: Vector2, colour: Color, amount := 8, speed := 50.0, life := 0.45) -> void:
	var p := CPUParticles2D.new()
	p.position = pos
	p.amount = amount
	p.lifetime = life
	p.one_shot = true
	p.explosiveness = 1.0
	p.spread = 180.0
	p.gravity = Vector2(0, 60)
	p.initial_velocity_min = speed * 0.4
	p.initial_velocity_max = speed
	p.scale_amount_min = 1.0
	p.scale_amount_max = 2.0
	p.color = colour
	var ramp := Gradient.new()
	ramp.set_color(0, Color(1, 1, 1, 1))
	ramp.set_color(1, Color(1, 1, 1, 0))
	p.color_ramp = ramp
	fx.add_child(p)
	p.emitting = true
	get_tree().create_timer(life + 0.2).timeout.connect(p.queue_free)

func slash(pos: Vector2, dir: Vector2, reach: float, colour: Color, thrust: bool) -> void:
	var poly := Polygon2D.new()
	if thrust:
		poly.polygon = PackedVector2Array([Vector2(-reach * 0.6, -2), Vector2(reach * 0.5, 0), Vector2(-reach * 0.6, 2)])
	else:
		var pts := PackedVector2Array()
		for i in 9:
			var a := -1.1 + 2.2 * i / 8.0
			pts.append(Vector2(cos(a), sin(a)) * reach * 0.55)
		for i in 9:
			var a := 1.1 - 2.2 * i / 8.0
			pts.append(Vector2(cos(a) * 0.62 - 0.1, sin(a) * 0.8) * reach * 0.55)
		poly.polygon = pts
		poly.position = -dir * reach * 0.35
	poly.color = colour
	poly.position += pos
	poly.rotation = dir.angle()
	fx.add_child(poly)
	var t := create_tween()
	t.tween_property(poly, "modulate:a", 0.0, 0.16)
	t.tween_callback(poly.queue_free)

## A warning strip on the ground where a charge is about to come through.
func lane(pos: Vector2, dir: Vector2, length: float, half_width: float) -> void:
	var poly := Polygon2D.new()
	poly.polygon = PackedVector2Array([Vector2(0, -half_width), Vector2(length, -half_width), Vector2(length, half_width), Vector2(0, half_width)])
	poly.color = Color(1, 0.2, 0.15, 0.34)
	poly.position = pos
	poly.rotation = dir.angle()
	ground_fx.add_child(poly)
	var t := create_tween()
	t.tween_property(poly, "modulate:a", 0.0, 1.5)
	t.tween_callback(poly.queue_free)

# ---------------------------------------------------------------- speech bubbles

func _build_bubble() -> void:
	_bubble = Node2D.new()
	_bubble.visible = false
	_bubble.z_index = 50
	fx.add_child(_bubble)
	var tail := Polygon2D.new()
	tail.polygon = PackedVector2Array([Vector2(-4, -7), Vector2(4, -7), Vector2(0, 0)])
	tail.color = Color("#f6f1e4")
	_bubble.add_child(tail)
	_bubble_panel = PanelContainer.new()
	_bubble_panel.add_theme_stylebox_override("panel", UI.box(Color("#f6f1e4"), UI.INK, 3, 1, 5))
	_bubble.add_child(_bubble_panel)
	var col := VBoxContainer.new()
	col.add_theme_constant_override("separation", 0)
	_bubble_panel.add_child(col)
	_bubble_who = UI.label(col, Vector2.ZERO, "", 8, Color("#8a4a1a"), true)
	_bubble_who.add_theme_constant_override("outline_size", 0)
	_bubble_text = UI.label(col, Vector2.ZERO, "", 8, UI.INK)
	_bubble_text.add_theme_constant_override("outline_size", 0)
	_bubble_text.autowrap_mode = TextServer.AUTOWRAP_WORD
	_bubble_text.custom_minimum_size = Vector2(150, 0)

## Shows a line over a character's head, and returns the label so the caller can type it out.
func say(on: Node2D, who: String, text: String) -> Label:
	_bubble_on = on
	_bubble_who.text = who
	_bubble_text.text = text
	_bubble_text.visible_characters = 0
	_bubble_text.custom_minimum_size = UI.text_box(text, 150.0)
	_bubble_panel.reset_size()
	_bubble.visible = true
	_place_bubble()
	return _bubble_text

func hush() -> void:
	_bubble.visible = false
	_bubble_on = null

func _place_bubble() -> void:
	if _bubble_on == null or not is_instance_valid(_bubble_on):
		return
	var head := 44.0
	if _bubble_on is Actor:
		head = SpriteLib.foot(_bubble_on.who) * 2.0 + 4.0
	_bubble.position = _bubble_on.global_position + Vector2(0, -head)
	_bubble_panel.reset_size()
	var size := _bubble_panel.size
	var c := camera.get_screen_center_position()
	var left := clampf(_bubble.position.x - size.x / 2.0, c.x - 312.0, c.x + 312.0 - size.x)
	_bubble_panel.position = Vector2(left - _bubble.position.x, -size.y - 6.0)
