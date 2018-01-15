# khanacademy_transcript
Quick and dirty script suite for curating khanacademy video transcripts

Usage
```
python download_video_ids.py
python download_transcripts.py
python parse_transcripts.py
```

Requirements
```
requests
```

TODO
- [x] Refactor `parse_transcripts.py`
- [x] Abstract file containing video ids
- [ ] Save video ids using directory hierarchy
- [ ] Auto detect subject(e.g. Math => Linear Algebra, Calculus ...)
