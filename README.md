# khanacademy_transcript
Quick and dirty script suite for curating khanacademy video transcripts

Usage
```
MODULE="Differential Calculus"
URL="https://www.khanacademy.org/math/early-math"
python download_video_ids.py ${MODULE} ${URL}
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
- [x] Save video ids using directory hierarchy
- [x] Auto detect subject(e.g. Math => Linear Algebra, Calculus ...)
- [x] Only download necessary tutorials
