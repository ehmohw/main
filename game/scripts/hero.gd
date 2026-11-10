class_name Hero
extends Actor
## Emma, Leo or Bender. One is controlled by the player; the other two follow and fight on their own.

const STATS := {
	"emma": {"name": "Emma", "hp": 60.0, "speed": 150.0, "dmg": 4.0, "cd": 0.7, "range": 300.0, "colour": Color(0.4, 0.75, 1.0)},
	"leo": {"name": "Leo", "hp": 140.0, "speed": 135.0, "dmg": 13.0, "cd": 0.5, "range": 62.0, "colour": Color(0.75, 0.85, 0.95)},
	"bender": {"name": "Bender", "hp": 90.0, "speed": 190.0, "dmg": 7.0, "cd": 0.32, "range": 44.0, "colour": Color(0.95, 0.75, 0.45)},
}

var kind := ""
var display_name := ""
var controlled := false
var base_hp := 10.0
var base_dmg := 1.0
var attack_cd := 0.5
var attack_range := 50.0
var cooldown := 0.0
var slot := 0             # follow position behind the leader
var down := false
var _bob := 0.0

func setup(game_: Node, kind_: String, slot_: int) -> void:
	game = game_
	kind = kind_
	slot = slot_
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
	game.add_light(self, Color(1.0, 0.9, 0.75), 2.6, 0.55, Vector2(0, -10))

func apply_level(heal: bool) -> void:
	var mult: float = 1.0 + 0.12 * (game.level - 1)
	var old := max_hp
	max_hp = base_hp * mult
	if heal and not down:
		hp = minf(max_hp, hp + (max_hp - old) + max_hp * 0.3)

func damage() -> float:
	return base_dmg * (1.0 + 0.12 * (game.level - 1))

func _physics_process(delta: float) -> void:
	if down or game.over:
		return
	cooldown -= delta
	if not tick_status(delta):
		return
	var move := Vector2.ZERO
	var want_attack := false
	if controlled and not game.autopilot:
		move = Input.get_vector("move_left", "move_right", "move_up", "move_down")
		want_attack = Input.is_action_pressed("attack")
	else:
		var r := _think()
		move = r[0]
		want_attack = r[1]
	if move.length() > 0.1:
		facing = move.normalized()
	if want_attack and cooldown <= 0.0:
		_attack()
	velocity = move * speed + knock
	move_and_slide()
	play_anim(move.length() > 0.1)
	if move.length() < 0.1:
		_bob += delta * 3.0
		sprite.position.y = sin(_bob) * 1.2

func _think() -> Array:
	## Ally AI (and the autopilot used for automated playtests).
	var leader: Hero = game.leader()
	var foe: Actor = game.nearest_enemy(global_position, 300.0)
	var to_leader := Vector2.ZERO
	if leader != self and leader != null:
		to_leader = leader.global_position - global_position
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
		if kind == "emma":
			# Emma keeps her distance and stuns from range
			if dist < 150.0:
				return [-to_foe.normalized(), dist < attack_range]
			return [Vector2.ZERO if dist < attack_range * 0.9 else to_foe.normalized(), dist < attack_range]
		if dist > attack_range * 0.8 + foe.radius:
			return [to_foe.normalized(), false]
		return [Vector2.ZERO, true]
	if leader == self:
		# autopilot only: head for the next objective
		var goal: Vector2 = game.objective_point()
		var d := goal - global_position
		return [d.normalized() if d.length() > 20.0 else Vector2.ZERO, false]
	if leader != null:
		var spot := leader.global_position - leader.facing * (46.0 * slot) + leader.facing.orthogonal() * (26.0 if slot == 1 else -26.0)
		var d2 := spot - global_position
		if d2.length() > 30.0:
			return [d2.normalized() * (1.0 if d2.length() > 90.0 else 0.6), false]
	return [Vector2.ZERO, false]

func _attack() -> void:
	cooldown = attack_cd
	if kind == "emma":
		var target: Actor = game.nearest_enemy(global_position, attack_range, facing if controlled else Vector2.ZERO)
		var dir := facing
		if target != null:
			dir = (target.global_position - global_position).normalized()
			facing = dir
		game.spawn_projectile(global_position + Vector2(0, -28) + dir * 14.0, dir, 0, damage(), "pebble")
		lunge(-dir, 4.0)
		return
	lunge(facing, 12.0 if kind == "leo" else 16.0)
	game.slash(global_position + Vector2(0, -22) + facing * attack_range * 0.6, facing, attack_range, STATS[kind]["colour"], kind == "leo")
	for e: Actor in game.enemies.duplicate():
		if e.dead:
			continue
		var off := e.global_position - global_position
		if off.length() <= attack_range + e.radius and (off.length() < 24.0 or off.normalized().dot(facing) > 0.25):
			e.take_damage(damage(), global_position, 220.0 if kind == "leo" else 80.0)

func die() -> void:
	down = true
	dead = true
	sprite.rotation = PI / 2
	sprite.modulate = Color(0.5, 0.5, 0.6)
	base_modulate = sprite.modulate
	game.hero_down(self)

func revive(fraction := 0.4) -> void:
	down = false
	dead = false
	hp = max_hp * fraction
	sprite.rotation = 0.0
	base_modulate = Color.WHITE
	sprite.modulate = Color.WHITE
	game.float_text(global_position + Vector2(0, -80), display_name + " is back up!", Color(0.6, 1, 0.7))
