# SPDX-FileCopyrightText: © 2025 VEXXHOST, Inc.
# SPDX-License-Identifier: GPL-3.0-or-later
# Atmosphere-Rebuild-Time: 2024-06-25T22:49:25Z

FROM openstack-venv-builder AS build
# renovate: name=openstack/octavia repo=https://opendev.org/openstack/octavia.git branch=master
ARG OCTAVIA_GIT_REF=e15cb80d8f325e7474fb2175a1a8e9805a473295
ADD --keep-git-dir=true https://opendev.org/openstack/octavia.git#${OCTAVIA_GIT_REF} /src/octavia
RUN git -C /src/octavia fetch --unshallow
# renovate: name=openstack/ovn-octavia-provider repo=https://opendev.org/openstack/ovn-octavia-provider.git branch=master
ARG OVN_OCTAVIA_PROVIDER_GIT_REF=a101619646c6dd792d10042100a78e4f2e13a3af
ADD --keep-git-dir=true https://opendev.org/openstack/ovn-octavia-provider.git#${OVN_OCTAVIA_PROVIDER_GIT_REF} /src/ovn-octavia-provider
RUN git -C /src/ovn-octavia-provider fetch --unshallow
RUN --mount=type=cache,target=/root/.cache/uv <<EOF bash -xe
uv pip install \
    --constraint /upper-constraints.txt \
        /src/octavia[redis] \
        /src/ovn-octavia-provider
EOF

FROM openstack-python-runtime
RUN <<EOF bash -xe
apt-get update -qq
apt-get install -qq -y --no-install-recommends \
    isc-dhcp-client openssh-client
apt-get clean
rm -rf /var/lib/apt/lists/*
EOF
COPY --from=build --link /var/lib/openstack /var/lib/openstack
