from git import Git, Repo
from jinja2 import Template, DebugUndefined
from mkdocs.plugins import BasePlugin
from natsort import natsorted

import re


class GitLatestReleasePlugin(BasePlugin):

    def __init__(self):
        self.g = Git()

    def on_page_markdown(self, markdown, page, config, files):
        tags = self.get_tags_from_repo(repo_path=page.file.abs_src_path)
        latest_git_tag = self.get_latest_tag(tags)
        t = Template(markdown, undefined=DebugUndefined)
        return t.render({'git_latest_tag': latest_git_tag})

    def get_tags_from_repo(self, repo_path):
        """Return an iterable list of all tags found in a git repository.

        :param repo_path: File path to the root directory or a sub-directory
        of a git repository.
        :return: Iterable list of all tags found in the git repository. Returns
        None if no tags found or no git repository found.
        """
        r = Repo(repo_path, search_parent_directories=True)
        if r:
            return r.tags
        else:
            return None

    def get_latest_tag(self, tags, regex=r"\d+\.\d+\.\d+"):
        """Return the highest tag from list which matches the configured regex.
        The highest tag is determined using the natsort natural sorting module

        :param tags: Iterable list of git tags to search. Each item in the list
        is expected to have a .name property.
        :param regex: Regular expression to filter the tag list with. Default is
        r"\d+\.\d+\.\d+"
        :return: String with the highest semver tag, returns "unknown" if not found.
        """
        r = re.compile(regex)
        matching_tags = [tag for tag in tags if r.search(tag.name)]

        if matching_tags:
            return natsorted(matching_tags)[-1]
        else:
            return "unknown"
