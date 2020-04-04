extends Area2D

var velocity = 400
var direction = Vector2()
var start_position

func _ready():
	start_position = position
	
func start():
	position = start_position
	direction = Vector2(rand_range(-1,1),rand_range(-1,1))

func _process(delta):
		global_translate(direction*velocity*delta)
	
func area_entered(area):
	if area == get_node("../bat1") || area == get_node("../bat2"):
		direction = Vector2(-direction.x, direction.y)
	if area == get_node("../topborder") || area == get_node("../bottomborder"):
		direction = Vector2(direction.x, -direction.y)
	if area == get_node("../leftborder"):
		get_node("../label2").text = String(int(get_node("../label2").text) + 1)
		start()
	if area == get_node("../rightborder"):
		get_node("../label1").text = String(int(get_node("../label2").text) + 1)
		start()
		