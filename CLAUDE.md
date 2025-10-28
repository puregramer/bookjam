# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BookJam is a DJMAX-style rhythm game with separate editor and player applications. Built using PixiJS v8 for rendering and Web Audio API for audio processing.

## Architecture

### File Structure
The project consists of three main HTML files:
- **`rhythm-game-editor.html`**: Chart editor for creating and editing note patterns
- **`rhythm-game-player.html`**: Game player for playing created charts
- **`rhythm-game.html`**: Legacy all-in-one version with auto-generation

Each file is self-contained with embedded CSS and JavaScript, allowing direct browser execution without build tools or servers.

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
3. **BPM Detection**:
   - OfflineAudioContext processes audio through lowpass filter (150Hz)
   - Peak detection identifies beats
   - Average interval calculation determines BPM
4. **Note Generation**: Creates note objects based on BPM and difficulty multiplier
5. **Playback**: BufferSource plays audio with precise timing for note synchronization

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

### Editor Workflow
1. Open `rhythm-game-editor.html` in browser
2. Load MP3 audio file
3. Set BPM (or use auto-detect)
4. Play audio and press keys (D, F, Space, J, K) to add notes at current time
5. Save as JSON chart file

```bash
open rhythm-game-editor.html
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
  "duration": 180.5,
  "lanes": 5,
  "notes": [
    { "time": 1.0, "lane": 0 },
    { "time": 1.5, "lane": 2 }
  ],
  "createdAt": "2025-10-28T..."
}
```

- `time`: When note reaches judgment line (seconds)
- `lane`: Lane index 0-4 (D, F, Space, J, K)

### Debugging
Check browser console for:
- Audio loading errors
- PixiJS initialization issues
- Note generation statistics (notes array length)
- Chart file validation errors

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
