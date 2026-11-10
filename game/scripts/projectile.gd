class_name Projectile
extends Node2D
## Emma's stunning pebble (team 0) or a fireball (team 1).

var game: Node
var dir := Vector2.RIGHT
var team := 0
var dmg := 1.0
var kind := "pebble"
var life := 1.6
var speed := 420.0

func _ready() -> void:
	z_index = 5
	if kind == "fire":
		speed = 230.0
		life = 3.0
		game.add_light(self, Color(1, 0.5, 0.1), 0.7, 0.8)

func _draw() -> void:
	if kind == "pebble":
		draw_circle(Vector2.ZERO, 4.0, Color(0.15, 0.12, 0.2))
		draw_circle(Vector2.ZERO, 3.0, Color(0.85, 0.85, 0.95))
	else:
		draw_circle(Vector2.ZERO, 8.0, Color(1.0, 0.35, 0.05))
		draw_circle(Vector2.ZERO, 5.0, Color(1.0, 0.8, 0.2))

func _physics_process(delta: float) -> void:
	if game.over:
		return
	position += dir * speed * delta
	life -= delta
	if life <= 0.0 or not game.in_bounds(position):
		queue_free()
		return
	if team == 0:
		for e: Actor in game.enemies:
			if not e.dead and e.global_position.distance_to(position + Vector2(0, 24)) < e.radius + 12.0:
				e.take_damage(dmg, position - dir * 10.0, 60.0, 1.3)
				queue_free()
				return
	else:
		for h: Hero in game.heroes:
			if not h.down and (h.global_position + Vector2(0, -24)).distance_to(position) < 20.0:
				h.take_damage(dmg, position - dir * 10.0, 120.0)
				queue_free()
				return
