class_name Projectile
extends Node2D
## Emma's stunning pebble, Cecil's poison bolt (team 0) or a fireball (team 1).
## Only the host's copy does damage; everyone else's is for show.

var game: Main
var dir := Vector2.RIGHT
var team := 0
var dmg := 1.0
var kind := "pebble"
var life := 1.6
var speed := 300.0

func _ready() -> void:
	if kind == "fire":
		speed = 160.0
		life = 3.0
		game.add_light(self, Color(1, 0.5, 0.1), 0.5, 0.8)
	elif kind == "poison":
		speed = 240.0
		game.add_light(self, Color(0.5, 1.0, 0.3), 0.4, 0.6)

func _draw() -> void:
	if kind == "pebble":
		draw_rect(Rect2(-2, -2, 4, 4), UI.INK)
		draw_rect(Rect2(-1, -1, 2, 2), Color(0.88, 0.88, 0.96))
	elif kind == "poison":
		draw_rect(Rect2(-3, -3, 6, 6), Color(0.2, 0.5, 0.12))
		draw_rect(Rect2(-2, -2, 4, 4), Color(0.7, 1.0, 0.4))
	else:
		draw_rect(Rect2(-4, -4, 8, 8), Color(0.75, 0.2, 0.05))
		draw_rect(Rect2(-3, -3, 6, 6), Color(1.0, 0.45, 0.08))
		draw_rect(Rect2(-1, -1, 3, 3), Color(1.0, 0.85, 0.3))

func _physics_process(delta: float) -> void:
	if game.frozen:
		return
	position += dir * speed * delta
	life -= delta
	if life <= 0.0 or not game.in_bounds(position):
		queue_free()
		return
	if team == 0:
		for e: Enemy in game.enemies:
			if not e.dead and e.global_position.distance_to(position + Vector2(0, 16)) < e.radius + 8.0:
				if game.is_host:
					if kind == "poison":
						e.take_damage(dmg, position - dir * 10.0, 28.0)
						e.poison_t = 4.0
						e.poison_dps = dmg * 0.8
					else:
						e.take_damage(dmg, position - dir * 10.0, 42.0, 1.3)
				queue_free()
				return
	else:
		for h: Hero in game.heroes:
			if not h.down and (h.global_position + Vector2(0, -16)).distance_to(position) < 13.0:
				if game.is_host:
					h.take_damage(dmg, position - dir * 10.0, 84.0)
				queue_free()
				return
