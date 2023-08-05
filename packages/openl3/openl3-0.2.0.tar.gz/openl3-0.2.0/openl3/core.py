import os
import resampy
import traceback
import soundfile as sf
import numpy as np
from numbers import Real
import warnings
import keras
from .models import load_embedding_model
from .openl3_exceptions import OpenL3Error
from .openl3_warnings import OpenL3Warning


TARGET_SR = 48000


def _center_audio(audio, frame_len):
    """Center audio so that first sample will occur in the middle of the first frame"""
    return np.pad(audio, (int(frame_len / 2.0), 0), mode='constant', constant_values=0)


def _pad_audio(audio, frame_len, hop_len):
    """Pad audio if necessary so that all samples are processed"""
    audio_len = audio.size
    if audio_len < frame_len:
        pad_length = frame_len - audio_len
    else:
        pad_length = int(np.ceil((audio_len - frame_len)/float(hop_len))) * hop_len \
                     - (audio_len - frame_len)

    if pad_length > 0:
        audio = np.pad(audio, (0, pad_length), mode='constant', constant_values=0)

    return audio


def get_embedding(audio, sr, model=None, input_repr="mel256",
                  content_type="music", embedding_size=6144,
                  center=True, hop_size=0.1, verbose=1):
    """
    Computes and returns L3 embedding for given audio data

    Parameters
    ----------
    audio : np.ndarray [shape=(N,) or (N,C)]
        1D numpy array of audio data.
    sr : int
        Sampling rate, if not 48kHz will audio will be resampled.
    model : keras.models.Model or None
        Loaded model object. If a model is provided, then `input_repr`,
        `content_type`, and `embedding_size` will be ignored.
        If None is provided, the model will be loaded using
        the provided values of `input_repr`, `content_type` and
        `embedding_size`.
    input_repr : "linear", "mel128", or "mel256"
        Spectrogram representation used for model. Ignored if `model` is
        a valid Keras model.
    content_type : "music" or "env"
        Type of content used to train embedding. Ignored if `model` is
        a valid Keras model.
    embedding_size : 6144 or 512
        Embedding dimensionality. Ignored if `model` is a valid
        Keras model.
    center : boolean
        If True, pads beginning of signal so timestamps correspond
        to center of window.
    hop_size : float
        Hop size in seconds.
    verbose : 0 or 1
        Keras verbosity.

    Returns
    -------
        embedding : np.ndarray [shape=(T, D)]
            Array of embeddings for each window.
        timestamps : np.ndarray [shape=(T,)]
            Array of timestamps corresponding to each embedding in the output.

    """
    if audio.size == 0:
        raise OpenL3Error('Got empty audio')

    # Warn user if audio is all zero
    if np.all(audio == 0):
        warnings.warn('Provided audio is all zeros', OpenL3Warning)

    if model is not None and not isinstance(model, keras.models.Model):
        raise OpenL3Error('Invalid model provided. Must be of type keras.model.Models'
                          ' but got {}'.format(str(type(model))))

    if str(input_repr) not in ("linear", "mel128", "mel256"):
        raise OpenL3Error('Invalid input representation "{}"'.format(input_repr))

    if str(content_type) not in ("music", "env"):
        raise OpenL3Error('Invalid content type "{}"'.format(content_type))

    if embedding_size not in (6144, 512):
        raise OpenL3Error('Invalid content type "{}"'.format(embedding_size))

    if not isinstance(hop_size, Real) or hop_size <= 0:
        raise OpenL3Error('Invalid hop size {}'.format(hop_size))

    if verbose not in (0, 1):
        raise OpenL3Error('Invalid verbosity level {}'.format(verbose))

    if center not in (True, False):
        raise OpenL3Error('Invalid center value {}'.format(center))

    # Check audio array dimension
    if audio.ndim > 2:
        raise OpenL3Error('Audio array can only be be 1D or 2D')
    elif audio.ndim == 2:
        # Downmix if multichannel
        audio = np.mean(audio, axis=1)

    # Resample if necessary
    if sr != TARGET_SR:
        audio = resampy.resample(audio, sr_orig=sr, sr_new=TARGET_SR, filter='kaiser_best')

    # Get embedding model
    if model is None:
        model = load_embedding_model(input_repr, content_type, embedding_size)

    audio_len = audio.size
    frame_len = TARGET_SR
    hop_len = int(hop_size * TARGET_SR)

    if audio_len < frame_len:
        warnings.warn('Duration of provided audio is shorter than window size (1 second). Audio will be padded.',
                      OpenL3Warning)

    if center:
        # Center audio
        audio = _center_audio(audio, frame_len)

    # Pad if necessary to ensure that we process all samples
    audio = _pad_audio(audio, frame_len, hop_len)

    # Split audio into frames, copied from librosa.util.frame
    n_frames = 1 + int((len(audio) - frame_len) / float(hop_len))
    x = np.lib.stride_tricks.as_strided(audio, shape=(frame_len, n_frames),
        strides=(audio.itemsize, hop_len * audio.itemsize)).T

    # Add a channel dimension
    x = x.reshape((x.shape[0], 1, x.shape[-1]))

    # Get embedding and timestamps
    embedding = model.predict(x, verbose=verbose)

    ts = np.arange(embedding.shape[0]) * hop_size

    return embedding, ts


def process_file(filepath, output_dir=None, suffix=None, model=None,
                 input_repr="mel256", content_type="music",
                 embedding_size=6144, center=True, hop_size=0.1, verbose=True):
    """
    Computes and saves L3 embedding for given audio file

    Parameters
    ----------
    filepath : str
        Path to WAV file to be processed.
    output_dir : str or None
        Path to directory for saving output files. If None, output files will
        be saved to the directory containing the input file.
    suffix : str or None
        String to be appended to the output filename, i.e. <base filename>_<suffix>.npz.
        If None, then no suffix will be added, i.e. <base filename>.npz.
    model : keras.models.Model or None
        Loaded model object. If a model is provided, then `input_repr`,
        `content_type`, and `embedding_size` will be ignored.
        If None is provided, the model will be loaded using
        the provided values of `input_repr`, `content_type` and
        `embedding_size`.
    input_repr : "linear", "mel128", or "mel256"
        Spectrogram representation used for model. Ignored if `model` is
        a valid Keras model.
    content_type : "music" or "env"
        Type of content used to train embedding. Ignored if `model` is
        a valid Keras model.
    embedding_size : 6144 or 512
        Embedding dimensionality. Ignored if `model` is a valid
        Keras model.
    center : boolean
        If True, pads beginning of signal so timestamps correspond
        to center of window.
    hop_size : float
        Hop size in seconds.
    verbose : 0 or 1
        Keras verbosity.

    Returns
    -------

    """
    if not os.path.exists(filepath):
        raise OpenL3Error('File "{}" could not be found.'.format(filepath))

    try:
        audio, sr = sf.read(filepath)
    except Exception:
        raise OpenL3Error('Could not open file "{}":\n{}'.format(filepath, traceback.format_exc()))

    if not suffix:
        suffix = ""

    output_path = get_output_path(filepath, suffix + ".npz", output_dir=output_dir)

    embedding, ts = get_embedding(audio, sr, model=model, input_repr=input_repr,
                                  content_type=content_type,
                                  embedding_size=embedding_size, center=center,
                                  hop_size=hop_size, verbose=1 if verbose else 0)

    np.savez(output_path, embedding=embedding, timestamps=ts)
    assert os.path.exists(output_path)


def get_output_path(filepath, suffix, output_dir=None):
    """

    Parameters
    ----------
    filepath : str
        Path to audio file to be processed
    suffix : str
        String to append to filename (including extension)
    output_dir : str or None
        Path to directory where file will be saved. If None, will use directory of given filepath.

    Returns
    -------
    output_path : str
        Path to output file

    """
    base_filename = os.path.splitext(os.path.basename(filepath))[0]
    if not output_dir:
        output_dir = os.path.dirname(filepath)

    if suffix[0] != '.':
        output_filename = "{}_{}".format(base_filename, suffix)
    else:
        output_filename = base_filename + suffix

    return os.path.join(output_dir, output_filename)
