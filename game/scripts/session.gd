class_name Session
## What survives a scene reload: how we are playing, and who controls which hero.

const KINDS := ["emma", "leo", "bender", "cecil"]

static var mode := ""            # "" (menu), "local", "host" or "client"
static var seats: Array = []     # one per hero: {"peer": 0 for the computer or a player's network id, "dev": that player's input device}
static var in_game := false
static var message := ""

static func reset_seats() -> void:
	seats = []
	for k in KINDS:
		seats.append({"peer": 0, "dev": -1})

static func humans() -> int:
	var n := 0
	for s: Dictionary in seats:
		if s["peer"] != 0:
			n += 1
	return n

static func dev_name(dev: int) -> String:
	return "keyboard" if dev == 0 else "controller %d" % dev
