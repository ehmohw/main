class_name Pickup
extends Sprite2D
## Soul embers (currency) and hearts. They drift to the nearest standing hero; the host decides who collects.

var game: Main
var id := 0
var kind := "ember"
var vel := Vector2.ZERO
var age := 0.0

func _ready() -> void:
	texture = load("res://assets/ui/%s.png" % kind)

func _process(delta: float) -> void:
	age += delta
	if game.paused:
		return
	vel = vel.move_toward(Vector2.ZERO, 210 * delta)
	position += vel * delta
	offset.y = roundf(sin(age * 5.0) * 2.0)
	if age < 0.35:
		return
	for h: Hero in game.heroes:
		if h.down:
			continue
		var d := h.global_position - global_position
		if d.length() < 15.0:
			if game.is_host:
				game.collect(self, h)
			return
		if d.length() < 104.0:
			position += d.normalized() * 180.0 * delta
