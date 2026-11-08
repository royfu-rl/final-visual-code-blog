  visualSuite('Image Based Lighting', function () {
    const shinesses = [50, 150];
    for (const shininess of shinesses) {
      visualTest(
        `${shininess < 100 ? 'low' : 'high'} shininess`,
        async function (p5, screenshot) {
          p5.createCanvas(100, 100, p5.WEBGL);

          // Load the environment map
          const env = await p5.loadImage('test/unit/assets/spheremap.jpg');
          p5.clear();

          // Set up panorama background
          p5.panorama(env);

          // Set up image-based lighting
          p5.push();
          p5.imageLight(env);
          p5.ambientLight(10);

          // Configure materials
          p5.specularMaterial(255);
          p5.shininess(shininess);
          p5.metalness(100);
          p5.noStroke();

          // Draw a sphere in the center
          p5.fill('white');
          p5.sphere(25);

          p5.pop();

          screenshot();
        },
        { timeout: 2000 }
      );
    }
  });
