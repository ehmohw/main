class_name Bar
extends ColorRect
## A plain HUD bar: a dark back with a coloured fill.

var fill: ColorRect
var max_value := 1.0
var value := 1.0:
	set(v):
		value = v
		if fill != null:
			fill.size = Vector2(maxf(0.0, (size.x - 2.0) * clampf(value / maxf(max_value, 0.001), 0.0, 1.0)), size.y - 2.0)
