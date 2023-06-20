#!/usr/bin/env python3

import argparse
import functools

from docker_image import reference
from oslo_config import cfg
from oslo_log import log as logging
from ruyaml import YAML
import requests

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


@functools.cache
def get_pinned_image(image_src):
    image_ref = reference.Reference.parse(image_src)

    if image_ref.domain() == "quay.io":
        r = requests.get(
            f"https://quay.io/api/v1/repository/{image_ref.path()}/tag/",
            params={"specificTag": image_ref["tag"]},
        )
        r.raise_for_status()
        digest = r.json()["tags"][0]["manifest_digest"]

    return f"{image_ref.domain()}/{image_ref.path()}@{digest}"


def main():
    logging.register_options(CONF)
    logging.setup(CONF, "atmosphere-bump-images")

    parser = argparse.ArgumentParser("bump-images")
    parser.add_argument(
        "src", help="Path for default values file", type=argparse.FileType("r")
    )
    parser.add_argument("dst", help="Path for output file", type=argparse.FileType("w"))

    args = parser.parse_args()

    yaml = YAML(typ="rt")
    data = yaml.load(args.src)

    for image in data["atmosphere_images"].ca.items:
        token = data["atmosphere_images"].ca.get(image, 2).value
        if not token.startswith("# image-source: "):
            LOG.info("Skipping image %s", image)
            continue

        image_src = token.replace("# image-source: ", "").strip()
        pinned_image = get_pinned_image(image_src)

        LOG.info("Pinning image %s from %s to %s", image, image_src, pinned_image)
        data["atmosphere_images"][image] = pinned_image

    yaml.dump(data, args.dst)


if __name__ == "__main__":
    main()