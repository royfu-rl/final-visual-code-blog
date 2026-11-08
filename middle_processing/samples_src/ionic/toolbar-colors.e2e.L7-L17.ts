configs({ directions: ['ltr'] }).forEach(({ title, screenshot, config }) => {
  test.describe(title('toolbar: colors'), () => {
    test('should not have visual regressions', async ({ page }) => {
      await page.goto(`/src/components/toolbar/test/colors`, config);

      await page.setIonViewport();

      await expect(page).toHaveScreenshot(screenshot(`toolbar-colors`));
    });
  });
});
