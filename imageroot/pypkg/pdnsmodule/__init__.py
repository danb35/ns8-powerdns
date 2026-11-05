#
# Copyright (C) 2026 Dan Brown
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""Backend library of the powerdns module.

The modules dnsutil, pdnsapi, config, peers and core hold the logic and do not
import the NS8 `agent` package, so tests can run them against a real PowerDNS
without a node. Everything touching the node or Redis is in nsplatform, and the
action entry points are in actions.
"""
