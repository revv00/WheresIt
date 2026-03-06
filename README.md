# WheresIt - AI Chat History Semantic Search

**WheresIt** is a lightweight, local-first tool for semantic searching through your AI chat histories (Gemini AI Studio, etc.). It enables you to find specific conversations based on meaning rather than just keywords, all while keeping your data private on your own machine.

---

## 📸 Screenshots

### UI Overview
![WheresIt UI Overview](./screenshots/ui_overview.png)

---

## 🚀 Quick Start

WheresIt is a single-file web application. You don't need to install anything—just open the HTML file in your browser and load your exported chat data.

### 1. Data Preparation: Export from Google AI Studio

Your chats are stored in Google Drive. To use them with WheresIt, you need to export them as JSON files.

#### **Method A: Manual Download (Easiest)**
1.  Go to [Google Drive](https://drive.google.com/) and navigate to the **"Google AI Studio"** folder in "My Drive".
2.  Select the chats you want to search:
    *   Click the first item, then **Shift+Click** the last item to select a range.
    *   Or use **Cmd+A** (Mac) / **Ctrl+A** (Windows) to select all.
3.  Right-click and select **"Download"**. 
    *   *Note: Google Drive may zip multiple files together. If so, unzip the downloaded file on your computer before loading them into WheresIt.*

#### **Method B: Automated Script (Advanced)**
If you have the [gog cli](https://github.com/revv00/gog) installed and configured, you can use the provided script to sync your chats locally:
```bash
./scripts/fetch_ai_studio_chats.sh
```
This will download and date-prefix your chats into a local directory.

### 2. Launching WheresIt

1.  **Open the App**: Locate [wheresit.html](file:///Volumes/data/dev/WheresIt/wheresit.html) on your machine and double-click it to open in any modern browser (Chrome, Edge, Safari, Firefox).
2.  **Import Data**:
    *   **Add Files**: Select individual `.json` files.
    *   **Add Folder**: Select an entire directory of chats. This is **highly recommended** as it preserves your folder hierarchy in the sidebar for better organization.
3.  **Search with AI**:
    *   Type a natural language query (e.g., *"How did I implement that React hook last week?"*).
    *   Click **"Find with AI"**.
    *   *First Run: The application will download the MiniLM semantic model (approx. 30MB) to your browser's local cache. This only happens once.*

### 3. Understanding Results
*   **Confidence Scores**: Each result shows a numerical score. Higher scores (closer to 0) indicate stronger semantic relevance.
*   **Folder Navigator**: The sidebar groups conversations based on their local folder structure, making it easy to filter by project or date if you've organized your exports.

---

## ✨ Key Features

- **Semantic Search**: Powered by `transformers.js` (MiniLM-L6-v2), allowing you to search by context and intent.
- **Privacy First**: Everything runs locally in your browser. No data is ever sent to a server.
- **Smart Grouping**: Automatically organizes your chats into folders based on your local directory structure.
- **Rich Rendering**: Full support for Markdown, LaTeX (math equations), and syntax highlighting for code blocks.
- **Visual Feedback**: Real-time progress bar during model download and scanning.

---

## 🛠️ How it Works

WheresIt uses **MiniLM-L6-v2**, a powerful cross-encoder model, to rank your conversations based on relevance to your search query. 

- **Local Execution**: The model is downloaded once to your browser's cache and performs all computations locally.
- **Hybrid Context**: The tool scans a context window from each chat to determine relevance, ensuring accurate matches even for long conversations.
- **Match Scores**: Results are ranked with a visual "confidence" score, making it easy to spot the best matches.

---

## 🔜 Roadmap

- [ ] **Qwen History Export**: A utility to convert Qwen chat exports into the Google AI Studio format compatible with WheresIt.
- [ ] **Performance Optimization**: Even faster scanning for very large libraries.
- [ ] **Saved Searches**: Bookmarking important filters or queries.

---

## ⚖️ License

MIT License. Feel free to use and modify for your own needs.
