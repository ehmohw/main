class_name Pickup
extends Sprite2D
## Soul embers (currency) and hearts. They drift to the nearest standing hero; the host decides who collects.

var game: Main
var id := 0
var kind := "ember"
var vel := Vector2.ZERO
var age := 0.0

func _ready() -> void:
	texture = load("res://assets/props/%s.png" % kind)
	scale = Vector2.ONE * 0.6

func _process(delta: float) -> void:
	age += delta
	vel = vel.move_toward(Vector2.ZERO, 300 * delta)
	position += vel * delta
	offset.y = sin(age * 5.0) * 3.0
	if age < 0.35:
		return
	for h: Hero in game.heroes:
		if h.down:
			continue
		var d := h.global_position - global_position
		if d.length() < 22.0:
			if game.is_host:
				game.collect(self, h)
			return
		if d.length() < 150.0:
			position += d.normalized() * 260.0 * delta
