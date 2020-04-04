extends Node

func _ready():
	$ball.start()
	pass

func _process(delta):
	if(Input.is_action_pressed("p1_up") && $bat1.get_overlapping_areas().find($topborder) == -1):
		$bat1.global_translate(Vector2(0,-100*delta))
	if(Input.is_action_pressed("p1_down") && $bat1.get_overlapping_areas().find($bottomborder) == -1):
		$bat1.global_translate(Vector2(0, 100*delta))
	if(Input.is_action_pressed("p2_up") && $bat2.get_overlapping_areas().find($topborder) == -1):
		$bat2.global_translate(Vector2(0,-100)*delta)
	if(Input.is_action_pressed("p2_down") && $bat2.get_overlapping_areas().find($bottomborder) == -1):
		$bat2.global_translate(Vector2(0,100)*delta)