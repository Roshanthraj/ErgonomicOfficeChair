# TODO: Enable CSV Export for Posture Reports in Web App

## Tasks

- [x] Edit `docs/web-app/script.js`:
  - [x] Add `postureTime` and `lastStatus` properties to PostureDetector constructor.
  - [x] Modify `updateStats` method to track postureTime (increment on same status, reset on change).
  - [x] Update `drawResults` method: Change dataPoint field names to match example and add `posture_time`.
  - [x] Add `exportToCSV` method to PostureDetector class.
  - [x] Update `setupEventListeners` to handle export button click.
- [x] Edit `docs/web-app/index.html`:
  - [x] Add export CSV button in controls section.
- [ ] Test the web app locally:
  - [ ] Start local server for docs/web-app/.
  - [ ] Launch browser and navigate to localhost.
  - [ ] Start camera, collect some posture data.
  - [ ] Click Export CSV button and verify download.
  - [ ] Check CSV file for correct data fields.
