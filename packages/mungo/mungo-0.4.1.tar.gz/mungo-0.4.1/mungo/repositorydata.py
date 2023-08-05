import bz2
import copy
import json
import os
import pickle
from collections import defaultdict
from datetime import datetime, timezone
from os.path import getmtime, basename
from typing import DefaultDict, List
from urllib.error import URLError
from urllib.request import Request, urlopen


def download_repo(url: str, name: str, offline: bool = False, force_download: bool = False):
    return RepositoryData.from_url(url, name, offline, force_download)


def get_repository_data(channels: list,
                        njobs: int = 8,
                        offline: bool = False,
                        force_download: bool = False) -> List['RepositoryData']:
    # retrieve repodata asynchronously
    urls = []
    for channel in channels:
        for arch in ['linux-64', 'noarch']:
            if channel != "defaults":
                urls.append((f"https://conda.anaconda.org/{channel}/{arch}", f"{channel}/{arch}"))
            else:
                for c in ['main', 'free', 'pro', 'r']:
                    urls.append((f"https://repo.anaconda.com/pkgs/{c}/{arch}", f"{c}/{arch}"))

    from joblib import Parallel, delayed
    return list(
        Parallel(n_jobs=njobs)(delayed(download_repo)(url, name, offline, force_download) for url, name in urls))


def merge_repository_data(repository_data_list: List['RepositoryData']) -> 'RepositoryData':
    ret = RepositoryData.empty()
    # deepcopy since we do not want to modify the contents of `repository_data_list[0].d`!
    ret.d = copy.deepcopy(repository_data_list[0].d)
    for r in repository_data_list[1:]:
        for name, versions in r.d.items():
            for version in versions:
                if version not in ret.d[name]:
                    ret.d[name][version] = r.d[name][version]
    return ret


def _mtime(filename: str) -> datetime:
    return datetime.fromtimestamp(getmtime(filename))


def _mtime_timestamp(filename: str) -> float:
    return _mtime(filename).replace(tzinfo=timezone.utc).timestamp()


def _cachedir() -> str:
    return os.getenv("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))


def parse_repository_data(repository_name: str, json_data: dict) -> DefaultDict[str, dict]:
    ret = defaultdict(dict)

    if json_data is None:
        return ret

    packages = json_data["packages"]

    for filename, p in packages.items():
        new_version = (p["version"], p["build"])
        p["fn"] = filename
        p["channel"] = f"https://conda.anaconda.org/{repository_name}"
        ret[p["name"]][new_version] = p

    for name, versions in ret.items():
        for v_name, v_value in versions.items():
            v_value["reponame"] = repository_name
    return ret


class RepositoryData:
    def __init__(self, name: str, data: dict):
        self.name = name
        self.d = data

    @classmethod
    def empty(cls) -> 'RepositoryData':
        return cls(None, defaultdict(dict))

    @classmethod
    def _from_json(cls,
                   name: str,
                   json_data: dict,
                   cache: bool = True,
                   remote_mtime=None,
                   force_store: bool = False) -> 'RepositoryData':
        repository_data = parse_repository_data(name, json_data)
        if cache:
            local_dir = os.path.expanduser(os.path.join(_cachedir(), 'conda', 'repos', name))
            local_file = os.path.join(local_dir, 'repodata.pickle')
            if os.path.exists(local_file):
                local_mtime = _mtime_timestamp(local_file)
                if force_store or not remote_mtime or remote_mtime > local_mtime:
                    # print(f"Remote {name}/repodata is newer, updating {local_file}.")
                    with open(local_file, 'wb') as writer:
                        pickle.dump(repository_data, writer)
                    os.utime(local_file, (remote_mtime, remote_mtime))
                else:
                    # print(f"{local_file} is up to date")
                    pass
            else:
                # print(f"Saving {name}/repodata to {local_file}")
                os.makedirs(local_dir, exist_ok=True)
                with open(local_file, 'wb') as writer:
                    pickle.dump(repository_data, writer)
                if remote_mtime:
                    os.utime(local_file, (remote_mtime, remote_mtime))
        return cls(name, repository_data)

    @classmethod
    def _from_pickle(cls, name: str, pickle_file: str) -> 'RepositoryData':
        with open(pickle_file, 'rb') as reader:
            repository_data = pickle.load(reader)
        return cls(name, repository_data)

    @classmethod
    def from_file(cls, filename: str) -> 'RepositoryData':
        opener = bz2.open if filename.endswith('.bz2') else open
        with opener(filename, 'rb') as reader:
            json_data = json.load(reader)
        return cls._from_json(filename, json_data)

    @classmethod
    def from_environment(cls, environment: str) -> 'RepositoryData':
        ret = defaultdict(dict)
        # This is a linux only, default path only version of conda's `list_all_known_prefixes`.
        environments_file = os.path.expanduser('~/.conda/environments.txt')
        if not os.path.exists(environments_file):
            raise ValueError("Could not read environment information from ~/.conda/environments.txt.")
        with open(environments_file, 'rt') as reader:
            # FIXME assumption that first line of environments.txt corresponds to base env path might be incorrect
            default_env_path = reader.readline().strip()
            env_map = {basename(path): path for path in map(str.strip, reader)}
            # env_map[default_env_name] = default_env_path
        if environment == "base" or environment == "":
            meta_dir = os.path.join(default_env_path, "conda-meta")
        else:
            env_path = env_map.get(environment)
            if env_path is None:
                raise ValueError(f"No such environment {environment}.")
            meta_dir = os.path.join(env_path, "conda-meta")

        for file in os.listdir(meta_dir):
            if not file.endswith(".json"):
                continue

            with open(os.path.join(meta_dir, file), 'rb') as reader:
                p = json.load(reader)
                name = p["name"]
                p["installed"] = True
            new_version = (p["version"], p["build"])
            ret[name][new_version] = p
        return cls(environment, ret)

    @classmethod
    def from_url(cls,
                 url: str,
                 repository_name: str,
                 offline: bool = False,
                 force_download: bool = False) -> 'RepositoryData':
        repodata_url = url + "/repodata.json.bz2"
        local_dir = os.path.expanduser(os.path.join(_cachedir(), 'conda', 'repos', repository_name))
        local_file = os.path.join(local_dir, 'repodata.pickle')
        headers = {}

        if offline:  # TODO if offline check if pickle exist
            return cls._from_pickle(repository_name, local_file)

        if not force_download and os.path.exists(local_file):
            local_timestamp = _mtime(local_file)
            d = local_timestamp.strftime('%a, %d %b %Y %H:%M:%S %Z')
            headers["If-Modified-Since"] = d
        request = Request(repodata_url, headers=headers)
        # The following code is slightly unwieldy, sorry for that
        with urlopen(Request(repodata_url, method='HEAD')) as conn:
            last_modified = conn.headers.get('last-modified', None)
            if last_modified is not None:
                last_modified = datetime.strptime(last_modified, '%a, %d %b %Y %H:%M:%S %Z')
                last_modified = last_modified.replace(tzinfo=timezone.utc).timestamp()
                if os.path.exists(local_file):
                    if last_modified <= _mtime_timestamp(local_file) and not force_download:
                        return cls._from_pickle(repository_name, local_file)
        try:
            with urlopen(request) as conn:
                json_data_compressed = conn.read()
                data = json.loads(bz2.decompress(json_data_compressed))
                return cls._from_json(repository_name, data, remote_mtime=last_modified, force_store=force_download)
        except URLError as e:
            if e.getcode() == 304:  # NOT MODIFIED
                return cls._from_pickle(repository_name, local_file)
            else:
                raise e
