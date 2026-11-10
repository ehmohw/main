class_name Actor
extends CharacterBody2D
## Anything that walks, fights and can be hurt: heroes and enemies.

var game: Node            # the Main node
var who := ""             # sprite set name in Manifest
var team := 0             # 0 = heroes, 1 = enemies
var max_hp := 10.0
var hp := 10.0
var speed := 100.0
var facing := Vector2.DOWN
var stun := 0.0
var knock := Vector2.ZERO
var dead := false
var four_dir := false     # heroes have east/west art; enemies only south/north
var radius := 14.0
var sprite: AnimatedSprite2D
var base_modulate := Color.WHITE
var _flash := 0.0
var stun_guard := 0.0     # after a stun wears off, a spell of immunity so nothing is stun-locked
var guard_time := 1.6
var _stars: Label

func build(who_: String, sprite_scale := 1.0, shadow_w := 22.0) -> void:
	who = who_
	var shadow := Polygon2D.new()
	var pts := PackedVector2Array()
	for i in 16:
		var a := TAU * i / 16.0
		pts.append(Vector2(cos(a) * shadow_w, sin(a) * shadow_w * 0.4))
	shadow.polygon = pts
	shadow.color = Color(0, 0, 0, 0.45)
	add_child(shadow)
	sprite = AnimatedSprite2D.new()
	sprite.sprite_frames = SpriteLib.frames(who)
	sprite.offset = Vector2(0, -SpriteLib.foot(who))
	sprite.scale = Vector2.ONE * sprite_scale
	add_child(sprite)
	var shape := CollisionShape2D.new()
	var circle := CircleShape2D.new()
	circle.radius = radius
	shape.shape = circle
	add_child(shape)
	collision_layer = 0
	collision_mask = 4      # walls only
	motion_mode = CharacterBody2D.MOTION_MODE_FLOATING
	_stars = Label.new()
	_stars.text = "* * *"
	_stars.add_theme_color_override("font_color", Color(1, 0.9, 0.3))
	_stars.add_theme_font_size_override("font_size", 14)
	_stars.position = Vector2(-18, -SpriteLib.foot(who) * 2.0 * sprite_scale - 14)
	_stars.visible = false
	add_child(_stars)
	play_anim(false)

func dir_name() -> String:
	if four_dir and absf(facing.x) > absf(facing.y):
		return "east" if facing.x > 0 else "west"
	return "north" if facing.y < -0.3 else "south"

func play_anim(moving: bool, action := "") -> void:
	var d := dir_name()
	var name_ := ("walk_" if moving else "idle_") + d
	if action != "":
		name_ = action + "_" + d
	if not sprite.sprite_frames.has_animation(name_):
		name_ = ("walk_" if moving else "idle_") + "south"
		if not sprite.sprite_frames.has_animation(name_):
			name_ = "walk_south"
	if not four_dir:
		sprite.flip_h = facing.x < -0.2
	if sprite.animation != name_ or not sprite.is_playing():
		sprite.play(name_)

func tick_status(delta: float) -> bool:
	## Returns true when the actor may act this frame.
	if _flash > 0.0:
		_flash -= delta
		sprite.modulate = Color(3, 3, 3) if _flash > 0.0 else base_modulate
	knock = knock.move_toward(Vector2.ZERO, 900.0 * delta)
	stun_guard -= delta
	if stun > 0.0:
		stun -= delta
		_stars.visible = stun > 0.0
		velocity = knock
		move_and_slide()
		return false
	return true

func take_damage(amount: float, from: Vector2, knockback := 160.0, stun_time := 0.0) -> void:
	if dead:
		return
	if stun > 0.0 and team == 1:
		amount *= 1.5       # Emma's stun opens a weak point
	hp -= amount
	_flash = 0.09
	knock = (global_position - from).normalized() * knockback
	if stun_time > 0.0 and stun_guard <= 0.0:
		stun = stun_time
		stun_guard = stun_time + guard_time
	game.float_text(global_position + Vector2(0, -SpriteLib.foot(who) * 1.6), str(int(round(amount))),
		Color(1, 0.4, 0.35) if team == 0 else Color(1, 1, 0.8))
	if hp <= 0.0:
		hp = 0.0
		die()

func die() -> void:
	dead = true

func lunge(dir: Vector2, dist := 10.0) -> void:
	var t := create_tween()
	t.tween_property(sprite, "position", dir * dist, 0.06)
	t.tween_property(sprite, "position", Vector2.ZERO, 0.12)
