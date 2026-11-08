let colors = [ "#FFFFFF","#F6D32D","#F05697"];

let mySeed;

function setup() {
	createCanvas(800, 800);
	rectMode(CENTER);
	ellipseMode(CENTER);
	pixelDensity(2);
	document.body.style.backgroundColor = "#FFFFFF";
	colorMode(HSB, 360, 100, 100, 100);
	mySeed = floor(random(1, 100000));
	fill(0);
	square(width / 2, height / 2, width);
}

function draw() {
	randomSeed(mySeed);
	let mySize = width / 8;
	for (let xx = mySize; xx < width; xx += mySize * 2) {
		for (let yy = mySize; yy < height; yy += mySize * 2) {
			fill(100, 2);
			square(xx, yy, mySize * 1.75);
			circleShadow(xx, yy, mySize);
			circleShadow(xx, yy, mySize / 2);
			circleShadow(xx, yy, mySize / 4);
		}
	}

}

function circleShadow(xc, yc, mySize) {
	let rad;
	stroke(0);
	for (let i = 0; i < 5; i++) {
		fill(generateColor());
		let amp = random(20, 50);
		let freq1 = random(0.01, 0.03);
		let freq2 = random(0.01, 0.03);
		let phase1 = random(TWO_PI);
		let phase2 = random(TWO_PI);
		let offsetX = amp * sin(frameCount * freq1 + phase1);
		let offsetY = amp * sin(frameCount * freq2 + phase2);
		rad = random(0.1, 0.5);
		rad += rad / 2 * sin(frameCount * freq2);
		line(xc, yc, xc + offsetX, yc + offsetY);
		circle(xc + offsetX, yc + offsetY, mySize * rad);
	}
	circle(xc, yc, mySize * rad);
}

function generateColor() {
	return color(random(colors));
}

