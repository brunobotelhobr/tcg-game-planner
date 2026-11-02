# TCG Game Planner — website and support

The public website and issue tracker for **TCG Game Planner**, a free app for Magic: The Gathering players on iPhone, iPad and Mac. This repository holds the website and the issue tracker.

- Website: https://brunobotelhobr.github.io/tcg-game-planner/
- Get help or report a bug: https://brunobotelhobr.github.io/tcg-game-planner/support/
- Privacy Policy: https://brunobotelhobr.github.io/tcg-game-planner/privacy/

## Editing the site

Pages are fragments in `src/pages/`, wrapped in `src/layout.html` by `build.py` (Python 3, standard library only). The built site goes to `docs/`, which GitHub Pages serves (Settings › Pages › branch `main`, folder `/docs`).

```bash
python3 build.py
```

Commit `src/` and `docs/` together. The design guide and the plan behind the site are in the app's own repository (`website.md`).

## Release day

In `build.py`, set `APP_STORE_URL` and `APP_STORE_ID`, rebuild, and every page switches from "Coming soon" to the store link and adds the Smart App Banner.

---

TCG Game Planner is unofficial Fan Content permitted under the Fan Content Policy. Not approved/endorsed by Wizards. Portions of the materials used are property of Wizards of the Coast. ©Wizards of the Coast LLC.
