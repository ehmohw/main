class_name Hero
extends Actor
## Emma, Leo, Bender or Cecil. A hero is driven by a player (here or on another machine) or by the computer.

const STATS := {
	"emma": {"name": "Emma", "role": "Slingshot: stuns", "hp": 60.0, "speed": 150.0, "dmg": 4.0, "cd": 0.7, "range": 300.0, "colour": Color(0.4, 0.75, 1.0)},
	"leo": {"name": "Leo", "role": "Trident: front line", "hp": 140.0, "speed": 135.0, "dmg": 13.0, "cd": 0.5, "range": 62.0, "colour": Color(0.75, 0.85, 0.95)},
	"bender": {"name": "Bender", "role": "Fast bites", "hp": 90.0, "speed": 190.0, "dmg": 7.0, "cd": 0.32, "range": 44.0, "colour": Color(0.95, 0.75, 0.45)},
	"cecil": {"name": "Cecil", "role": "Staff: poison", "hp": 80.0, "speed": 125.0, "dmg": 5.0, "cd": 0.9, "range": 280.0, "colour": Color(0.75, 0.5, 1.0)},
}

var idx := 0
var kind := ""
var display_name := ""
var base_hp := 10.0
var base_dmg := 1.0
var attack_cd := 0.5
var attack_range := 50.0
var cooldown := 0.0       # the owner's own pacing of attack requests
var host_cd := 0.0        # the host's check on it
var slot := 1             # follow position behind whoever this hero follows
var down := false
var _bob := 0.0
var _send_t := 0.0

func setup(game_: Main, idx_: int) -> void:
	game = game_
	idx = idx_
	kind = Session.party[idx]
	team = 0
	four_dir = true
	var s: Dictionary = STATS[kind]
	display_name = s["name"]
	base_hp = s["hp"]
	base_dmg = s["dmg"]
	speed = s["speed"]
	attack_cd = s["cd"]
	attack_range = s["range"]
	radius = 10.0 if kind == "bender" else 13.0
	build(kind, 1.0, 14.0 if kind == "bender" else 20.0)
	apply_level(false)
	hp = max_hp
	game.add_light(self, Color(1.0, 0.9, 0.75), 2.6, 0.5, Vector2(0, -10))

func ranged() -> bool:
	return kind == "emma" or kind == "cecil"

func seat() -> Dictionary:
	return Session.seats[idx]

func is_player() -> bool:
	return seat()["peer"] != 0

func is_mine() -> bool:
	return seat()["peer"] == game.my_id

## True on the one machine that moves this hero: its player's, or the host's for a computer ally.
func has_control() -> bool:
	return is_mine() or (not is_player() and game.is_host)

func apply_level(heal: bool) -> void:
	var mult: float = 1.0 + 0.12 * (game.level - 1)
	var old := max_hp
	max_hp = base_hp * mult
	if heal and not down:
		hp = minf(max_hp, hp + (max_hp - old) + max_hp * 0.3)

func damage() -> float:
	return base_dmg * (1.0 + 0.12 * (game.level - 1))

func _physics_process(delta: float) -> void:
	cooldown -= delta
	host_cd -= delta
	if game.over:
		return
	if game.cut:
		play_anim(false)
		return
	if not has_control():
		if _flash > 0.0:
			_flash -= delta
			sprite.modulate = Color(3, 3, 3) if _flash > 0.0 else base_modulate
		if not down:
			follow_net(delta)
		return
	net_pos = global_position
	if down:
		_send(delta, false)
		return
	if not tick_status(delta):
		_send(delta, false)
		return
	var move := Vector2.ZERO
	var want_attack := false
	if is_mine() and not game.autopilot:
		var pad: Dictionary = game.pads[seat()["dev"]]
		move = pad["move"]
		want_attack = pad["attack"]
	else:
		var r := _think(is_mine())
		move = r[0]
		want_attack = r[1]
	if move.length() > 0.1:
		facing = move.normalized()
	if want_attack and cooldown <= 0.0:
		cooldown = attack_cd
		if ranged() and is_mine() and not game.autopilot:
			var target: Actor = game.nearest_enemy(global_position, attack_range, facing)
			if target != null:
				facing = (target.global_position - global_position).normalized()
		game.to_host("req_attack", [idx, facing])
	velocity = move * speed + knock
	move_and_slide()
	if is_mine():
		global_position = game.keep_on_screen(global_position)
	var moving := move.length() > 0.1
	play_anim(moving)
	if not moving:
		_bob += delta * 3.0
		sprite.position.y = sin(_bob) * 1.2
	_send(delta, moving)

func _send(delta: float, moving: bool) -> void:
	net_moving = moving
	if game.is_host or not is_mine():
		return
	_send_t -= delta
	if _send_t <= 0.0:
		_send_t = 0.05
		game.hero_input.rpc_id(1, idx, global_position, facing, moving)

func _think(as_leader: bool) -> Array:
	## Computer allies, and the autopilot used for automated playtests.
	var lead: Hero = self if as_leader else game.leader_for(self)
	var foe: Actor = game.nearest_enemy(global_position, 300.0)
	var to_leader := Vector2.ZERO
	if lead != self and lead != null:
		to_leader = lead.global_position - global_position
	# step out of the Brood Lantern's charge lane
	var lane: Array = game.charge_lane()
	if not lane.is_empty():
		var rel: Vector2 = global_position - lane[0]
		var along: float = rel.dot(lane[1])
		var side: float = rel.dot(lane[1].orthogonal())
		if along > -40.0 and along < 480.0 and absf(side) < 90.0:
			return [lane[1].orthogonal() * (1.0 if side >= 0.0 else -1.0), false]
	if foe != null and to_leader.length() < 460.0:
		var to_foe := foe.global_position - global_position
		var dist := to_foe.length()
		facing = to_foe.normalized()
		if ranged():
			# keep a distance and fight from range
			if dist < 150.0:
				return [-to_foe.normalized(), dist < attack_range]
			return [Vector2.ZERO if dist < attack_range * 0.9 else to_foe.normalized(), dist < attack_range]
		if dist > attack_range * 0.8 + foe.radius:
			return [to_foe.normalized(), false]
		return [Vector2.ZERO, true]
	if as_leader:
		var goal: Vector2 = game.objective_point(self)
		var d := goal - global_position
		return [d.normalized() if d.length() > 20.0 else Vector2.ZERO, false]
	if lead != null:
		var spot := lead.global_position - lead.facing * (40.0 + 22.0 * slot) + lead.facing.orthogonal() * (28.0 if slot % 2 == 1 else -28.0)
		var d2 := spot - global_position
		if d2.length() > 30.0:
			return [d2.normalized() * (1.0 if d2.length() > 90.0 else 0.6), false]
	return [Vector2.ZERO, false]

## Runs on the host: the attack lands here, whoever asked for it.
func host_attack() -> void:
	if down or host_cd > 0.0:
		return
	host_cd = attack_cd * 0.85
	var origin := global_position
	if ranged():
		var target: Actor = game.nearest_enemy(origin, attack_range, facing)
		var dir := facing
		if target != null and (not is_player() or (target.global_position - origin).normalized().dot(facing) > 0.5):
			dir = (target.global_position - origin).normalized()
		game.emit_fx("proj", [origin + Vector2(0, -28) + dir * 14.0, dir, 0, damage(), "pebble" if kind == "emma" else "poison"])
		game.emit_fx("lunge_h", [idx, -dir, 4.0])
		return
	game.emit_fx("lunge_h", [idx, facing, 12.0 if kind == "leo" else 16.0])
	game.emit_fx("slash", [origin + Vector2(0, -22) + facing * attack_range * 0.6, facing, attack_range, STATS[kind]["colour"], kind == "leo"])
	for e: Enemy in game.enemies.duplicate():
		if e.dead:
			continue
		var off := e.global_position - origin
		if off.length() <= attack_range + e.radius and (off.length() < 24.0 or off.normalized().dot(facing) > 0.25):
			e.take_damage(damage(), origin, 220.0 if kind == "leo" else 80.0)

func apply_hit(k: Vector2, stun_time: float) -> void:
	if has_control():
		super.apply_hit(k, stun_time)
	else:
		game.hero_hit.rpc_id(seat()["peer"], idx, k, stun_time)

func die() -> void:
	set_down(true)
	game.hero_down(self)

func set_down(on: bool) -> void:
	if down == on:
		return
	down = on
	dead = on
	sprite.rotation = PI / 2 if on else 0.0
	base_modulate = Color(0.5, 0.5, 0.6) if on else Color.WHITE
	sprite.modulate = base_modulate
	if on:
		stun = 0.0
		show_stun(false)

func revive(fraction := 0.4) -> void:
	set_down(false)
	hp = max_hp * fraction
	game.float_text(global_position + Vector2(0, -80), display_name + " is back up!", Color(0.6, 1, 0.7))
