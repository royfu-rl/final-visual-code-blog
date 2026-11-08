    visualTest('Strands tutorial', function (p5, screenshot) {
      // From Luke Plowden's Intro to Strands tutorial
      // https://beta.p5js.org/tutorials/intro-to-p5-strands/

      function starShaderCallback({ p5 }) {
        const time = p5.uniformFloat(() => p5.millis());
        const skyRadius = p5.uniformFloat(90);

        function rand2(st) {
          return p5.sin((st.x + st.y) * 123.456);
        }

        function semiSphere() {
          let id = p5.instanceIndex;
          let theta = rand2([id, 0.1234]) * p5.TWO_PI + time / 100000;
          let phi = rand2([id, 3.321]) * p5.PI + time / 50000;

          let r = skyRadius;
          r *= p5.sin(phi);
          let x = r * p5.sin(phi) * p5.cos(theta);
          let y = r * 1.5 * p5.cos(phi);
          let z = r * p5.sin(phi) * p5.sin(theta);
          return [x, y, z];
        }

        p5.getWorldInputs(inputs => {
          inputs.position += semiSphere();
          return inputs;
        });

        p5.getObjectInputs(inputs => {
          let size = 1 + 0.5 * p5.sin(time * 0.002 + p5.instanceIndex);
          inputs.position *= size;
          return inputs;
        });
      }

      function pixelateShaderCallback({ p5 }) {
        const pixelCountX = p5.uniformFloat(() => 100);

        p5.getColor((inputs, canvasContent) => {
          const aspectRatio = inputs.canvasSize.x / inputs.canvasSize.y;
          const pixelSize = [pixelCountX, pixelCountX / aspectRatio];

          let coord = inputs.texCoord;
          coord = p5.floor(coord * pixelSize) / pixelSize;

          let col = p5.getTexture(canvasContent, coord);
          return col; //[coord, 0, 1];
        });
      }

      function bloomShaderCallback({ p5, originalImage }) {
        const preBlur = p5.uniformTexture(() => originalImage);

        getColor((input, canvasContent) => {
          const blurredCol = p5.getTexture(canvasContent, input.texCoord);
          const originalCol = p5.getTexture(preBlur, input.texCoord);

          const intensity = p5.max(originalCol, 0.1) * 12.2;

          const bloom = originalCol + blurredCol * intensity;
          return [bloom.rgb, 1];
        });
      }

      p5.createCanvas(200, 200, p5.WEBGL);
      const stars = p5.buildGeometry(() => p5.sphere(4, 4, 2));
      const originalImage = p5.createFramebuffer();

      function fresnelShaderCallback({ p5 }) {
        const fresnelPower = p5.uniformFloat(2);
        const fresnelBias = p5.uniformFloat(-0.1);
        const fresnelScale = p5.uniformFloat(2);

        p5.getCameraInputs(inputs => {
          let n = p5.normalize(inputs.normal);
          let v = p5.normalize(-inputs.position);
          let base = 1.0 - p5.dot(n, v);
          let fresnel = fresnelScale * p5.pow(base, fresnelPower) + fresnelBias;
          let col = p5.mix([0, 0, 0], [1, 0.5, 0.7], fresnel);
          inputs.color = [col, 1];
          return inputs;
        });
      }

      const starShader = p5
        .baseMaterialShader()
        .modify(starShaderCallback, { p5 });
      const starStrokeShader = p5
        .baseStrokeShader()
        .modify(starShaderCallback, { p5 });
      const fresnelShader = p5
        .baseColorShader()
        .modify(fresnelShaderCallback, { p5 });
      const bloomShader = p5
        .baseFilterShader()
        .modify(bloomShaderCallback, { p5, originalImage });
      const pixelateShader = p5
        .baseFilterShader()
        .modify(pixelateShaderCallback, { p5 });

      originalImage.begin();
      p5.background(0);

      p5.push();
      p5.strokeWeight(2);
      p5.stroke(255, 0, 0);
      p5.fill(255, 100, 150);
      p5.strokeShader(starStrokeShader);
      p5.shader(starShader);
      p5.model(stars, 100);
      p5.pop();

      p5.push();
      p5.shader(fresnelShader);
      p5.noStroke();
      p5.sphere(30);
      p5.filter(pixelateShader);
      p5.pop();

      originalImage.end();

      p5.imageMode(p5.CENTER);
      p5.image(originalImage, 0, 0);

      p5.filter(p5.BLUR, 5);
      p5.filter(bloomShader);

      screenshot();
    });
