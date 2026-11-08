/* Created for #WCCChallenge "Shadow"

This sketch renders a fractal shape with a shadow using the p5.utils library.;

References:
Franks laboratory Learn Creative Coding Fractals: https://www.youtube.com/watch?v=dQKYao-daYw
https://thecodingtrain.com/challenges/19-superellipse
https://openprocessing.org/@kfahn/2910529 // superellipse LUT grid
https://github.com/alptugan/p5.utils#beginShadow
*/

let utils = new p5.Utils(); // declare library so we can use the shadow function
let angle = 0;

// fractal variables
const maxLevel = 4;
const branches = 2;
let shape;
let S, c, s, sw;
let currentLevel = 0;

let sc = 0.7;

let myPalettes = [
	["#f94144", "#f3722c", "#f8961e", "#f9844a", "#f9c74f", "#90be6d", "#43aa8b", "#4d908e", "#577590", "#277da1"],
	["#d9ed92", "#b5e48c", "#99d98c", "#76c893", "#52b69a", "#34a0a4", "#168aad", "#1a759f", "#1e6091", "#184e77"],
	["#ff6d00", "#ff5400", "#ff8500", "#ff9e00", "#240046", "#3c096c", "#5a189a", "#7b2cbf", "#9d4edd", "#184e77"],
	["#54478c", "#2c699a", "#048ba8", "#0db39e", "#16db93", "#83e377", "#efea5a", "#f1c453", "#f29e4c", "#184e77"],
	["#ffffad", "#ffff5c", "#ffee33", "#ffda47", "#ffc60a", "#901447", "#c21e65", "#e02a7a", "#fd358f", "#fd5da5"],
	["#011a51", "#1957db", "#487bea", "#7ea3f1", "#c8d7f9", "#b83700", "#f06c00", "#fab129", "#fde9c3", "#fd5da5"],
	["#797d62", "#9b9b7a", "#baa587", "#d9ae94", "#f1dca7", "#ffcb69", "#e8ac65", "#d08c60", "#b58463", "#997b66"],
	["#8ecae6", "#73bfdc", "#58b4d1", "#219ebc", "#126782", "#023047", "#ffb703", "#fd9e02", "#fb8500", "#fb9017"],
	["#baebff", "#bbdbfe", "#bccbfd", "#bebcfc", "#bfacfb", "#c09cfa", "#c18cf9", "#c37df8", "#c46df7", "#c55df6"],
	["#114b5f", "#106776", "#0f838d", "#0e9fa4", "#0cbaba", "#07bad5", "#01baef", "#029ccc", "#027da9", "#035e86"]
]

OPC.palette('palette', myPalettes);

OPC.select('shapeChoice', {
	"flower": 0,
	"gear": 1,
	"rose curve": 2,
	"superellipse": 3,

});

OPC.slider({
	name: 'sides',
	value: 7,
	min: 3,
	max: 9,
	step: 1,
	label: 'Number of sides',
	description: 'number of sides'
});

OPC.slider({
	name: 'shapeSize',
	value: 0.08,
	min: 0.05,
	max: 0.12,
	step: 0.01,
	label: 'Shape size',
	description: 'shape size'
})


function setup() {
	S = min(windowWidth, windowHeight)
	createCanvas(S, S);
	s = S * shapeSize;

	chooseShape()
}

function chooseShape() {
	switch (shapeChoice) {
		case 0:
			shape = new Shape()
			shape.buildFlowerLUT()
			break;
		case 1:
			shape = new Gear();
			break;
		case 2:
			shape = new Shape()
			shape.buildRoseLUT()
			break;
		case 3:
			shape = new Shape()
			shape.buildSuperellipseLUT();
			break;
	}
}

function draw() {
	background(palette[3]);
	
	translate(width * 0.5, height * 0.5);
	rotate(angle);

	push()
	let shadowC = color(palette[0])
	shadowC.setAlpha(200)
	// Call begin shadow effect
	// Refer to documentation for the input arguments.
	utils.beginShadow(
		shadowC, // Shadow color 
		10 + abs(sin(millis() / 100)), // Blur amount of the shadow.
		cos(millis() * 0.001) * 10, // Shadow offset for x axis.
		sin(millis() * 0.001) * 10); // Shadow offset for y axis.

	angle += PI / 60;
	translate(-width * 0.5, -height * 0.5);
	drawFractal();

	utils.endShadow();
	pop();

}

function branch(level) {
	if (level > maxLevel) return;
	let index = level + 4;
	let col = color(palette[index])
	let sw = map(level, 0, maxLevel, 4.5, 3.5)
	for (let i = 1; i < branches; i++) {
		push();
		translate(s + (s / branches) * (i + 1), 0);
		scale(sc, sc);

		shape.show(s, angle, col, sw);

		rotate(angle);
		branch(level + 1);

		pop();

	}
}

function drawFractal() {
	push();
	translate(width / 2, height / 2);
	push()
	c = color(palette[4])
	shape.show(s, angle, c, 5.5);
	pop()
	for (let i = 0; i < sides; i++) {
		rotate(TWO_PI / sides);
		branch(0);
	}
	pop();
}

function parameterChanged(variableName, value) {
	if (variableName === 'shapeChoice') {
		chooseShape()
	}
	if (variableName === "shapeSize") {
    s = S * shapeSize;
	}

}

class Gear {
	constructor() {
		this.points = this.addShape()
	}

	hyperbolicTan(theta) {
		let e = 2.71828;
		let l = pow(e, 2 * theta);
		return (l - 1) / (l + 1);
	}

	addShape(a = 1, b = 6, m = 8) {
		let points = []
		for (let theta = 0; theta < TWO_PI; theta += 0.01) {
			let r =
				a +
				(1 / b) * this.hyperbolicTan(b * sin(m * theta));
			let x = r * sin(theta);
			let y = r * cos(theta);
			points.push(createVector(x, y))

		}
		return points;
	}

	show(r, a, col, sw) {
		push()
		//noFill()
		fill(col)
		noStroke()
		strokeWeight(sw)
		rotate(a)
		beginShape()
		for (let p of this.points) {
			vertex(r * p.x, r * p.y)
		}
		endShape(CLOSE)
		pop()
	}
}

class Shape {
	constructor(shapechoice) {
		this.choice = shapechoice;
		this.center = createVector(width / 2, height / 2)
		this.lut = new Map()
		//this.buildLUT()
		this.keyVals = [...this.lut.keys()];
	}

	buildFlowerLUT() {
		push()
		angleMode(RADIANS)
		this.lut = [];
		this.keyVals = [];
		const m = 8;
		const steps = 32;
		const count = steps + 1;

		for (let a = 0.1; a <= 2; a += 0.1) {
			//const d = k * m;
			const data = new Float32Array(count * 2);
			let k = 0;
			for (let i = 0; i <= steps; i++) {
				const theta = i * (HALF_PI / steps);
				//const theta = i * (TWO_PI*this.reduceDenominator(d, m) / steps);
				const r = a + cos(m * theta);
				const c = r * Math.cos(theta);
				const s = r * Math.sin(theta);

				data[k++] = c;  // x
				data[k++] = s;  // y
			}

			this.lut.push(data);
			this.keyVals.push(k);
		}

		this.steps = count;
		pop()
	}

	buildRoseLUT() {
		push()
		angleMode(RADIANS)
		this.lut = [];
		this.keyVals = [];
		const m = 8;
		const steps = 64;
		const count = steps + 1;

		for (let k = 0.1; k <= 4; k += 0.05) {
			const d = k * m;
			const data = new Float32Array(count * 2);
			let j = 0;
			for (let i = 0; i <= steps; i++) {
				const theta = i * (HALF_PI / steps);
				//const theta = i * (TWO_PI*this.reduceDenominator(d, m) / steps);
				const r = Math.cos(k * theta);
				const c = r * Math.cos(theta);
				const s = r * Math.sin(theta);

				data[j++] = c; //Math.pow(c, na); // x
				data[j++] = s; ///Math.pow(s, na); // y
			}

			this.lut.push(data);
			this.keyVals.push(k);
		}

		this.steps = count;
		pop()
	}

	buildSuperellipseLUT() {
		push()
		angleMode(RADIANS)
		this.lut = [];
		this.keyVals = [];

		const steps = 32;
		const count = steps + 1;

		for (let m = 0.6; m <= 3.0; m += 0.1) {
			const na = 2 / m;
			const data = new Float32Array(count * 2);
			let k = 0;
			for (let i = 0; i <= steps; i++) {
				const theta = i * (HALF_PI / steps);
				const c = Math.cos(theta);
				const s = Math.sin(theta);

				data[k++] = Math.pow(c, na); // x
				data[k++] = Math.pow(s, na); // y
			}

			this.lut.push(data);
			this.keyVals.push(m);
		}

		this.steps = count;
		pop()
	}

	drawShape(r, idx, col, sw) {
		const pts = this.lut[idx];

		const n = this.steps;

		// Render superellipse with fill
		if (shapeChoice === 3) {
			fill(col);
			noStroke()
		} else {
			stroke(col)
			noFill()
			strokeWeight(sw)
		}

		beginShape();
		this.shapePoints(pts, r, n);
		endShape(CLOSE);

	}

	// We have only created the Look ups for 1/4 of the points.  We now 
	// render each of the quadrants separately. We have to be careful about the 
	// winding order to avoid having the individual shapes cancel each other out when try to fill. 
	shapePoints(pts, r, n) {

		// Q1
		for (let i = 0; i < n; i++) {
			vertex(pts[i * 2] * r, pts[i * 2 + 1] * r);
		}

		// Q2
		for (let i = n - 1; i >= 0; i--) {
			vertex(-pts[i * 2] * r, pts[i * 2 + 1] * r);
		}

		// Q3
		for (let i = 0; i < n; i++) {
			vertex(-pts[i * 2] * r, -pts[i * 2 + 1] * r);
		}

		// Q4
		for (let i = n - 1; i >= 0; i--) {
			vertex(pts[i * 2] * r, -pts[i * 2 + 1] * r);
		}
	}

	show(r, a, c, sw) {
		// Get index into LUT table 
		let idx = floor(
			map(sin(a), -1, 1, 0, this.lut.length - 1)
		);

		this.drawShape(r, idx, c, sw);
	}
}
