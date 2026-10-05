# Blind Listening Test Generator

A small Python tool for running fair, blind listening tests on different versions of a mix.

## Why this exists

Louder versions almost always sound better to listeners. If you compare two mixes at different levels, you are testing loudness, not quality. This tool removes that bias: it measures each version's integrated loudness (LUFS), matches them, hides the filenames behind random labels, logs your scores, and only reveals which version is which at the end.

## How it works

1. **prepare.py** loads every WAV in `versions/`, measures loudness with pyloudnorm (ITU-R BS.1770), turns every version down to match the quietest one (so nothing can clip), shuffles them, and saves them as `A.wav`, `B.wav`, `C.wav` in `output/`. The answer key is saved to `key.json`.
2. **score.py** asks for a 1-5 score and an optional comment for each label and appends them to `results.csv`.
3. **reveal.py** joins your scores to the key and prints the average score per version, ranked best to worst.

## Usage

    pip install -r requirements.txt
    # put your WAV files in versions/
    python prepare.py
    # listen to output/A.wav, B.wav, C.wav
    python score.py
    python reveal.py

Do not open `key.json` until you have finished scoring. Running `prepare.py` again reshuffles the labels and overwrites the key.

## Example run

Three versions of the same 48-second stereo clip: unfiltered, low-pass and high-pass. Original loudness was -7.3, -11.1 and -15.5 LUFS, so all three were matched to -15.5 LUFS before listening.

| Version | Score | Comment |
|---|---|---|
| Normal (unfiltered) | 5 | no comment |
| High-pass | 2 | piercing |
| Low-pass | 1 | extremely muddy |

The blind descriptions matched what the filters actually do: removing highs sounds muddy, removing lows leaves the top end sharp and thin.

## Design choices

- **Match to the quietest file, turn down only.** Raising quieter files could push peaks past full scale and add clipping, which would give the version away.
- **Random shuffle with a separate key file.** The listener cannot tell which version is which until the reveal.
- **Separate scripts.** Scoring and revealing never reshuffle the labels.

## Limitations

- One listener and one rating per version, so results show a pattern, not statistical significance.
- Scripts assume all versions share the same sample rate, length and channel count, and do not check this.
- Simple 1-5 scoring, not a full MUSHRA or ABX protocol.

## Possible next steps

- MUSHRA-style test with a hidden reference and a low-pass anchor
- Repeat trials and multiple listeners
- Apply the same method to AI model outputs, such as source separation results

Built in Python with soundfile, pyloudnorm and numpy.
