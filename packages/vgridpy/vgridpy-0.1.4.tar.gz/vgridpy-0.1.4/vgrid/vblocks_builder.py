"""Utilities for building VGrid inputs from Rekall interval sets

VGrid displays a list of VBlocks. Each VBlock can have multiple tracks, and
each track shows a timeline of intervals in that track, as well as drawing
objects and showing metadata of the interval as configured.

There are two main use cases of VGrid:
    1. VideoVBlocks. This mode displays a VBlock for each video. Each track
        in the VBlock is an IntervalSet to visualize in that video.
    2. IntervalVBlocks. This mode displays a VBlock for each interval/clip.
        Each track in the VBlock is an IntervalSet to visualize in that
        interval/clip.

The VBlocksBuilders in this module helps building the JSON structure for this
list of VBlocks.

Example of using VideoVBlock:

    # face_collection is a rekall IntervalSetMapping of face intervals.

    # We want to see a list of VBlocks where each is a video in the collection
    # We want to see one track in each VBlock that shows all faces in the
    # collection with bounding boxes drawn and a flag metadata set.

    json = VideoVBlocksBuilder()\\
        .add_track(
            VideoTrackBuilder('faces', face_collection)\\
                .set_draw_type(DrawType_Bbox())\\
                .add_metadata('flag', Metadata_Flag()))\\
        .build()

Example of using IntervalBlock:

    # conversations_with_ids is a rekall IntervalSetMapping of conversation
    # sequences, where the payload on each conversation is an IntervalSet of
    # face bounding boxes with identity as payload.

    # We want to see a list of VBlocks where each is a conversation 
    # sequence in the collection. We want to see two tracks in each VBlock:
    # one showing the conversation sequence; another showing all the faces with
    # the bounding boxes drawn and generic metadata showing the identities.

    json = IntervalVBlocksBuilder()\\
        .add_track(
            IntervalTrackBuilder('conversation'))\\
        .add_track(
            IntervalTrackBuilder('faces', lambda i:i.payload)\\
                    .set_draw_type(DrawType_Bbox())\\
                    .add_metadata('identity', Metadata_Generic()))\\
        .build(conversations_with_ids)

Symbols exported in this module are the following.

VBlocksBuilders:
    VideoVBlocksBuilder: VideoVBlocks mode.
    IntervalVBlocksBuilder: IntervalVBlocks mode.

Tracks:
    VideoTrackBuilder: Build custom tracks for VideoVBlocks mode.
    IntervalTrackBuilder: Build custom tracks for IntervalVBlocks mode.

DrawTypes:
    DrawType_Bbox: Draw bounding boxes around the spatial dimension.
    DrawType_Caption: Display text in the caption box.

Metadatas:
    Metadata_Flag: Plant a flag marking the temporal interval.
    Metadata_Generic: Show a generic JSON text.

Helpers:
    build_interval: Build a JSON representation of the rekall interval.
"""

from rekall import IntervalSet, Interval
from rekall.bounds import Bounds3D
import shlex
import subprocess as sp
import json
import os


class _BlockMetaMixin:
    def add_video_metadata(self, video_baseurl, video_meta):
        self._video_meta = [
            {**v.to_json(), 'path': '{}/{}'.format(video_baseurl, v.path)} 
            for v in video_meta
        ]

        return self


class VideoVBlocksBuilder(_BlockMetaMixin):
    """Builder of a list of VBlocks, one for each video."""
    def __init__(self):
        self._tracks = {}
        self._video_ids = set([])
        self._video_meta = []

    def add_track(self, track):
        """Adds a track to vblocks.
        
        Args:
            track (VideoTrackBuilder): the track to add

        Returns:
            self for chaining
        """
        self._tracks[track.name] = track
        self._video_ids.update(track.video_ids)
        return self

    def build(self):
        """Builds the JSON list of vblocks to feed into VGrid."""
        return {
            'interval_blocks': [{
                'video_id': vid,
                'interval_dict': {
                    name: track.build_for_video(vid)
                    for name, track in self._tracks.items()
                },            
            } for vid in self._video_ids],
            'database': {
                'videos': self._video_meta
            }
        }

class _CustomTrackMixin:
    """Mixin for a TrackBuilder that allows custom draw type and metadata"""
    
    def set_draw_type(self, draw_type):
        """Set the type of visualization to draw for this track.

        VGrid will draw the visualization for each interval in this track.

        Args:
            draw_type: A function that takes video_id and Interval, and
                returns the JSON of the object to draw.

        Returns:
            self for chaining
        """
        self._draw_type = draw_type
        return self

    def add_metadata(self, name, metadata):
        """Add a named metadata to this track.

        VGrid will display the metadata for each interval in this track.

        Args:
            name (string): Name of the metadata
            metadata: A function that takes video_id and Interval, and
                returns the JSON of the metadata to display.

        Returns:
            self for chaining
        """
        self._metadatas[name] = metadata
        return self

    def _build_interval(self, video_id, interval):
        """Helper to build a JSON interval in this track."""
        return build_interval(video_id, interval,
                self._draw_type, self._metadatas)

def build_interval(video_id, interval, draw_type, metadatas):
    """Returns a JSON interval with given draw_type and metadatas.

    Args:
        video_id (int): Video ID as interval domain.
        interval (Interval): The interval to JSONify. Assumes the bounds is a
            Bounds3D.
        draw_type: A function that takes video_id and Interval, and
            returns the JSON of the object to draw.
        metadatas: A dictionary from metadata name to function that takes
            video_id and Interval, and returns the JSON of the metadata to
            display.

    Returns:
        A JSON interval with video_id as domain and all the draw_types and 
        metadatas.
    """
    return {
        "t": (interval['t1'], interval['t2']),
        "x": (interval['x1'], interval['x2']),
        "y": (interval['y1'], interval['y2']),
        "domain": _video_domain_in_json(video_id),
        "payload": {
            "draw_type": draw_type(video_id, interval),
            "metadata": {
                name: metadata(video_id, interval)
                for name, metadata in metadatas.items()
            },
        }
    }

class VideoTrackBuilder(_CustomTrackMixin):
    """Builder of a track for some collection of videos from IntervalSet.
    
    Attributes:
        name (string): Name of the track
        video_ids (Set[int]): Videos that should have this track.
    """
    def __init__(self, name, collection):
        """Initializer

        Args:
            name (string): Name of the track
            collection (DomainVideoCollection): intervals grouped by video_ids
                from which to build the visualization track
        """
        self.name = name
        self.video_ids = set(collection.keys())

        self._collection = collection
        self._draw_type = DrawType_Bbox()
        self._metadatas = {}

    def build_for_video(self, video_id):
        """Builds list of JSON intervals for the track on one VBlock/Video."""
        intervalset = self._collection[video_id]
        return [self._build_interval(video_id, interval)
                for interval in intervalset.get_intervals()]

class IntervalVBlocksBuilder(_BlockMetaMixin):
    """Builder of a list of VBlocks, one for each interval."""
    def __init__(self):
        self._tracks = {}

    def add_track(self, track):
        """Adds a track to each vblock

        Args:
            track (IntervalTrackBuilder): the track to add

        Returns:
            self for chaining
        """
        self._tracks[track.name] = track
        return self

    def build(self, collection):
        """Builds the JSON list of vblocks to feed into VGrid."""
        output = []
        for video_id, intervals in collection.items():
            for interval in intervals.get_intervals():
                output.append({
                    "video_id": video_id,
                    "interval_dict": {
                        name: track.build_for_interval(video_id, interval)
                        for name, track in self._tracks.items()
                    },
                })
        return {
            'interval_blocks': output,
            'database': {
                'videos': self._video_meta
            }
        }

class IntervalTrackBuilder(_CustomTrackMixin):
    """Builder of a track for single-interval vblocks.
    
    Attributes:
        name (string): Name of the track
    """
    def __init__(self, name, intervalset_getter=lambda i: IntervalSet([i])):
        """Initializer

        Args:
            name (string): Name of the track
            intervalset_getter (optional): A function that takes an Interval
                and returns the IntervalSet to visualize for that vblock.
                Defaults to the intervalset with only the vblock interval.
        """
        self.name = name

        self._intervalset_getter = intervalset_getter
        self._draw_type = DrawType_Bbox()
        self._metadatas = {}

    def build_for_interval(self, video_id, interval):
        """Builds list of JSON intervals for the track for one Interval."""
        intervalset = self._intervalset_getter(interval)
        return [self._build_interval(video_id, interval)
                for interval in intervalset.get_intervals()]

def _bounds_in_json(video_id, interval):
    """Returns a JSON object for interval bounds in VGrid."""
    return {
        "domain": _video_domain_in_json(video_id),
        "t1": interval.t[0],
        "t2": interval.t[1],
        "bbox": _bbox_in_json(interval),
    }

def _video_domain_in_json(video_id):
    """Returns a JSON  Domain_Video object."""
    return {
        "type": "Domain_Video",
        "args": {
            "video_id": video_id
        },
    }

def _bbox_in_json(interval):
    """Returns a JSON BoundingBox object."""
    return {
        "x1": interval.x[0],
        "x2": interval.x[1],
        "y1": interval.y[0],
        "y2": interval.y[1],
    }

def _get_payload(i):
    return i.payload

class DrawType_Caption:
    """A DrawType for displaying text in caption box"""
    def __init__(self, get_caption=_get_payload):
        """Initialize

        Args:
            get_caption (optional): A function from Interval to caption.
                Defaults to the payload field
        """
        self._get_caption = get_caption

    def __call__(self, video_id, interval):
        return {
            "type": "DrawType_Caption",
            "args": {
                "text": self._get_caption(interval)    
            },                    
        }

class DrawType_Bbox:
    """A DrawType for drawing bounding boxes around spatial extent"""
    def __call__(self, video_id, interval):
        return {"type": "DrawType_Bbox"}

class Metadata_Flag:
    """A Metadata that flags the interval on the Timeline."""
    def __init__(self, predicate=lambda _:True):
        """Initialize

        Args:
            predicate (optional): A function that takes an interval and returns
                whether to flag it.
                Defaults to always flagging.
        """
        self._pred = predicate

    def __call__(self, video_id, interval):
        if self._pred(interval):
            return {"type": "Metadata_Flag"}
        return None

class Metadata_Generic:
    """A Metadata that stores generic JSON"""
    def __init__(self, getter=_get_payload):
        """Initialize

        Args:
            getter (optional): A function from Interval to the generic
                metadata.
                Defaults to the payload field
        """
        self._getter = getter

    def __call__(self, video_id, interval):
        return {
            "type": "Metadata_Generic",
            "args": {
                "data": self._getter(interval)    
            }
        }

class Metadata_Categorical:
    """A Metadata that stores categorical values"""
    def __init__(self, category_name, getter=_get_payload):
        """Initialize

        Args:
            category_name (string): Name of the category.
            getter (optional): A function from Interval to the category.
                Defaults to the payload field
        """
        self._category_name = category_name
        self._getter = getter

    def __call__(self, video_id, interval):
        return {
            "type": "Metadata_Categorical",
            "args": {
                "category_type": self._category_name,
                "category": self._getter(interval),
            },
        }

class VideoMetadata:
    """Metadata about a video.

    The basic metadata is the video path and ID. The ID can be any arbitrary
    unique number, or a database ID if you have one. If the video path is on
    your local machine (as opposed to, say, a cloud bucket), then this class
    can fill in the remaining metadata (width, height, etc.) using ffprobe.
    """

    def __init__(self, path, id=None, fps=None, num_frames=None, width=None, height=None):
        if not os.path.isfile(path):
            raise Exception("Error: path {} does not exist".format(path))

        if fps is None:
            cmd = 'ffprobe -v quiet -print_format json -show_streams "{}"' \
                .format(path)
            outp = sp.check_output(shlex.split(cmd)).decode('utf-8')
            streams = json.loads(outp)['streams']
            video_stream = [s for s in streams if s['codec_type'] == 'video'][0]
            width = video_stream['width']
            height = video_stream['height']
            [num, denom] = map(int, video_stream['r_frame_rate'].split('/'))
            fps = float(num) / float(denom)
            num_frames = video_stream['nb_frames']

        self.path = path
        self.id = id
        self.fps = fps
        self.num_frames = num_frames
        self.width = width
        self.height = height

    def to_json(self):
        return {
            'id': self.id,
            'path': self.path,
            'num_frames': self.num_frames,
            'fps': self.fps,
            'width': self.width,
            'height': self.height
        }

class Category:
    def __init__(self):
        # TODO
        pass

class DatabaseBuilder:
    """Builder for the VGrid metadata database."""

    def __init__(self, video_baseurl):
        self._video_baseurl = video_baseurl
        self._videos = None

    def add_category(self, category):
        # TODO
        return self

    def build(self):
        for video in self._videos:
            video.path = '{}/{}'.format(self._video_baseurl, video.path)

        return {
            'videos': [v.to_json() for v in self._videos]
        }

