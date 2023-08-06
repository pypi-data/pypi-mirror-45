from functools import reduce
import os
import sys
import logging
import time
import marshal
import tempfile
import threading
from shutil import move as _replace_file
from hashlib import md5

DICT_WRITING = {}
_get_abs_path = lambda path: os.path.normpath(os.path.join(os.path.split(os.path.realpath(__file__))[0], path))
DEFAULT_DICT = "simple_dict.txt"
log_console = logging.StreamHandler(sys.stderr)
default_logger = logging.getLogger(__name__)
default_logger.setLevel(logging.DEBUG)
default_logger.addHandler(log_console)


class yn(object):
    def __init__(self, dictionary=DEFAULT_DICT):
        self.lock = threading.RLock()
        if dictionary == DEFAULT_DICT:
            self.dictionary = dictionary
        else:
            self.dictionary = _get_abs_path(dictionary)
        self.initialized = None
        self.tmp_dir = None
        self.cache_file = None
        self._initialize(dictionary)

    def __repr__(self):
        return "Simple dictionary file={}".format(self.dictionary)

    def _initialize(self, dictionary=None):
        if dictionary:
            abs_path = _get_abs_path(dictionary)
            if self.dictionary == abs_path and self.initialized:
                return
            else:
                self.dictionary = abs_path
                self.initialized = False
        else:
            abs_path = self.dictionary

        with self.lock:
            try:
                with DICT_WRITING[abs_path]:
                    pass
            except KeyError:
                pass
            if self.initialized:
                return

        default_logger.debug(
            "Building from %s ..." % (abs_path or "the default dictionary")
        )
        t1 = time.time()
        if self.cache_file:
            cache_file = self.cache_file
            # default dictionary
        elif abs_path == DEFAULT_DICT:
            cache_file = "yn.cache"
            # custom dictionary
        else:
            cache_file = (
                "yn.u%s.cache" % md5(abs_path.encode("utf-8", "replace")).hexdigest()
            )
        cache_file = os.path.join(self.tmp_dir or tempfile.gettempdir(), cache_file)
        load_from_cache_fail = True
        tmpdir = os.path.dirname(cache_file)

        if os.path.isfile(cache_file) and (
            abs_path == DEFAULT_DICT
            or os.path.getmtime(cache_file) > os.path.getmtime(abs_path)
        ):
            default_logger.debug("Loading model from cache %s" % cache_file)
            try:
                with open(cache_file, "rb") as cf:
                    self.yes, self.no, self.others, self.filtered = marshal.load(cf)
                    load_from_cache_fail = False
            except Exception:
                load_from_cache_fail = True
        if load_from_cache_fail:
            wlock = DICT_WRITING.get(abs_path, threading.RLock())
            DICT_WRITING[abs_path] = wlock
            with wlock:
                self.yes, self.no, self.others, self.filtered = self._load_simple_dict(
                    self.dictionary
                )
                default_logger.debug("Dumping model to file cache %s" % cache_file)
                try:
                    # prevent moving across different filesystems
                    fd, fpath = tempfile.mkstemp(dir=tmpdir)
                    with os.fdopen(fd, "wb") as temp_cache_file:
                        marshal.dump(
                            (self.yes, self.no, self.others, self.filtered),
                            temp_cache_file,
                        )
                    _replace_file(fpath, cache_file)
                except Exception:
                    default_logger.exception("Dump cache file failed.")

            try:
                del DICT_WRITING[abs_path]
            except KeyError:
                pass
        self.yes = set(self.yes)
        self.no = set(self.no)
        self.filtered = set(self.filtered)
        self.others = set(self.others)
        self.initialized = True
        default_logger.debug("Loading dict cost %.3f seconds." % (time.time() - t1))
        default_logger.debug("simple dict has been built successfully.")

    """
    pos: 肯定
    neg: 否定
    others: 语气词，无实际意义的词
    filter: 过滤词（可能判断错）
    """

    def _load_simple_dict(self, path):
        yes = []
        no = []
        others = []
        filtered = []
        with open(path, "r", encoding="utf8") as file:
            y = False
            n = False
            o = False
            f = False
            for line in file:
                line = line.rstrip()
                if line == "pos:":
                    y = True
                    n = False
                    o = False
                    f = False
                elif line == "neg:":
                    y = False
                    n = True
                    o = False
                    f = False
                elif line == "others:":
                    y = False
                    n = False
                    o = True
                    f = False
                elif line == "filter:":
                    y = False
                    n = False
                    o = False
                    f = True
                elif y and line:
                    yes.append(line)
                elif n and line:
                    no.append(line)
                elif o and line:
                    others.append(line)
                elif f and line:
                    filtered.append(line)
                else:
                    pass

        return yes, no, others, filtered

    '''
    识别肯否定
    params: 
    s: 字符串
    thre: 字符串最长长度
    return:
    Positive: 肯定
    Negtive: 否定
    Nonsense: 无意义
    Incognizance: 不识别
    too long: 字符串长度超过thre
    '''
    def y_n(self, s, thre=6):
        if len(s) < thre:
            # 如果有过滤词，直接返回4
            for e in self.filtered:
                if s.find(e) > -1:
                    return "Incognizance"
            sen1 = set(s) - self.others
            sen2 = sen1 - self.yes - self.no
            # 无意义句子
            if not sen1:
                return "Nonsense"
            if sen2:
                return "Incognizance"
            t_count = 0
            f_count = 0
            for e in self.yes:
                t_count += s.count(e)
            t = [True for _ in range(t_count)]
            for e in self.no:
                f_count += s.count(e)
            f = [False for _ in range(f_count)]

            tf = t + f
            result = reduce(lambda x, y: not (bool(x) ^ bool(y)), tf)
            if result:
                return "Positive"
            if not result:
                return "Negtive"
        else:
            return "too long"
