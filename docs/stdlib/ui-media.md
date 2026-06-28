# UI & Media Workers

The **UI & Media** category contains optional extensions for Atlas applications that require graphical interfaces or rich media processing. While Atlas is heavily CLI-first, these workers allow Managers to boot full desktop applications.

---

## 1. UI Workers

### Window (`atlas.ui.window`)
**Purpose:** Creates and manages native OS application windows.
**Implemented Model:** `WindowModel`

**Public APIs:**
- `create(title: str, width: int, height: int) -> str` (Returns Window ID)
- `show(window_id: str) -> None`
- `close(window_id: str) -> None`
- `render(window_id: str, layout: dict) -> None`

### Dialogs (`atlas.ui.dialogs`)
**Purpose:** Triggers native OS modal dialogs (alerts, confirmations).
**Implemented Model:** `DialogModel`

**Public APIs:**
- `alert(title: str, message: str) -> None`
- `confirm(title: str, message: str) -> bool`

### File Picker (`atlas.ui.file_picker`)
**Purpose:** Opens the native OS file selection dialog.
**Implemented Model:** `FilePickerModel`

**Public APIs:**
- `open_file(allowed_extensions: list[str]) -> str` (Returns file path)
- `save_file(default_name: str) -> str`

### Other Proposed UI Workers
- **Theme:** Manages light/dark mode transitions and color palettes across the application.
- **Workspace:** Manages multiple windows or tabs within a complex application (like Atlas Studio).

---

## 2. Media Workers

### Image (`atlas.media.image`)
**Purpose:** Loads, resizes, and manipulates image data.
**Implemented Model:** `ImageModel`

**Public APIs:**
- `resize(image_bytes: bytes, width: int, height: int) -> bytes`
- `convert(image_bytes: bytes, format: str) -> bytes`

### Camera (`atlas.media.camera`)
**Purpose:** Captures still frames or video streams from attached webcams.
**Implemented Model:** `CameraModel`

**Public APIs:**
- `capture_frame() -> bytes`
- `start_stream(fps: int) -> None`
- `stop_stream() -> None`

### Audio & Video (`atlas.media.audio`, `atlas.media.video`)
**Purpose:** Plays and records audio/video files.

**Public APIs:**
- `play(file_path: str) -> None`
- `record(duration_seconds: int) -> bytes`

### Microphone (`atlas.media.microphone`)
**Purpose:** Streams raw audio data for processing (essential for voice-to-text AI workers).
