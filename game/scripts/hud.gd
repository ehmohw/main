class_name Hud
extends CanvasLayer
## Everything drawn over the game: party frames, level and embers, the objective, the boss's bar, messages,
## title cards, the cutscene bars and narration, the pause menu and the end screen. Laid out for 640 x 360.

var game: Main
var _play: Control          # hidden during cutscenes
var _frames: Array = []
var _level: Label
var _xp: Bar
var _embers: Label
var _goal: Label
var _goal_box: PanelContainer
var _toast: Label
var _toast_box: PanelContainer
var _toast_t := 0.0
var _hint: Label
var _hint_t := 16.0
var _boss_box: Control
var _boss_bar: Bar
var _card: Control
var _card_title: Label
var _card_sub: Label
var _cut: Control
var _bars: Array[ColorRect] = []
var _story: PanelContainer
var _story_who: Label
var _story_text: Label
var _cut_hint: Label
var _menu: Control
var _end: Control
var _end_title: Label
var _end_rows: Label
var _end_foot: Label
var _shown_level := 1
var _card_tween: Tween
var _hurt: TextureRect

func build(game_: Main) -> void:
	game = game_
	layer = 10
	var root := Control.new()
	root.theme = UI.theme()
	root.size = UI.SCREEN
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(root)
	# a soft dark rim round the screen
	var vignette := TextureRect.new()
	vignette.texture = UI.glow(256, Color(0, 0, 0, 0), Color(0, 0, 0, 0.6))
	vignette.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	vignette.position = Vector2(-90, -50)
	vignette.size = UI.SCREEN + Vector2(180, 100)
	vignette.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(vignette)
	_hurt = TextureRect.new()
	_hurt.texture = UI.glow(128, Color(0.8, 0.05, 0.05, 0.0), Color(0.8, 0.05, 0.05, 0.75))
	_hurt.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_hurt.position = Vector2(-40, -24)
	_hurt.size = UI.SCREEN + Vector2(80, 48)
	_hurt.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_hurt.modulate.a = 0.0
	root.add_child(_hurt)
	_play = Control.new()
	_play.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(_play)
	_build_party()
	_build_status()
	_build_messages()
	_build_cut(root)
	_build_menu(root)
	_build_end(root)

# ---------------------------------------------------------------- pieces

func _build_party() -> void:
	for i in game.heroes.size():
		var h: Hero = game.heroes[i]
		var box := UI.panel(_play, Rect2(6, 6 + i * 25, 108, 22))
		var face := TextureRect.new()
		face.texture = UI.head(h.kind)
		face.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		face.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		face.position = Vector2(2, 2)
		face.size = Vector2(18, 18)
		face.mouse_filter = Control.MOUSE_FILTER_IGNORE
		box.add_child(face)
		var name_l := UI.label(box, Vector2(24, 0), h.display_name, 8, UI.TEXT, true)
		var tag := UI.label(box, Vector2(60, 0), "", 8, UI.DIM)
		tag.size = Vector2(44, 10)
		tag.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
		var bar := UI.bar(box, Rect2(24, 13, 80, 6), UI.GREEN)
		_frames.append({"box": box, "face": face, "name": name_l, "tag": tag, "bar": bar})

func _build_status() -> void:
	var box := UI.panel(_play, Rect2(540, 6, 94, 28))
	_level = UI.label(box, Vector2(5, 0), "LV 1", 8, UI.GOLD, true)
	_xp = UI.bar(box, Rect2(34, 4, 55, 5), Color("#8a7dff"))
	var ember := TextureRect.new()
	ember.texture = load("res://assets/ui/ember.png")
	ember.position = Vector2(5, 14)
	ember.mouse_filter = Control.MOUSE_FILTER_IGNORE
	box.add_child(ember)
	_embers = UI.label(box, Vector2(18, 13), "0", 8, UI.TEAL)
	# the objective, top centre
	_goal_box = PanelContainer.new()
	_goal_box.add_theme_stylebox_override("panel", UI.box(Color(UI.PANEL, 0.85), UI.EDGE, 2, 1, 4))
	_goal_box.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_play.add_child(_goal_box)
	_goal = UI.label(_goal_box, Vector2.ZERO, "", 8, UI.GOLD)
	set_goal("Head east through the woods")
	# the boss's bar, bottom centre
	_boss_box = Control.new()
	_boss_box.visible = false
	_play.add_child(_boss_box)
	UI.panel(_boss_box, Rect2(166, 331, 308, 22))
	UI.centred(_boss_box, Vector2(166, 331), 308, "The Brood Lantern", 8, Color("#ffb060"), true)
	_boss_bar = UI.bar(_boss_box, Rect2(172, 343, 296, 6), Color("#f07a28"))
	_hint = UI.label(_play, Vector2(6, 348), "Move: WASD / stick     Attack: Space / A     Switch hero: Tab / bumpers     Menu: Esc", 8, UI.DIM)

func _build_messages() -> void:
	_toast_box = PanelContainer.new()
	_toast_box.add_theme_stylebox_override("panel", UI.box(Color(UI.INK, 0.8), Color(0, 0, 0, 0), 2, 0, 5))
	_toast_box.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_toast_box.modulate.a = 0.0
	_play.add_child(_toast_box)
	_toast = UI.label(_toast_box, Vector2.ZERO, "", 8, UI.TEXT)
	_toast.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	# title cards for the level and its areas
	_card = Control.new()
	_card.modulate.a = 0.0
	_card.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_play.add_child(_card)
	var rule := ColorRect.new()
	rule.color = Color(UI.GOLD, 0.7)
	rule.position = Vector2(240, 112)
	rule.size = Vector2(160, 1)
	_card.add_child(rule)
	_card_title = UI.centred(_card, Vector2(0, 88), 640, "", 16, UI.GOLD, true)
	_card_sub = UI.centred(_card, Vector2(0, 116), 640, "", 8, UI.TEXT)

func _build_cut(root: Control) -> void:
	_cut = Control.new()
	_cut.visible = false
	_cut.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(_cut)
	for i in 2:
		var band := ColorRect.new()
		band.color = UI.INK
		band.size = Vector2(640, 30)
		_cut.add_child(band)
		_bars.append(band)
	_story = PanelContainer.new()
	_story.add_theme_stylebox_override("panel", UI.box(Color(UI.PANEL, 0.94), UI.EDGE, 3, 1, 7))
	_story.position = Vector2(120, 262)
	_story.custom_minimum_size = Vector2(400, 0)
	_cut.add_child(_story)
	var col := VBoxContainer.new()
	col.add_theme_constant_override("separation", 1)
	_story.add_child(col)
	_story_who = UI.label(col, Vector2.ZERO, "", 8, UI.GOLD, true)
	_story_text = UI.label(col, Vector2.ZERO, "", 8, UI.TEXT)
	_story_text.autowrap_mode = TextServer.AUTOWRAP_WORD
	_story_text.custom_minimum_size = Vector2(386, 0)
	_cut_hint = UI.label(_cut, Vector2(456, 341), "Space / A: next     Esc / B: skip scene", 8, UI.DIM)

func _build_menu(root: Control) -> void:
	_menu = Control.new()
	_menu.visible = false
	root.add_child(_menu)
	var shade := ColorRect.new()
	shade.color = Color(UI.INK, 0.6)
	shade.size = UI.SCREEN
	_menu.add_child(shade)
	UI.panel(_menu, Rect2(230, 112, 180, 124), UI.PANEL, UI.GOLD, 3)
	UI.centred(_menu, Vector2(230, 122), 180, "Menu", 16, UI.GOLD, true)
	UI.button(_menu, Rect2(256, 156, 128, 22), "Back to the game", func() -> void: game.set_menu(false))
	UI.button(_menu, Rect2(256, 184, 128, 22), "Leave to the main menu", func() -> void: game.leave())
	UI.centred(_menu, Vector2(230, 216), 180, "Esc closes this menu", 8, UI.DIM)

func _build_end(root: Control) -> void:
	_end = Control.new()
	_end.visible = false
	_end.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(_end)
	var shade := ColorRect.new()
	shade.color = Color(UI.INK, 0.72)
	shade.size = UI.SCREEN
	_end.add_child(shade)
	UI.panel(_end, Rect2(170, 92, 300, 176), UI.PANEL, UI.GOLD, 3)
	_end_title = UI.centred(_end, Vector2(170, 106), 300, "", 16, UI.GOLD, true)
	var rule := ColorRect.new()
	rule.color = Color(UI.GOLD, 0.6)
	rule.position = Vector2(230, 132)
	rule.size = Vector2(180, 1)
	_end.add_child(rule)
	_end_rows = UI.centred(_end, Vector2(190, 142), 260, "", 8, UI.TEXT)
	_end_rows.size = Vector2(260, 84)
	_end_rows.autowrap_mode = TextServer.AUTOWRAP_WORD
	_end_rows.add_theme_constant_override("line_spacing", 4)
	_end_foot = UI.centred(_end, Vector2(170, 246), 300, "", 8, UI.DIM)

# ---------------------------------------------------------------- every frame

func tick(delta: float) -> void:
	var mine := 0
	for h: Hero in game.heroes:
		if h.is_mine():
			mine += 1
	for i in game.heroes.size():
		var h: Hero = game.heroes[i]
		var f: Dictionary = _frames[i]
		var bar: Bar = f["bar"]
		bar.max_value = h.max_hp
		bar.value = h.hp
		bar.health_colours()
		var seat: Dictionary = h.seat()
		var edge := UI.EDGE
		var tag := "CPU"
		var tag_colour := Color("#6a6888")
		if h.is_mine():
			edge = UI.PLAYER[clampi(seat["dev"], 0, 3)]
			tag = "YOU" if mine == 1 else "P%d" % (seat["dev"] + 1)
			tag_colour = edge
		elif h.is_player():
			edge = UI.TEAL
			tag = "ONLINE"
			tag_colour = UI.TEAL
		if h.down:
			tag = "DOWN"
			tag_colour = UI.RED
		f["box"].add_theme_stylebox_override("panel", UI.box(Color(UI.PANEL_LIT if h.is_mine() else UI.PANEL, 0.9), edge, 2))
		f["tag"].text = tag
		f["tag"].add_theme_color_override("font_color", tag_colour)
		f["face"].modulate = Color(0.45, 0.45, 0.55) if h.down else Color.WHITE
		f["name"].add_theme_color_override("font_color", UI.DIM if h.down else UI.TEXT)
	_level.text = "LV %d" % game.level
	_xp.max_value = game.xp_need()
	_xp.value = game.xp
	_embers.text = str(game.embers)
	if game.level > _shown_level:
		_shown_level = game.level
		toast("Level %d!  The party grows stronger." % game.level, 2.5)
	var boss := game.boss()
	_boss_box.visible = boss != null
	if boss != null:
		_boss_bar.max_value = boss.max_hp
		_boss_bar.value = boss.hp
	_goal_box.reset_size()
	_goal_box.position = Vector2(320.0 - _goal_box.size.x / 2.0, 6)
	if _toast_t > 0.0:
		_toast_t -= delta
		_toast_box.modulate.a = clampf(_toast_t * 2.0, 0.0, 1.0)
		_toast_box.reset_size()
		_toast_box.position = Vector2(320.0 - _toast_box.size.x / 2.0, 322.0 if boss == null else 306.0)
	if _hint_t > 0.0:
		_hint_t -= delta
		_hint.modulate.a = clampf(_hint_t, 0.0, 1.0)
	_hint.visible = boss == null

## A red flash at the screen's edge: one of this machine's players was hit.
func hurt() -> void:
	_hurt.modulate.a = 0.55
	create_tween().tween_property(_hurt, "modulate:a", 0.0, 0.4)

func set_goal(text: String) -> void:
	_goal.text = text

func toast(text: String, seconds: float) -> void:
	_toast.text = text
	_toast_t = seconds
	_toast_box.modulate.a = 1.0

## A title card: a big line and a small one, fading in and out.
func card(title: String, sub: String, hold := 2.4) -> void:
	_card_title.text = title
	_card_sub.text = sub
	if _card_tween != null:
		_card_tween.kill()
	_card_tween = create_tween()
	_card_tween.tween_property(_card, "modulate:a", 1.0, 0.4)
	_card_tween.tween_interval(hold)
	_card_tween.tween_property(_card, "modulate:a", 0.0, 0.6)

## Clear a title card early, when someone starts speaking under it.
func card_hide() -> void:
	if _card_tween != null:
		_card_tween.kill()
	_card_tween = create_tween()
	_card_tween.tween_property(_card, "modulate:a", 0.0, 0.25)

func show_menu(on: bool) -> void:
	_menu.visible = on
	if on:
		_hint_t = 8.0

func menu_open() -> bool:
	return _menu.visible

# ---------------------------------------------------------------- cutscenes

func cut_on() -> void:
	_cut.visible = true
	_play.visible = false
	_story.visible = false
	_cut_hint.visible = false
	_bars[0].position = Vector2(0, -30)
	_bars[1].position = Vector2(0, 360)
	var t := create_tween().set_parallel()
	t.tween_property(_bars[0], "position:y", 0.0, 0.35).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_CUBIC)
	t.tween_property(_bars[1], "position:y", 330.0, 0.35).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_CUBIC)

func cut_off() -> void:
	_cut.visible = false
	_play.visible = true

## Narration, or a line from someone who isn't on screen. Returns the label so the caller can type it out.
func narrate(who: String, text: String) -> Label:
	_story.visible = true
	_story_who.text = who
	_story_who.visible = who != ""
	_story_text.text = text
	_story_text.visible_characters = 0
	_story_text.custom_minimum_size = Vector2(386, UI.text_box(text, 386.0).y)
	_story.reset_size()
	_story.position = Vector2(320.0 - _story.size.x / 2.0, 322.0 - _story.size.y)
	return _story_text

func cut_line(has_text: bool, boxed: bool) -> void:
	_cut_hint.visible = has_text
	if not boxed:
		_story.visible = false

# ---------------------------------------------------------------- the end

func finish(won: bool, level: int, embers: int, clock: float) -> void:
	_end.visible = true
	_play.visible = false
	var again := "R: play again" if game.is_host else "Waiting for the host to restart"
	if won:
		_end_title.text = "The Lantern Woods are clear"
		_end_rows.text = "Through the trees, a light: Omega Palace.\n\nParty level  %d\nSoul embers  %d\nTime  %d:%02d" % [level, embers, int(clock) / 60, int(clock) % 60]
	else:
		_end_title.text = "The woods take you"
		_end_rows.text = "Everyone is down.\n\nParty level  %d\nSoul embers  %d" % [level, embers]
	_end_foot.text = "%s     Esc: main menu" % again
