# mkdocs_latest_release_plugin

Plugin for MKDocs to inject a Git Tag into the markdown. The primary purpose is to allow an MKDocs site, in the same repository as the application in GitHub, to display the latest released version, based on the git tags. 

## Origin and Purpose

This plugin was specifically created to support GitHub projects using GitHub Pages and mkdocs to publish documentation which also use tags to mark releases. Case in point is authoring Jenkins shared libraries and associated documentation. The shared libraries are cloned by consumers using a the repository source and a git tag to specify the version. Documentation for the shared library lives within the same repository, so ensuring documentation is updated can be part of the Pull Request/review process, however not all merges to master are released. It was initially useful to refer to the latest release version in the documentation, but this quickly went out of date, as not all merges to master were released, so it was not practical to maintain this manually, and in generally nothing should be maintained manually that doesn't have to be. Hence the need for this plugin to MKDocs which is used in the automated build and release process for our Jenkins shared library code.    

## Install

`pip install mkdocs_latest_release_plugin`

## Usage

Enable the plugin in `mkdocs.yml`

```yaml
plugins:
  - search
  - git-latest-release
```

Add `{{ git_latest_release }}` anywhere in the markdown where you want to refer to the latest release tag. Release tags are presumed to be semantic version tags, therefore matching the regex `\d+\.\d+\.\d+`.  
