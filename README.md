# yum_repository_info ansible module

A repo file can contain meta data on multiple repos from a variety of sources. This information constitutes one of the views on the content available for the host that we are examining. This module reads the information from a provided repo file defined by path and returns a dictionary called content_view. This maps to familiar terminology from foreman. 