configs({ directions: ['ltr'] }).forEach(({ title, screenshot, config }) => {
  test.describe(title('datetime: highlightedDates'), () => {
    test.beforeEach(async ({ page }) => {
      await page.setContent(
        `
        <ion-datetime value="2023-01-01" locale="en-US"></ion-datetime>
      `,
        config
      );
    });
