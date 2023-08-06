# -*- coding: utf-8 -*-

# Copyright 2017-2019 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extract images from https://www.flickr.com/"""

from .common import Extractor, Message
from .. import text, oauth, util, exception


class FlickrExtractor(Extractor):
    """Base class for flickr extractors"""
    category = "flickr"
    filename_fmt = "{category}_{id}.{extension}"

    def __init__(self, match):
        Extractor.__init__(self, match)
        self.api = FlickrAPI(self)
        self.item_id = match.group(1)
        self.user = None
        self.load_extra = self.config("metadata", False)

    def items(self):
        info = self.data()
        yield Message.Version, 1
        yield Message.Directory, info
        for photo in self.photos():
            photo.update(info)
            url = photo["photo"]["source"]
            yield Message.Url, url, text.nameext_from_url(url, photo)

    def data(self):
        self.user = self.api.urls_lookupUser(self.item_id)
        return {"user": self.user}

    def photos(self):
        return []


class FlickrImageExtractor(FlickrExtractor):
    """Extractor for individual images from flickr.com"""
    subcategory = "image"
    archive_fmt = "{id}"
    pattern = (r"(?:https?://)?(?:"
               r"(?:(?:www\.|m\.)?flickr\.com/photos/[^/]+/"
               r"|[^.]+\.static\.?flickr\.com/(?:\d+/)+)(\d+)"
               r"|flic\.kr/p/([A-Za-z1-9]+))")
    test = (
        ("https://www.flickr.com/photos/departingyyz/16089302239", {
            "pattern": pattern,
            "content": "0821a28ee46386e85b02b67cf2720063440a228c",
            "keyword": {
                "extension": "jpg",
                "filename": "16089302239_de18cd8017_b",
                "id": "16089302239",
                "photo": {
                    "height": "683",
                    "label": "Large",
                    "media": "photo",
                    "source": str,
                    "url": str,
                    "width": "1024"
                },
            },
        }),
        ("http://c2.staticflickr.com/2/1475/24531000464_9a7503ae68_b.jpg", {
            "pattern": pattern}),
        ("https://farm2.static.flickr.com/1035/1188352415_cb139831d0.jpg", {
            "pattern": pattern}),
        ("https://flic.kr/p/FPVo9U", {
            "pattern": pattern}),
        ("https://www.flickr.com/photos/zzz/16089302238", {
            "exception": exception.NotFoundError}),
    )

    def __init__(self, match):
        FlickrExtractor.__init__(self, match)
        if not self.item_id:
            alphabet = ("123456789abcdefghijkmnopqrstu"
                        "vwxyzABCDEFGHJKLMNPQRSTUVWXYZ")
            self.item_id = util.bdecode(match.group(2), alphabet)

    def items(self):
        size = self.api.photos_getSizes(self.item_id)[-1]

        if self.load_extra:
            info = self.api.photos_getInfo(self.item_id)
            self._clean(info)
        else:
            info = {"id": self.item_id}

        info["photo"] = size
        url = size["source"]
        text.nameext_from_url(url, info)

        yield Message.Version, 1
        yield Message.Directory, info
        yield Message.Url, url, info

    @staticmethod
    def _clean(photo):
        del photo["comments"]
        del photo["views"]

        photo["title"] = photo["title"]["_content"]
        photo["tags"] = [t["raw"] for t in photo["tags"]["tag"]]

        if "location" in photo:
            location = photo["location"]
            for key, value in location.items():
                if isinstance(value, dict):
                    location[key] = value["_content"]


class FlickrAlbumExtractor(FlickrExtractor):
    """Extractor for photo albums from flickr.com"""
    subcategory = "album"
    directory_fmt = ("{category}", "{subcategory}s",
                     "{album[id]} - {album[title]}")
    archive_fmt = "a_{album[id]}_{id}"
    pattern = (r"(?:https?://)?(?:www\.)?flickr\.com/"
               r"photos/([^/]+)/(?:album|set)s(?:/(\d+))?")
    test = (
        (("https://www.flickr.com/photos/shona_s/albums/72157633471741607"), {
            "pattern": FlickrImageExtractor.pattern,
            "count": 6,
        }),
        ("https://www.flickr.com/photos/shona_s/albums", {
            "pattern": pattern,
            "count": 2,
        }),
    )

    def __init__(self, match):
        FlickrExtractor.__init__(self, match)
        self.album_id = match.group(2)

    def items(self):
        if self.album_id:
            return FlickrExtractor.items(self)
        return self._album_items()

    def _album_items(self):
        yield Message.Version, 1
        data = FlickrExtractor.data(self)
        data["_extractor"] = FlickrAlbumExtractor

        for albums in self.api.photosets_getList(self.user["nsid"]):
            for album in albums["photoset"]:
                self.api._clean_info(album).update(data)
                url = "https://www.flickr.com/photos/{}/albums/{}".format(
                    self.user["path_alias"], album["id"])
                yield Message.Queue, url, album

    def data(self):
        data = FlickrExtractor.data(self)
        data["album"] = self.api.photosets_getInfo(
            self.album_id, self.user["nsid"])
        return data

    def photos(self):
        return self.api.photosets_getPhotos(self.album_id)


class FlickrGalleryExtractor(FlickrExtractor):
    """Extractor for photo galleries from flickr.com"""
    subcategory = "gallery"
    directory_fmt = ("{category}", "galleries",
                     "{user[username]} {gallery[id]}")
    archive_fmt = "g_{gallery[id]}_{id}"
    pattern = (r"(?:https?://)?(?:www\.)?flickr\.com/"
               r"photos/([^/]+)/galleries/(\d+)")
    test = (("https://www.flickr.com/photos/flickr/"
             "galleries/72157681572514792/"), {
        "pattern": FlickrImageExtractor.pattern,
        "count": 12,
    })

    def __init__(self, match):
        FlickrExtractor.__init__(self, match)
        self.gallery_id = match.group(2)

    def data(self):
        info = FlickrExtractor.data(self)
        if self.load_extra:
            info["gallery"] = self.api.galleries_getInfo(self.gallery_id)
        else:
            info["gallery"] = {"id": self.gallery_id}
        return info

    def photos(self):
        return self.api.galleries_getPhotos(self.gallery_id)


class FlickrGroupExtractor(FlickrExtractor):
    """Extractor for group pools from flickr.com"""
    subcategory = "group"
    directory_fmt = ("{category}", "{subcategory}s", "{group[groupname]}")
    archive_fmt = "G_{group[nsid]}_{id}"
    pattern = r"(?:https?://)?(?:www\.)?flickr\.com/groups/([^/]+)"
    test = ("https://www.flickr.com/groups/bird_headshots/", {
        "pattern": FlickrImageExtractor.pattern,
        "count": "> 150",
    })

    def data(self):
        self.group = self.api.urls_lookupGroup(self.item_id)
        return {"group": self.group}

    def photos(self):
        return self.api.groups_pools_getPhotos(self.group["nsid"])


class FlickrUserExtractor(FlickrExtractor):
    """Extractor for the photostream of a flickr user"""
    subcategory = "user"
    directory_fmt = ("{category}", "{user[username]}")
    archive_fmt = "u_{user[nsid]}_{id}"
    pattern = r"(?:https?://)?(?:www\.)?flickr\.com/photos/([^/]+)/?$"
    test = ("https://www.flickr.com/photos/shona_s/", {
        "pattern": FlickrImageExtractor.pattern,
        "count": 28,
    })

    def photos(self):
        return self.api.people_getPhotos(self.user["nsid"])


class FlickrFavoriteExtractor(FlickrExtractor):
    """Extractor for favorite photos of a flickr user"""
    subcategory = "favorite"
    directory_fmt = ("{category}", "{subcategory}s", "{user[username]}")
    archive_fmt = "f_{user[nsid]}_{id}"
    pattern = r"(?:https?://)?(?:www\.)?flickr\.com/photos/([^/]+)/favorites"
    test = ("https://www.flickr.com/photos/shona_s/favorites", {
        "pattern": FlickrImageExtractor.pattern,
        "count": 4,
    })

    def photos(self):
        return self.api.favorites_getList(self.user["nsid"])


class FlickrSearchExtractor(FlickrExtractor):
    """Extractor for flickr photos based on search results"""
    subcategory = "search"
    directory_fmt = ("{category}", "{subcategory}", "{search[text]}")
    archive_fmt = "s_{search}_{id}"
    pattern = r"(?:https?://)?(?:www\.)?flickr\.com/search/?\?([^#]+)"
    test = (
        ("https://flickr.com/search/?text=mountain"),
        ("https://flickr.com/search/?text=tree%20cloud%20house"
         "&color_codes=4&styles=minimalism"),
    )

    def __init__(self, match):
        FlickrExtractor.__init__(self, match)
        self.search = text.parse_query(match.group(1))
        if "text" not in self.search:
            self.search["text"] = ""

    def data(self):
        return {"search": self.search}

    def photos(self):
        return self.api.photos_search(self.search)


class FlickrAPI(oauth.OAuth1API):
    """Minimal interface for the flickr API"""
    API_URL = "https://api.flickr.com/services/rest/"
    API_KEY = "ac4fd7aa98585b9eee1ba761c209de68"
    API_SECRET = "3adb0f568dc68393"
    FORMATS = [
        ("o", "Original", None),
        ("k", "Large 2048", 2048),
        ("h", "Large 1600", 1600),
        ("l", "Large", 1024),
        ("c", "Medium 800", 800),
        ("z", "Medium 640", 640),
        ("m", "Medium", 500),
        ("n", "Small 320", 320),
        ("s", "Small", 240),
        ("q", "Large Square", 150),
        ("t", "Thumbnail", 100),
        ("s", "Square", 75),
    ]

    def __init__(self, extractor):
        oauth.OAuth1API.__init__(self, extractor)

        self.maxsize = extractor.config("size-max")
        if isinstance(self.maxsize, str):
            for fmt, fmtname, fmtwidth in self.FORMATS:
                if self.maxsize == fmt or self.maxsize == fmtname:
                    self.maxsize = fmtwidth
                    break
            else:
                self.maxsize = None
                extractor.log.warning(
                    "Could not match '%s' to any format", self.maxsize)
        if self.maxsize:
            self.formats = [fmt for fmt in self.FORMATS
                            if not fmt[2] or fmt[2] <= self.maxsize]
        else:
            self.formats = self.FORMATS
        self.formats = self.formats[:4]

    def favorites_getList(self, user_id):
        """Returns a list of the user's favorite photos."""
        params = {"user_id": user_id}
        return self._listing("favorites.getList", params)

    def galleries_getInfo(self, gallery_id):
        """Gets information about a gallery."""
        params = {"gallery_id": gallery_id}
        gallery = self._call("galleries.getInfo", params)["gallery"]
        return self._clean_info(gallery)

    def galleries_getPhotos(self, gallery_id):
        """Return the list of photos for a gallery."""
        params = {"gallery_id": gallery_id}
        return self._listing("galleries.getPhotos", params)

    def groups_pools_getPhotos(self, group_id):
        """Returns a list of pool photos for a given group."""
        params = {"group_id": group_id}
        return self._listing("groups.pools.getPhotos", params)

    def people_getPhotos(self, user_id):
        """Return photos from the given user's photostream."""
        params = {"user_id": user_id}
        return self._listing("people.getPhotos", params)

    def photos_getInfo(self, photo_id):
        """Get information about a photo."""
        params = {"photo_id": photo_id}
        return self._call("photos.getInfo", params)["photo"]

    def photos_getSizes(self, photo_id):
        """Returns the available sizes for a photo."""
        params = {"photo_id": photo_id}
        sizes = self._call("photos.getSizes", params)["sizes"]["size"]
        if sizes[-1]["media"] == "video":
            # filter all non-video and mobile entries
            sizes = [size for size in sizes
                     if size["media"] == "video" and
                     not size["label"].startswith(("Mobile ", "Video "))]
        if self.maxsize:
            for index, size in enumerate(sizes):
                if index > 0 and (int(size["width"]) > self.maxsize or
                                  int(size["height"]) > self.maxsize):
                    del sizes[index:]
                    break
        return sizes

    def photos_search(self, params):
        """Return a list of photos matching some criteria."""
        return self._listing("photos.search", params.copy())

    def photosets_getInfo(self, photoset_id, user_id):
        """Gets information about a photoset."""
        params = {"photoset_id": photoset_id, "user_id": user_id}
        photoset = self._call("photosets.getInfo", params)["photoset"]
        return self._clean_info(photoset)

    def photosets_getList(self, user_id):
        """Returns the photosets belonging to the specified user."""
        params = {"user_id": user_id}
        return self._pagination("photosets.getList", params)

    def photosets_getPhotos(self, photoset_id):
        """Get the list of photos in a set."""
        params = {"photoset_id": photoset_id}
        return self._listing("photosets.getPhotos", params)

    def urls_lookupGroup(self, groupname):
        """Returns a group NSID, given the url to a group's page."""
        params = {"url": "https://www.flickr.com/groups/" + groupname}
        group = self._call("urls.lookupGroup", params)["group"]
        return {"nsid": group["id"],
                "path_alias": groupname,
                "groupname": group["groupname"]["_content"]}

    def urls_lookupUser(self, username):
        """Returns a user NSID, given the url to a user's photos or profile."""
        params = {"url": "https://www.flickr.com/photos/" + username}
        user = self._call("urls.lookupUser", params)["user"]
        return {"nsid": user["id"],
                "path_alias": username,
                "username": user["username"]["_content"]}

    def _call(self, method, params):
        params["method"] = "flickr." + method
        params["format"] = "json"
        params["nojsoncallback"] = "1"
        if self.api_key:
            params["api_key"] = self.api_key
        data = self.request(self.API_URL, params=params).json()
        if "code" in data:
            if data["code"] == 1:
                raise exception.NotFoundError(self.extractor.subcategory)
            elif data["code"] == 98:
                raise exception.AuthenticationError(data.get("message"))
            elif data["code"] == 99:
                raise exception.AuthorizationError()
            self.log.error("API call failed: %s", data.get("message"))
            raise exception.StopExtraction()
        return data

    def _pagination(self, method, params):
        params["extras"] = ",".join("url_" + fmt[0] for fmt in self.formats)
        params["page"] = 1

        while True:
            data = self._call(method, params)

            for key, obj in data.items():
                if not key.startswith("stat"):
                    break
            del obj["page"]
            del obj["perpage"]
            if "per_page" in obj:
                del obj["per_page"]

            yield obj

            if params["page"] >= obj["pages"]:
                break
            params["page"] += 1

    def _listing(self, method, params):
        for photos in self._pagination(method, params):
            for photo in photos["photo"]:
                self._extract_format(photo)
                yield photo

    def _extract_format(self, photo):
        for fmt, fmtname, fmtwidth in self.formats:
            key = "url_" + fmt
            if key in photo:
                width, height = photo["width_" + fmt], photo["height_" + fmt]
                if self.maxsize and (int(width) > self.maxsize or
                                     int(height) > self.maxsize):
                    continue
                # generate photo info
                photo["photo"] = {
                    "source": photo[key],
                    "width" : width,
                    "height": height,
                    "label" : fmtname,
                    "media" : "photo",
                }
                # remove excess data
                keys = [
                    key for key in photo.keys()
                    if key.startswith(("url_", "width_", "height_"))
                ]
                for key in keys:
                    del photo[key]
                break
        else:
            # extra API call to get photo url and size
            photo["photo"] = self.photos_getSizes(photo["id"])[-1]

    @staticmethod
    def _clean_info(info):
        del info["count_views"]
        del info["count_comments"]
        info["title"] = info["title"]["_content"]
        info["description"] = info["description"]["_content"]
        return info
