    visualSuite('textStyle', function () {
      visualTest('all text styles', async function (p5, screenshot) {
        p5.createCanvas(150, 150);
        const font = await p5.loadFont(
          'https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&display=swap'
        );
        p5.textSize(20);
        p5.textFont(font);
        p5.textAlign(p5.LEFT, p5.TOP);

        p5.text('Regular Text', 0, 0);
        p5.textStyle(p5.BOLD);
        p5.text('Bold Text', 0, 30);
        p5.textStyle(p5.ITALIC);
        p5.text('Italic Text', 0, 60);
        p5.textStyle(p5.BOLDITALIC);
        p5.text('Bold Italic Text', 0, 90);
        screenshot();
      });
    });
