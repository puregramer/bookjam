#!/usr/bin/env python3
"""
Analyze note density patterns to identify song structure (Verse, Chorus, Bridge, etc.)
"""

import json
import sys
from collections import defaultdict

def analyze_note_density(notes, window_size=4.0):
    """Analyze note density over time to identify song sections"""
    if not notes:
        return []

    # Get time range
    max_time = max(note['time'] for note in notes)

    # Calculate note density in windows
    densities = []
    current_time = 0

    while current_time < max_time:
        window_end = current_time + window_size
        notes_in_window = [n for n in notes if current_time <= n['time'] < window_end]
        density = len(notes_in_window)
        densities.append({
            'start': current_time,
            'end': window_end,
            'density': density,
            'notes_per_second': density / window_size
        })
        current_time += window_size

    return densities

def identify_sections(densities, duration):
    """Identify likely song sections based on density patterns"""
    if not densities:
        return []

    # Calculate average density
    avg_density = sum(d['density'] for d in densities) / len(densities)

    sections = []
    current_section = None

    for d in densities:
        # Classify based on density
        if d['density'] < avg_density * 0.5:
            section_type = 'intro/outro/break'
        elif d['density'] < avg_density * 0.85:
            section_type = 'verse'
        elif d['density'] < avg_density * 1.3:
            section_type = 'pre-chorus/bridge'
        else:
            section_type = 'chorus'

        # Group consecutive similar sections
        if current_section and current_section['type'] == section_type:
            current_section['end'] = d['end']
            current_section['avg_nps'] = (current_section['avg_nps'] + d['notes_per_second']) / 2
        else:
            if current_section:
                sections.append(current_section)
            current_section = {
                'type': section_type,
                'start': d['start'],
                'end': d['end'],
                'avg_nps': d['notes_per_second']
            }

    if current_section:
        sections.append(current_section)

    return sections

def suggest_lyrics_timing(sections, lyrics_structure):
    """Suggest timing for lyrics based on identified sections"""
    suggestions = []

    # Define expected structure
    expected_structure = {
        'intro': 0,
        'verse1': 1,
        'verse2': 2,
        'chorus1': 3,
        'bridge': 4,
        'chorus2': 5,
        'outro': 6
    }

    # Try to map sections to song structure
    verse_sections = [s for s in sections if 'verse' in s['type'].lower()]
    chorus_sections = [s for s in sections if 'chorus' in s['type'].lower()]
    bridge_sections = [s for s in sections if 'bridge' in s['type'].lower()]
    intro_outro = [s for s in sections if 'intro' in s['type'].lower() or 'outro' in s['type'].lower()]

    print("\n=== SONG STRUCTURE ANALYSIS ===\n")
    print(f"Total Duration: {sections[-1]['end']:.1f} seconds\n")

    print("Detected Sections:")
    for i, section in enumerate(sections):
        print(f"  {i+1}. {section['start']:.1f}s - {section['end']:.1f}s: {section['type']} (NPS: {section['avg_nps']:.2f})")

    print("\n=== SUGGESTED LYRICS TIMING ===\n")

    # Intro (usually first low-density section)
    if intro_outro and intro_outro[0]['start'] < 10:
        intro = intro_outro[0]
        print(f"Intro: {intro['start']:.1f}s - {intro['end']:.1f}s")
        suggestions.append({
            'section': 'intro',
            'start': intro['start'],
            'end': intro['end']
        })

    # Verse 1 (first verse-like section after intro)
    if verse_sections:
        verse1 = verse_sections[0]
        print(f"Verse 1: {verse1['start']:.1f}s - {verse1['end']:.1f}s")
        suggestions.append({
            'section': 'verse1',
            'start': verse1['start'],
            'end': verse1['end']
        })

    # Verse 2 (second verse-like section)
    if len(verse_sections) > 1:
        verse2 = verse_sections[1]
        print(f"Verse 2: {verse2['start']:.1f}s - {verse2['end']:.1f}s")
        suggestions.append({
            'section': 'verse2',
            'start': verse2['start'],
            'end': verse2['end']
        })

    # Chorus 1 (first high-density section)
    if chorus_sections:
        chorus1 = chorus_sections[0]
        print(f"Chorus 1: {chorus1['start']:.1f}s - {chorus1['end']:.1f}s")
        suggestions.append({
            'section': 'chorus1',
            'start': chorus1['start'],
            'end': chorus1['end']
        })

    # Bridge (middle section, often different pattern)
    if bridge_sections:
        bridge = bridge_sections[0]
        print(f"Bridge: {bridge['start']:.1f}s - {bridge['end']:.1f}s")
        suggestions.append({
            'section': 'bridge',
            'start': bridge['start'],
            'end': bridge['end']
        })

    # Chorus 2 (second high-density section)
    if len(chorus_sections) > 1:
        chorus2 = chorus_sections[1]
        print(f"Chorus 2: {chorus2['start']:.1f}s - {chorus2['end']:.1f}s")
        suggestions.append({
            'section': 'chorus2',
            'start': chorus2['start'],
            'end': chorus2['end']
        })

    # Outro (last low-density section)
    if len(intro_outro) > 1:
        outro = intro_outro[-1]
        print(f"Outro: {outro['start']:.1f}s - {outro['end']:.1f}s")
        suggestions.append({
            'section': 'outro',
            'start': outro['start'],
            'end': outro['end']
        })
    elif sections[-1]['type'] == 'intro/outro/break':
        outro = sections[-1]
        print(f"Outro: {outro['start']:.1f}s - {outro['end']:.1f}s")
        suggestions.append({
            'section': 'outro',
            'start': outro['start'],
            'end': outro['end']
        })

    return suggestions

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_audio_structure.py <chart.json>")
        sys.exit(1)

    # Load chart data
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        chart = json.load(f)

    notes = chart.get('notes', [])
    duration = chart.get('duration', 0)
    bpm = chart.get('bpm', 120)

    print(f"Chart: {chart.get('title', 'Unknown')}")
    print(f"BPM: {bpm}")
    print(f"Duration: {duration:.1f}s")
    print(f"Total Notes: {len(notes)}")
    print(f"Average NPS: {len(notes) / duration:.2f}\n")

    # Analyze note density
    densities = analyze_note_density(notes, window_size=4.0)

    # Identify sections
    sections = identify_sections(densities, duration)

    # Suggest lyrics timing
    suggestions = suggest_lyrics_timing(sections, {})

    print("\n=== COPY THIS STRUCTURE ===\n")
    for suggestion in suggestions:
        print(f"{suggestion['section']}: {suggestion['start']:.1f}s ~ {suggestion['end']:.1f}s")

if __name__ == '__main__':
    main()
