# khanacademy_transcript
Quick and dirty suite of scripts for curating khanacademy video transcripts

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
- [ ] Auto detect subject(e.g. Math => Linear Algebra, Probability Theory, Calculus ...)
