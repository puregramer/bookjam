# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BookJam is a DJMAX-style rhythm game with separate editor and player applications. Built using PixiJS v8 for rendering and Web Audio API for audio processing.

## Architecture

### File Structure
The project consists of three main HTML files plus a landing page:
- **`index.html`**: GitHub Pages landing page with navigation to editor/player
- **`rhythm-game-editor-auto.html`**: AUTO editor with BPM+Offset auto-detection (recommended)
- **`rhythm-game-player.html`**: Game player for playing created charts
- **`rhythm-game-editor-auto.html`**: Legacy editor (kept for reference)

Each file is self-contained with embedded CSS and JavaScript, allowing direct browser execution without build tools or servers.

### Multiple Editor Versions
The project has evolved through several editor iterations (see README.md for full history):
- **AUTO editor** (rhythm-game-editor-auto.html): Latest, with automatic BPM/offset detection and frequency-based lane mapping
- **FINAL editor**: BPM grid-based with manual control
- **Pro v2 editor**: Improved beat detection with sensitivity controls
- **Pro editor**: Advanced charting with Beat Snap Divisor support

Users should start with the AUTO editor for easiest experience.

### Core Technologies
- **PixiJS v8.12.0**: 2D WebGL rendering engine (loaded via CDN)
- **Web Audio API**: Audio playback, decoding, and BPM detection
- **Vanilla JavaScript**: No framework dependencies

### Key Components

#### Game State (`gameState` object)
Centralized state management tracking:
- Score, combo, health, and judgment statistics
- Audio context and buffer references
- Note collection and timing
- BPM and difficulty settings

#### Lane System (`LANES` array)
5-lane configuration matching keyboard layout (D, F, Space, J, K). Each lane has:
- Key mapping
- Color (hex value)
- Label for display

Reduced from 7 lanes to 5 for easier gameplay and better accessibility.

#### Judgment System (`JUDGMENT` object)
Timing windows for hit accuracy:
- PERFECT: ±50ms (100 points)
- GREAT: ±100ms (70 points)
- GOOD: ±150ms (40 points)
- MISS: ±200ms (0 points, health penalty)

#### Responsive Dimension System
`calculateDimensions()` function dynamically computes game dimensions based on viewport:
- Game width (max 1200px)
- Lane width (divided by 5 lanes)
- Note height and speed (scaled to screen height)
- Touch button height (15% of screen height)
- Judgment line position

### Audio Processing Pipeline

1. **File Loading**: User selects MP3 file via file input or drag-and-drop
2. **Decoding**: Web Audio API `decodeAudioData()` converts to audio buffer
3. **BPM Detection** (AUTO editor):
   - OfflineAudioContext processes audio through lowpass filter (150Hz)
   - Peak detection identifies beats (threshold: 0.9, min distance: 200ms)
   - Average interval calculation determines BPM (60 / avgInterval)
   - BPM range: 60-240 BPM
4. **Offset Detection** (AUTO editor):
   - First significant beat time becomes offset
   - Used to align note grid with actual music beats
5. **Note Generation**:
   - **Multi-band Onset Detection**: Splits audio into 3 frequency bands (kick: 20-150Hz, snare: 150-4kHz, hi-hat: 4-20kHz)
   - **Spectral Flux**: Calculates energy changes to detect note onsets
   - **Adaptive Thresholding**: Local average-based peak detection
   - **Lane Mapping**: Frequency band determines lane assignment (kick→left, snare→center, hi-hat→right)
   - **Beat Grid Snapping**: Aligns detected onsets to BPM grid for consistency
6. **Playback**: BufferSource plays audio with precise timing for note synchronization

For detailed algorithm documentation, see BEAT_DETECTION.md and NOTE_GENERATION.md.

### PixiJS Rendering Architecture

Four container layers (render order):
1. `gameContainer`: Background lanes and judgment line
2. `notesContainer`: Falling note sprites
3. `particleContainer`: Hit effect particles
4. `uiContainer`: Score, combo, health, accuracy displays

### Input System

Dual input support:
- **Keyboard**: Event listeners for D/F/Space/J/K keys (5 lanes)
- **Touch/Mouse**: DOM elements positioned at screen bottom for each lane

Both systems trigger the same `handleKeyPress(laneIndex)` function for consistent gameplay.

### Editor-Specific Input
- Keys add notes at current playback time
- Delete key removes last added note
- Space bar toggles play/pause (when not in input field)

### Note Lifecycle

1. **Generation**: `generateNotes()` creates note objects with `time` and `lane` properties
2. **Spawning**: Game loop creates PixiJS Graphics when note enters viewport
3. **Movement**: Position updated each frame based on `NOTE_SPEED` and current audio time
4. **Hit Detection**: `handleKeyPress()` finds closest note within timing window
5. **Cleanup**: Sprites removed from container after hit or miss

## Common Issues and Solutions

### PixiJS Graphics API
- **Do not use** Canvas API methods like `context.createLinearGradient()` on PixiJS Graphics objects
- Use PixiJS's fill/stroke API with layered rectangles for gradient effects
- PixiJS v8 requires `new PIXI.Graphics()` before drawing operations

### Audio Context
- Must be created after user interaction (browser autoplay policy)
- Use `audioContext.currentTime` for precise timing, not `Date.now()`
- Remember to stop audio source before page unload

### Touch Events
- Set `touch-action: none` on body to prevent scroll interference
- Use `{ passive: false }` on touch event listeners to call `preventDefault()`
- Touch buttons must be DOM elements, not PixiJS sprites, for reliable touch detection

### Responsive Design
- All dimensions calculated dynamically in `calculateDimensions()`
- Call this function on window resize (but not during active gameplay)
- Use `clamp()` CSS function for responsive typography

## Development Workflow

### Quick Start (Recommended)
1. Open `index.html` in browser or visit GitHub Pages: https://puregramer.github.io/bookjam/
2. Click "Chart Editor" to create charts or "Game Player" to play existing ones

### Editor AUTO Workflow (Easiest)
1. Open `rhythm-game-editor-auto.html` in browser
2. Select difficulty (Easy/Normal/Hard/Expert) before loading audio
3. Load MP3 audio file
4. Wait for automatic analysis (BPM + Offset + Note generation)
5. Review generated notes with beat grid visualization
6. Adjust BPM/Offset if needed (notes regenerate automatically)
7. Manually add/remove notes during playback (D, F, Space, J, K keys)
8. Save as JSON chart file

```bash
open rhythm-game-editor-auto.html
```

### Editor FINAL Workflow (Manual Control)
1. Open rhythm-game-editor-final.html
2. Load MP3 file
3. Manually input BPM (required!)
4. Set offset if needed (default: 0)
5. Choose generation mode (Simple/Kick Only/Kick+Snare/Full Drums)
6. Adjust density slider (10-100%)
7. Click "Auto Generate"
8. Save chart

### Testing Local Files
```bash
# Open editor
open rhythm-game-editor-auto.html

# Open player
open rhythm-game-player.html

# Open landing page
open index.html
```

### Player Workflow
1. Open `rhythm-game-player.html` in browser
2. Load chart JSON file (created from editor)
3. Load same MP3 file used in editor
4. Start game and play

```bash
open rhythm-game-player.html
```

### Testing Legacy Version
Open `rhythm-game.html` for all-in-one version with auto-generation:
```bash
open rhythm-game.html
```

### Chart File Format
JSON structure for saved charts:
```json
{
  "title": "Song Title",
  "bpm": 120,
  "offset": 0.123,
  "difficulty": "Hard",
  "duration": 180.5,
  "lanes": 5,
  "notes": [
    { "time": 1.0, "lane": 0 },
    { "time": 1.5, "lane": 2 }
  ],
  "metadata": {
    "nps": "3.50",
    "noteCount": 630,
    "createdAt": "2025-10-28T...",
    "editor": "BEAT MASTER Auto"
  }
}
```

- `title`: Song title
- `bpm`: Beats per minute
- `offset`: First beat offset in seconds (auto-detected in AUTO editor)
- `difficulty`: Easy/Normal/Hard/Expert
- `duration`: Song length in seconds
- `lanes`: Number of lanes (always 5)
- `notes`: Array of note objects
  - `time`: When note reaches judgment line (seconds, includes offset)
  - `lane`: Lane index 0-4 (D, F, Space, J, K)
- `metadata`: Additional chart information
  - `nps`: Notes per second (difficulty metric)
  - `noteCount`: Total number of notes
  - `editor`: Which editor was used
  - `createdAt`: ISO timestamp

**Important**: The player automatically loads the offset from the chart file for perfect timing synchronization.

### Debugging
Check browser console (F12) for:
- Audio loading errors
- PixiJS initialization issues
- Note generation statistics:
  - Total beats detected
  - Frequency band distribution (kick/snare/hi-hat counts)
  - Final note count
  - NPS (Notes Per Second)
- Chart file validation errors
- BPM detection results
- Offset values

**Common Console Messages (AUTO editor)**:
```
🎵 Audio loaded: 3:24 duration
🎯 BPM detected: 135 BPM
📍 Offset: 0.234s
🎼 Generating notes for difficulty: Hard
✅ Total beats: 487
   - Kick: 145 (low frequency)
   - Snare: 198 (mid frequency)
   - Hi-hat: 144 (high frequency)
📊 Generated 631 notes (NPS: 3.12)
```

## Design System

### Visual Theme
- **Style**: Dark cyberpunk with glassmorphism
- **Colors**: Purple/blue gradients (#667eea, #764ba2, #f093fb)
- **Typography**: Orbitron (English), Noto Sans KR (Korean)
- **Effects**: Backdrop blur, neon glow, particle systems

### Mobile Optimization
- Viewport meta tag prevents zoom/scale
- Touch buttons sized at 15% screen height minimum
- All UI elements use responsive `clamp()` sizing
- Maximum game width of 1200px on large screens

## Chart Design Philosophy

When creating or modifying charts, follow these principles from CHARTING_METHODOLOGY.md:

### Core Principles
1. **Musicality**: Notes should reflect actual sounds in the music (drums, melody, vocals)
2. **Playability**: Hand movements should feel natural and comfortable
3. **Readability**: Players should be able to see and react to notes clearly

### Lane Assignment Strategy
- **Lanes 0-1 (D, F)**: Kick drum and bass (low frequency, 20-150Hz)
- **Lane 2 (Space)**: Melody, vocals, important accents (center focus)
- **Lanes 3-4 (J, K)**: Snare, hi-hat, cymbals (mid-high frequency, 150Hz+)

### Difficulty Guidelines
- **Easy**: 1-2 NPS, single notes only, 1/1 or 1/2 beat divisions
- **Normal**: 2-4 NPS, occasional 2-note chords, 1/2 and 1/4 beats
- **Hard**: 4-6 NPS, frequent chords, 1/4 and occasional 1/8 beats
- **Expert**: 6-10+ NPS, complex patterns, 1/8 and 1/16 beats

### Pattern Types
- **Single Notes**: Basic taps for individual sounds
- **Chords**: 2-3 simultaneous notes for accents or multiple instruments
- **Streams**: Fast consecutive notes (1/8 or 1/16 divisions)
- **Jacks**: Same lane repeated (use sparingly, physically demanding)

### BPM and Timing
- Use `audioContext.currentTime` for precise timing, not `Date.now()`
- Beat interval formula: `60 / BPM` seconds
- Common BPM ranges:
  - Ballad: 60-80
  - Pop: 100-130
  - Dance/EDM: 120-150
  - Drum & Bass: 160-180+

For comprehensive charting guidelines, see CHARTING_METHODOLOGY.md (1800+ lines of detailed methodology).
