class_name UI
## The demo's look in one place: the font, the palette, and helpers that build styled labels, panels and bars.
## Everything is laid out for a 640 x 360 screen. Text sizes are 8, 16, 24 or 32 so the pixel fonts stay crisp.

const INK := Color("#0b0a17")
const PANEL := Color("#15142a")
const PANEL_LIT := Color("#262d5c")
const EDGE := Color("#494880")
const GOLD := Color("#ffd98a")
const TEXT := Color("#eeeaf6")
const DIM := Color("#9c9ab8")
const TEAL := Color("#7fe0d8")
const GREEN := Color("#5fd47a")
const AMBER := Color("#f0b040")
const RED := Color("#e8584e")
const PLAYER: Array[Color] = [Color("#5aa8ff"), Color("#ff6a6a"), Color("#6ae08a"), Color("#ffd24a")]
const SCREEN := Vector2(640, 360)

static var _fonts := {}
static var _theme: Theme

## Tiny5 for everything, and Press Start 2P for the big logo.
static func font(logo := false) -> Font:
	var key := "press-start-2p" if logo else "tiny5"
	if not _fonts.has(key):
		_fonts[key] = load("res://assets/fonts/%s.woff2" % key)
	return _fonts[key]

static func box(bg: Color, border := Color(0, 0, 0, 0), radius := 2, border_w := 1, pad := 0) -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = bg
	s.border_color = border
	s.set_border_width_all(border_w if border.a > 0.0 else 0)
	s.set_corner_radius_all(radius)
	s.anti_aliasing = false
	s.set_content_margin_all(pad)
	return s

static func theme() -> Theme:
	if _theme != null:
		return _theme
	var t := Theme.new()
	t.default_font = font()
	t.default_font_size = 8
	t.set_stylebox("normal", "Button", box(PANEL_LIT, EDGE, 2, 1, 4))
	t.set_stylebox("hover", "Button", box(Color("#34407e"), GOLD, 2, 1, 4))
	t.set_stylebox("pressed", "Button", box(Color("#1c2148"), GOLD, 2, 1, 4))
	t.set_stylebox("disabled", "Button", box(Color("#1a1a2c"), Color("#2c2c44"), 2, 1, 4))
	t.set_stylebox("focus", "Button", box(Color(0, 0, 0, 0), GOLD, 2, 1, 4))
	t.set_color("font_color", "Button", TEXT)
	t.set_color("font_hover_color", "Button", GOLD)
	t.set_color("font_pressed_color", "Button", GOLD)
	t.set_color("font_disabled_color", "Button", Color("#5c5a78"))
	t.set_stylebox("normal", "LineEdit", box(INK, EDGE, 2, 1, 4))
	t.set_stylebox("focus", "LineEdit", box(INK, GOLD, 2, 1, 4))
	t.set_color("font_color", "LineEdit", TEXT)
	t.set_color("font_placeholder_color", "LineEdit", Color("#6a6888"))
	t.set_color("font_color", "Label", TEXT)
	_theme = t
	return t

static func label(parent: Node, pos: Vector2, text: String, size := 8, colour := TEXT, _strong := false) -> Label:
	var l := Label.new()
	l.position = pos
	l.text = text
	l.add_theme_font_override("font", font(size >= 24))
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_color_override("font_color", colour)
	l.add_theme_color_override("font_outline_color", INK)
	l.add_theme_constant_override("outline_size", 3 if size <= 8 else 5)
	l.add_theme_constant_override("line_spacing", 1)
	parent.add_child(l)
	return l

## A label centred in a box of the given width.
static func centred(parent: Node, pos: Vector2, width: float, text: String, size := 8, colour := TEXT, bold := false) -> Label:
	var l := label(parent, pos, text, size, colour, bold)
	l.size = Vector2(width, size + 4)
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	return l

static func panel(parent: Node, rect: Rect2, bg := PANEL, border := EDGE, radius := 2) -> Panel:
	var p := Panel.new()
	p.position = rect.position
	p.size = rect.size
	p.add_theme_stylebox_override("panel", box(Color(bg, 0.9), border, radius))
	p.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(p)
	return p

static func bar(parent: Node, rect: Rect2, fill: Color) -> Bar:
	var b := Bar.new()
	b.position = rect.position
	b.size = rect.size
	b.color = INK
	b.fill = ColorRect.new()
	b.fill.color = fill
	b.fill.position = Vector2(1, 1)
	b.add_child(b.fill)
	b.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(b)
	return b

static func button(parent: Node, rect: Rect2, text: String, action: Callable) -> Button:
	var b := Button.new()
	b.position = rect.position
	b.size = rect.size
	b.text = text
	b.focus_mode = Control.FOCUS_NONE
	b.pressed.connect(action)
	parent.add_child(b)
	return b

## The room a wrapped line of small text needs: no wider than `max_width`, and tall enough for every line.
static func text_box(text: String, max_width: float) -> Vector2:
	var f := font()
	var one_line := f.get_string_size(text, HORIZONTAL_ALIGNMENT_LEFT, -1, 8).x + 2.0
	var w := minf(max_width, one_line)
	var wrapped := f.get_multiline_string_size(text, HORIZONTAL_ALIGNMENT_LEFT, w, 8)
	var lines := maxi(1, int(round(wrapped.y / f.get_height(8))))
	return Vector2(w, wrapped.y + lines)

## A character's head, cut from its front-facing sprite, for the party frames.
static func head(who: String) -> AtlasTexture:
	var at := AtlasTexture.new()
	at.atlas = load("res://assets/chars/%s/idle_south/0.png" % who)
	var r: Array = Manifest.DATA[who]["head"]
	at.region = Rect2(r[0], r[1], r[2], r[3])
	return at

## A soft round glow: white in the middle, clear at the rim. Used for lights and the screen's vignette.
static func glow(size := 256, inner := Color(1, 1, 1, 1), outer := Color(1, 1, 1, 0)) -> GradientTexture2D:
	var g := Gradient.new()
	g.set_color(0, inner)
	g.set_color(1, outer)
	var t := GradientTexture2D.new()
	t.gradient = g
	t.fill = GradientTexture2D.FILL_RADIAL
	t.fill_from = Vector2(0.5, 0.5)
	t.fill_to = Vector2(1.0, 0.5)
	t.width = size
	t.height = size
	return t
