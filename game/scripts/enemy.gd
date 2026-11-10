class_name Enemy
extends Actor
## Arachno-Lanterns, Stalkers, egg sacs and the Brood Lantern boss. The host simulates them; other machines show puppets.

const KINDS := ["lantern", "stalker", "sac", "boss"]
const STATS := {
	"lantern": {"who": "lantern", "hp": 64.0, "speed": 104.0, "dmg": 12.0, "range": 40.0, "cd": 1.0, "xp": 12, "scale": 1.0, "embers": 2},
	"stalker": {"who": "stalker", "hp": 80.0, "speed": 150.0, "dmg": 16.0, "range": 44.0, "cd": 1.3, "xp": 20, "scale": 1.0, "embers": 3},
	"sac": {"who": "", "hp": 22.0, "speed": 0.0, "dmg": 0.0, "range": 0.0, "cd": 0.0, "xp": 6, "scale": 1.0, "embers": 1},
	"boss": {"who": "lantern", "hp": 900.0, "speed": 84.0, "dmg": 16.0, "range": 92.0, "cd": 1.8, "xp": 200, "scale": 2.6, "embers": 30},
}

var id := 0
var kind := ""
var puppet := false
var dmg := 1.0
var attack_range := 40.0
var attack_cd := 1.0
var cooldown := 0.6
var xp := 0
var embers := 0
var hatch_in := -1.0        # egg sacs only
var shaking := false
var sac_sprite: Sprite2D
# boss
var special_in := 4.0
var state := "chase"
var state_t := 0.0
var charge_dir := Vector2.ZERO
var summons_left := 2
var _hit_in_charge := {}

func setup(game_: Main, kind_: String, id_: int, puppet_: bool) -> void:
	game = game_
	kind = kind_
	id = id_
	puppet = puppet_
	team = 1
	var s: Dictionary = STATS[kind]
	max_hp = s["hp"] * (1.0 + 0.15 * maxi(0, Session.humans() - 1))
	hp = max_hp
	speed = s["speed"] * randf_range(0.9, 1.1)
	dmg = s["dmg"]
	attack_range = s["range"]
	attack_cd = s["cd"]
	xp = s["xp"]
	embers = s["embers"]
	if kind == "sac":
		radius = 18.0
		_build_sac()
		return
	radius = 16.0 * s["scale"] if kind != "boss" else 44.0
	build(s["who"], s["scale"], 24.0 * s["scale"])
	if kind == "boss":
		guard_time = 5.0
		base_modulate = Color(1.0, 0.75, 0.95)
		sprite.modulate = base_modulate
	if s["who"] == "lantern":
		game.add_light(self, Color(1.0, 0.55, 0.15), 1.5 * s["scale"], 0.8)

func _build_sac() -> void:
	who = "sac"
	sac_sprite = Sprite2D.new()
	sac_sprite.texture = load("res://assets/props/eggsac.png")
	sac_sprite.offset = Vector2(0, -22)
	add_child(sac_sprite)
	var shape := CollisionShape2D.new()
	var circle := CircleShape2D.new()
	circle.radius = radius
	shape.shape = circle
	add_child(shape)
	collision_layer = 4      # sacs block the way like scenery
	collision_mask = 0
	game.add_light(self, Color(1.0, 0.6, 0.2), 1.0, 0.6)

func take_damage(amount: float, from: Vector2, knockback := 160.0, stun_time := 0.0) -> void:
	if kind == "sac":
		if dead:
			return
		hp -= amount
		game.float_text(global_position + Vector2(0, -50), str(int(round(amount))), Color(1, 1, 0.8))
		game.emit_fx("lunge_e", [id, Vector2.ZERO, 0.0])
		if hp <= 0.0:
			die()
		return
	if kind == "boss":
		knockback *= 0.15
		stun_time *= 0.6
	super.take_damage(amount, from, knockback, stun_time)

func squash() -> void:
	var t := create_tween()
	t.tween_property(sac_sprite, "scale", Vector2(1.2, 0.85), 0.05)
	t.tween_property(sac_sprite, "scale", Vector2.ONE, 0.1)

func _physics_process(delta: float) -> void:
	if dead or game.over:
		return
	if kind == "sac":
		if shaking:
			sac_sprite.position.x = sin(Time.get_ticks_msec() / 25.0) * 2.5
		if puppet:
			global_position = net_pos
			return
		if hatch_in > 0.0:
			hatch_in -= delta
			shaking = hatch_in < 1.2
			if hatch_in <= 0.0:
				game.spawn_enemy("lantern", global_position)
				dead = true
				game.enemy_gone(self, false)
				queue_free()
		return
	if puppet:
		if _flash > 0.0:
			_flash -= delta
			sprite.modulate = Color(3, 3, 3) if _flash > 0.0 else base_modulate
		follow_net(delta)
		return
	cooldown -= delta
	if not tick_status(delta):
		net_moving = false
		return
	if kind == "boss":
		_boss(delta)
		return
	var target: Hero = _pick_target()
	if target == null:
		velocity = knock
		move_and_slide()
		play_anim(false)
		net_moving = false
		return
	var off := target.global_position - global_position
	var dist := off.length()
	facing = off.normalized()
	var move := Vector2.ZERO
	if dist > attack_range * 0.8:
		move = facing
		# a little weaving so packs don't stack on one spot
		move = (move + facing.orthogonal() * sin(Time.get_ticks_msec() / 400.0 + id % 7) * 0.35).normalized()
	elif cooldown <= 0.0:
		_bite(target)
	velocity = move * speed + knock
	move_and_slide()
	net_moving = move.length() > 0.1
	play_anim(net_moving)

func _pick_target() -> Hero:
	var best: Hero = null
	var best_score := INF
	for h: Hero in game.heroes:
		if h.down:
			continue
		var score := global_position.distance_to(h.global_position)
		if kind == "stalker":
			score += h.hp * 3.0      # Stalkers hunt the weakest
		if score < best_score:
			best_score = score
			best = h
	return best

func _bite(target: Hero) -> void:
	cooldown = attack_cd
	game.emit_fx("lunge_e", [id, facing, 14.0])
	if global_position.distance_to(target.global_position) <= attack_range + target.radius + 6.0:
		target.take_damage(dmg, global_position, 140.0)

func _boss(delta: float) -> void:
	var target: Hero = _pick_target()
	if target == null:
		return
	var off := target.global_position - global_position
	state_t -= delta
	net_moving = false
	# call the brood at two thirds and one third health
	if summons_left > 0 and hp < max_hp * (summons_left / 3.0):
		summons_left -= 1
		game.toast("The brood answers its mother!")
		for i in 3:
			game.spawn_enemy("lantern", global_position + Vector2.from_angle(TAU * i / 3.0) * 120.0)
	match state:
		"chase":
			facing = off.normalized()
			special_in -= delta
			var move := Vector2.ZERO
			if off.length() > attack_range * 0.75:
				move = facing
			elif cooldown <= 0.0:
				_bite(target)
			velocity = move * speed + knock
			move_and_slide()
			net_moving = move.length() > 0.1
			play_anim(net_moving)
			if special_in <= 0.0:
				special_in = randf_range(4.0, 6.0)
				if randf() < 0.5:
					state = "wind_spit"
					state_t = 0.7
				else:
					state = "wind_charge"
					state_t = 0.85
					charge_dir = off.normalized()
					game.emit_fx("tele", [global_position, charge_dir, 420.0])
		"wind_spit":
			facing = off.normalized()
			sprite.modulate = Color(1.6, 0.9, 0.5) if int(state_t * 12) % 2 == 0 else base_modulate
			if state_t <= 0.0:
				sprite.modulate = base_modulate
				for i in range(-3, 4):
					game.emit_fx("proj", [global_position + Vector2(0, -50), facing.rotated(i * 0.2), 1, 10.0, "fire"])
				state = "chase"
		"wind_charge":
			sprite.modulate = Color(1.8, 0.6, 0.6) if int(state_t * 14) % 2 == 0 else base_modulate
			if state_t <= 0.0:
				sprite.modulate = base_modulate
				state = "charge"
				state_t = 0.75
				_hit_in_charge = {}
		"charge":
			facing = charge_dir
			velocity = charge_dir * 520.0
			move_and_slide()
			net_moving = true
			play_anim(true)
			for h: Hero in game.heroes:
				if not h.down and not _hit_in_charge.has(h) and h.global_position.distance_to(global_position) < radius + 26.0:
					_hit_in_charge[h] = true
					h.take_damage(24.0, global_position, 380.0)
			if state_t <= 0.0 or get_slide_collision_count() > 0:
				state = "chase"
				stun = 0.9       # she dazes herself: the opening to strike

func die() -> void:
	dead = true
	game.enemy_gone(self, true)
	fade_out()

func fade_out() -> void:
	dead = true
	if kind == "sac":
		queue_free()
		return
	collision_mask = 0
	var t := create_tween()
	t.tween_property(self, "modulate", Color(1, 0.6, 0.2, 0.0), 0.35 if kind != "boss" else 1.2)
	t.tween_callback(queue_free)
