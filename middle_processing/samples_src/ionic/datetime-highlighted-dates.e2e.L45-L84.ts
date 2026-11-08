    test('should render highlights correctly when using a callback', async ({ page }) => {
      const datetime = page.locator('ion-datetime');

      await datetime.evaluate((el: HTMLIonDatetimeElement) => {
        el.highlightedDates = (isoString) => {
          const date = new Date(isoString);
          const utcDay = date.getUTCDate();

          // ensure selected date style overrides highlight
          if (utcDay === 1) {
            return {
              textColor: '#b22222',
              backgroundColor: '#fa8072',
              border: '2px solid purple',
            };
          }

          if (utcDay % 5 === 0) {
            return {
              textColor: '#800080',
              backgroundColor: '#ffc0cb',
              border: '2px solid purple',
            };
          }

          if (utcDay % 3 === 0) {
            return {
              textColor: '#0000ff',
              backgroundColor: '#add8e6',
              border: '2px solid purple',
            };
          }

          return undefined;
        };
      });

      await page.waitForChanges();
      await expect(datetime).toHaveScreenshot(screenshot(`datetime-highlightedDates-callback`));
    });
