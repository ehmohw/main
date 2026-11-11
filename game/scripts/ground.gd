class_name Ground
extends Node2D
## The ground, drawn from corner-matched tiles. Each grid corner holds a terrain; a tile is picked by its four corners.
## Terrains run sea, sand, forest floor, dirt path, and each neighbouring pair has its own sheet of sixteen tiles.

const T := 32
const SEA := 0
const SAND := 1
const FOREST := 2
const PATH := 3
const SHEETS := ["sea_sand", "sand_forest", "forest_path"]

var cols := 0
var rows := 0
var _v := PackedByteArray()
var _tex: Array[Texture2D] = []

func setup(width: float, height: float, terrain_at: Callable) -> void:
	cols = int(ceil(width / T))
	rows = int(ceil(height / T))
	_v.resize((cols + 1) * (rows + 1))
	for y in rows + 1:
		for x in cols + 1:
			_v[y * (cols + 1) + x] = terrain_at.call(Vector2(x * T, y * T))
	for s: String in SHEETS:
		_tex.append(load("res://assets/tiles/%s.png" % s))
	queue_redraw()

## The terrain under a point (by its nearest grid corner).
func terrain(p: Vector2) -> int:
	var x := clampi(int(round(p.x / T)), 0, cols)
	var y := clampi(int(round(p.y / T)), 0, rows)
	return _v[y * (cols + 1) + x]

func _draw() -> void:
	for cy in rows:
		for cx in cols:
			var i := cy * (cols + 1) + cx
			var c := [_v[i], _v[i + 1], _v[i + cols + 1], _v[i + cols + 2]]
			var lo: int = c.min()
			var hi: int = c.max()
			var sheet := mini(lo, 2)
			var src := Vector2i.ZERO
			if lo == hi:
				# all one terrain: the plain tile, or one of its mirrored copies so the grid doesn't show
				var upper := lo > sheet
				var pick := (cx * 7 + cy * 13 + cx * cy) % 3
				if pick == 0:
					src = Vector2i(3, 3) if upper else Vector2i(0, 0)
				else:
					src = Vector2i((2 if upper else 0) + pick - 1, 4)
			else:
				var mask := 0
				for k in 4:
					if c[k] > lo:
						mask |= 1 << k
				src = Vector2i(mask % 4, mask / 4)
			draw_texture_rect_region(_tex[sheet], Rect2(cx * T, cy * T, T, T), Rect2(src.x * T, src.y * T, T, T))
