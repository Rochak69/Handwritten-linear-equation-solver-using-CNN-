const canvas1 = document.getElementById("canvas1");
const canvas2 = document.getElementById("canvas2");
const canvas3 = document.getElementById("canvas3");

const ctx1 = canvas1.getContext("2d");
const ctx2 = canvas2.getContext("2d");
const ctx3 = canvas3.getContext("2d");

const clear1 = document.getElementById("clear1");
const clear2 = document.getElementById("clear2");
const clear3 = document.getElementById("clear3");

const eq1 = document.getElementById("eq1");
const eq2 = document.getElementById("eq2");
const eq3 = document.getElementById("eq3");

const X = document.getElementById("solnX");
const Y = document.getElementById("solnY");
const Z = document.getElementById("solnZ");

const error = document.getElementById("error");

const calc = document.getElementById("calc");

const lineWidth = 4 ;
const lineColor = "#000";

function prepareCanvas(canvas, ctx, clearBtn) {
	const canvasWidth = canvas.clientWidth;
	const canvasHeight = canvas.clientHeight;

	let isDrawing = false;
	let curPos; // current position

	canvas.width = canvasWidth;
	canvas.height = canvasHeight;

	function getPosition(clientX, clientY) {
		let box = canvas.getBoundingClientRect();
		return { x: clientX - box.x, y: clientY - box.y };
	}

	function draw(e) {
		if (isDrawing) {
			let pos = getPosition(e.clientX, e.clientY);

			ctx.strokeStyle = lineColor;
			ctx.lineWidth = lineWidth;
			ctx.lineCap = "round";
			ctx.lineJoin = "round";
			ctx.beginPath();
			ctx.moveTo(curPos.x, curPos.y);
			ctx.lineTo(pos.x, pos.y);
			ctx.stroke();
			ctx.closePath();
			curPos = pos;
		}
	}

	canvas.onmousedown = function (e) {
		isDrawing = true;
		curPos = getPosition(e.clientX, e.clientY);
		draw(e);
	};

	canvas.onmousemove = function (e) {
		draw(e);
	};

	canvas.onmouseup = function (e) {
		isDrawing = false;
	};

	// Set up touch events for mobile, etc
	canvas.addEventListener(
		"touchstart",
		function (e) {
			mousePos = getTouchPos(canvas, e);
			var touch = e.touches[0];
			var mouseEvent = new MouseEvent("mousedown", {
				clientX: touch.clientX,
				clientY: touch.clientY,
			});
			canvas.dispatchEvent(mouseEvent);
		},
		false
	);
	canvas.addEventListener(
		"touchend",
		function (e) {
			var mouseEvent = new MouseEvent("mouseup", {});
			canvas.dispatchEvent(mouseEvent);
		},
		false
	);
	canvas.addEventListener(
		"touchmove",
		function (e) {
			var touch = e.touches[0];
			var mouseEvent = new MouseEvent("mousemove", {
				clientX: touch.clientX,
				clientY: touch.clientY,
			});
			canvas.dispatchEvent(mouseEvent);
		},
		false
	);

	clearBtn.addEventListener("click", clearCanvas);

	function clearCanvas() {
		ctx.fillStyle = "#ffffff";
		ctx.fillRect(0, 0, canvasWidth, canvasHeight);
	}
	clearCanvas();

	// Get the position of a touch relative to the canvas
	function getTouchPos(canvasDom, touchEvent) {
		var rect = canvasDom.getBoundingClientRect();
		return {
			x: touchEvent.touches[0].clientX - rect.left,
			y: touchEvent.touches[0].clientY - rect.top,
		};
	}
}

window.addEventListener("load", resize);
window.addEventListener("resize", resize);

calc.addEventListener("click", () => {
	const img1 = new Image();
	const img2 = new Image();
	const img3 = new Image();

	img1.src = canvas1.toDataURL();
	img2.src = canvas2.toDataURL();
	img3.src = canvas3.toDataURL();

	imgData1 = img1.src.split(",")[1];
	imgData2 = img2.src.split(",")[1];
	imgData3 = img3.src.split(",")[1];

	let data = {
		Image1: imgData1,
		Image2: imgData2,
		Image3: imgData3,
	};

	clearAnswer();

	fetch("/upload3", {
		method: "POST",
		headers: {
			Accept: "application/json, text/plain, */*",
			"Content-Type": "application/json",
		},
		body: JSON.stringify(data),
	})
		.then((res) => res.json())
		.then((res) => {
			if (res.Success) {
				eq1.innerText = res.Eqn_1;
				eq2.innerText = res.Eqn_2;
				eq3.innerText = res.Eqn_3;

				X.innerText = res.Soln_X;
				Y.innerText = res.Soln_Y;
				Z.innerText = res.Soln_Z;
			} else {
				error.innerText = res.Error;
			}
		});
});

function resize() {
	prepareCanvas(canvas1, ctx1, clear1);
	prepareCanvas(canvas2, ctx2, clear2);
	prepareCanvas(canvas3, ctx3, clear3);
}

function clearAnswer() {
	eq1.innerText = "";
	eq2.innerText = "";
	eq3.innerText = "";
	X.innerText = "";
	Y.innerText = "";
	Z.innerText = "";
	error.innerText = "";
}
 
