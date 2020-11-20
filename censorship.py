from typing import List, Tuple
from datetime import datetime
from pydub import AudioSegment
from pydub.playback import play

bleep = AudioSegment.from_file('./bleep.wav', format="wav")[0]


def play_audio_file(fpath: str) -> None:
    """ 
      a helper function which plays the wav file at the given path.
    """
    play(AudioSegment.from_file(fpath, format="wav"))


def censor(fpath: str, snippets: List[Tuple[int, int]]) -> str:
    """ 
      takes a file path for a wav file to censor, and a list
      of ms timestamp pairs representing segments to bleep
      out. returns a file path for the censored audio file.

      start time is inclusive, end time is exclusive, so if you
      need to censor the final millisecond, that end timestamp is
      just the length of the audio in milliseconds. it seems like
      pydub will politely ignore the discrepancy if you pass a value
      greater than the ms length of the recording.
    """

    wav = AudioSegment.from_file(fpath, format="wav")
    newwav = AudioSegment(
        data=b'',
        sample_width=wav.sample_width,
        frame_rate=wav.frame_rate,
        channels=wav.channels
    )

    # iterate over a list of ms timestamp 3-tuples containing
    # the end of the previous snippet, the beginning of the
    # current snippet, and the end of the current snippet. the
    # end of the previous snippet prior to the first snippet in
    # the list is assumed to be the very start of the recording.
    for prev_end, cur_begin, cur_end in [
        (s[0], s[1][0], s[1][1]) for s in
            zip([0] + [snip[1] for snip in snippets[:-1]], snippets)]:

        # no shenanigans
        if prev_end > cur_begin or cur_begin > cur_end:
            break

        newwav = newwav.append(wav[prev_end:cur_begin-1], crossfade=0)
        newwav = newwav.append(
            bleep * min(len(wav) - cur_begin, cur_end - cur_begin - 1), crossfade=0)

        # again, no shenanigans
        if cur_end >= len(wav):
            break

    newwav = newwav.append(wav[cur_end:len(wav)], crossfade=0)

    newpath = f"./censored_{''.join(fpath)}.wav"
    newwav.export(newpath, format="wav")
    return newpath
