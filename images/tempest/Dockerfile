# Copyright (c) 2024 VEXXHOST, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

ARG RELEASE

FROM golang:1.18 AS octavia-test-server
ADD --keep-git-dir=true https://opendev.org/openstack/octavia-tempest-plugin.git#master /src
RUN GO111MODULE=off CGO_ENABLED=0 GOOS=linux go build \
    -a -ldflags '-s -w -extldflags -static' \
    -o /build/test_server.bin \
    /src/octavia_tempest_plugin/contrib/test_server/test_server.go

FROM registry.atmosphere.dev/library/openstack-venv-builder:${RELEASE} AS build
ARG TEMPEST_GIT_REF=c0da6e843a74c2392c8e87e8ff36d2fea12949c4
ADD --keep-git-dir=true https://opendev.org/openstack/tempest.git#${TEMPEST_GIT_REF} /src/tempest
RUN git -C /src/tempest fetch --unshallow
ADD --keep-git-dir=true https://opendev.org/openstack/barbican-tempest-plugin.git#master /src/barbican-tempest-plugin
RUN git -C /src/barbican-tempest-plugin fetch --unshallow
ADD --keep-git-dir=true https://opendev.org/openstack/cinder-tempest-plugin.git#master /src/cinder-tempest-plugin
RUN git -C /src/cinder-tempest-plugin fetch --unshallow
ADD --keep-git-dir=true https://opendev.org/openstack/heat-tempest-plugin.git#master /src/heat-tempest-plugin
RUN git -C /src/heat-tempest-plugin fetch --unshallow
ADD --keep-git-dir=true https://opendev.org/openstack/keystone-tempest-plugin.git#master /src/keystone-tempest-plugin
RUN git -C /src/keystone-tempest-plugin fetch --unshallow
ADD --keep-git-dir=true https://opendev.org/openstack/neutron-tempest-plugin.git#master /src/neutron-tempest-plugin
RUN git -C /src/neutron-tempest-plugin fetch --unshallow
ADD --keep-git-dir=true https://opendev.org/openstack/octavia-tempest-plugin.git#master /src/octavia-tempest-plugin
RUN git -C /src/octavia-tempest-plugin fetch --unshallow
ADD https://releases.openstack.org/constraints/upper/master /upper-constraints.txt
RUN --mount=type=cache,mode=0755,target=/root/.cache/pip,sharing=private <<EOF bash -xe
pip3 install \
    --constraint /upper-constraints.txt \
        /src/tempest \
        /src/barbican-tempest-plugin \
        /src/cinder-tempest-plugin \
        /src/heat-tempest-plugin \
        /src/keystone-tempest-plugin \
        /src/neutron-tempest-plugin \
        /src/octavia-tempest-plugin
EOF

FROM registry.atmosphere.dev/library/openstack-python-runtime:${RELEASE}
RUN <<EOF bash -xe
apt-get update -qq
apt-get install -qq -y --no-install-recommends \
    iputils-ping openssh-client
apt-get clean
rm -rf /var/lib/apt/lists/*
EOF
COPY --from=octavia-test-server --link /build/test_server.bin /opt/octavia-tempest-plugin/test_server.bin
COPY --from=build --link /var/lib/openstack /var/lib/openstack
