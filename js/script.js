var flag = 0;
baby();
function baby() {
	var baby = document.getElementById("baby");
	var arm = document.getElementById("arm");
	var leg = document.getElementById("leg");
	var escape = document.getElementById("escape");
	var rays = document.getElementById("rays");
	if (flag == 0) {
		baby.style.webkitAnimationName = "";
		arm.style.webkitAnimationName = "";
		leg.style.webkitAnimationName = "";
		escape.style.webkitAnimationName = "";
		rays.style.webkitAnimationName = "";
	}
	else if (flag === 1) {
		baby.style.webkitAnimationName = "baby";
		arm.style.webkitAnimationName = "arm";
		leg.style.webkitAnimationName = "leg";
		escape.style.webkitAnimationName = "escape";
		rays.style.webkitAnimationName = "flash";
	}
}