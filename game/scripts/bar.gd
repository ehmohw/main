class_name Bar
extends ColorRect
## A plain bar: a dark back with a coloured fill that eases toward its value.

var fill: ColorRect
var max_value := 1.0
var value := 1.0
var _shown := 1.0

func _process(delta: float) -> void:
	if fill == null:
		return
	var want := clampf(value / maxf(max_value, 0.001), 0.0, 1.0)
	_shown = move_toward(_shown, want, delta * 1.6) if absf(_shown - want) < 0.5 else want
	fill.size = Vector2(maxf(0.0, (size.x - 2.0) * _shown), size.y - 2.0)

## Green when healthy, amber when hurt, red when nearly gone.
func health_colours() -> void:
	var r := value / maxf(max_value, 0.001)
	fill.color = UI.GREEN if r > 0.5 else (UI.AMBER if r > 0.25 else UI.RED)
