# HSD: A hierarchical singing annotation dataset

This repository provides a singing annotation dataset that records vocal information in pop songs. It mainly labels pitch, duration, lyric, onset, and offset of each musical note. Meanwhile, all the information is recorded in a hierarchical structure.

## Annotations

Two kind of annotations are offered: enhanced LRC and MIDI. The enhanced LRC annotations are recommended because the singing information is recorded in a hierarchical structure.

### enhanced LRC

The enhanced LRC files are in the "enhanced_lrc" folder. Each line in an enhanced LRC file records the vocal information of a music phrase. Each line is in the format:  
  
[phrase time tag]\<onset time tag>lyric pitch duration{offset time tag}\<onset time tag>lyric pitch duration{offset time tag}...\<onset time tag>lyric pitch duration{offset time tag}  
  
"read_enhanced_lyric.py" can be used to read the annotations.

### MIDI

The annotation MIDIs are also proviced in the "midi" folder.

## Label Initialization

## Manual Label Calibration

## Raw Audio
