# Privacy Policy for TCG Game Planner

**Last Updated:** October 27, 2026

Your privacy is a core principle in the design and development of **TCG Game Planner** ("the App"). This Privacy Policy outlines our commitment to transparency regarding how your data is handled.

---

## 1. Zero Personal Data Collection

**TCG Game Planner does not collect, transmit, sell, or monetize any of your personal information.**

- **No User Accounts:** You do not need an email, phone number, or account to use any feature of the App.
- **No Third-Party Analytics or Advertising:** We do not embed third-party advertising frameworks, tracking cookies, or commercial telemetry SDKs.
- **Local Storage:** All decks, card collection inventories, tournament match histories, and custom sideboard plans are stored locally on your device in a private SQLite database (`db.sqlite`).

---

## 2. Network Connections & Third-Party APIs

The App makes internet connections exclusively to fulfill functionality requested by you:

- **Scryfall API:** When searching for cards, viewing artwork, or updating card market prices, the App connects to the public Scryfall API (`api.scryfall.com`). Scryfall processes these queries according to their public API terms. No personal identification or user credentials are sent in these requests.
- **Cached Imagery:** Downloaded card images are cached locally on your device so that you can view your decks offline.

---

## 3. iCloud Sync & Backups

If you choose to use iCloud backup or sync features:
- Your database backups are stored directly in your personal Apple iCloud Drive container.
- We have no access to your iCloud account, your encryption keys, or your stored backup files. Apple manages all transmission and storage security according to Apple's Privacy Policy.

---

## 4. On-Device Speech Recognition & Photos

- **Photo Library / Camera:** If you grant permission, the App accesses your camera or photo library solely to attach custom photos to altered or physical cards. Photos never leave your device.
- **Microphone & Speech:** If you grant permission to use voice dictation for notes, speech-to-text processing occurs directly on your Apple device using Apple's built-in Speech framework.

---

## 5. Children's Privacy

The App does not knowingly collect or solicit any personal information from children under the age of 13.

---

## 6. Contact & Support

If you have questions, feedback, or inquiries regarding this Privacy Policy, please open an issue on our public GitHub repository:

- **GitHub Issues:** [https://github.com/brunobotelhobr/tcg-game-planner/issues](https://github.com/brunobotelhobr/tcg-game-planner/issues)
- **Repository:** [https://github.com/brunobotelhobr/tcg-game-planner](https://github.com/brunobotelhobr/tcg-game-planner)
