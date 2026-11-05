#
# Copyright (C) 2026 Dan Brown
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""Which dnshelper instance manages a zone (DESIGN 8.3), with the NS8 agent stubbed out."""
import os
import sys
import types
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'imageroot', 'pypkg'))

# nsplatform imports the NS8 agent, which exists only on a node.
_agent = sys.modules.get('agent') or types.ModuleType('agent')
_agent.SD_INFO, _agent.SD_WARNING = '<6>', '<4>'
_agent.tasks = getattr(_agent, 'tasks', None) or types.ModuleType('agent.tasks')
sys.modules.setdefault('agent', _agent)
sys.modules.setdefault('agent.tasks', _agent.tasks)

from pdnsmodule import nsplatform as ns  # noqa: E402


class FakeRedis:
    def __init__(self, module_node):
        self.module_node = module_node

    def hgetall(self, key):
        assert key == 'cluster/module_node'
        return dict(self.module_node)


class Lookup(unittest.TestCase):
    def setUp(self):
        self.rdb = FakeRedis({'dnshelper1': '1', 'dnshelper10': '2', 'dnshelper3': '2', 'powerdns26': '2',
                              'mail1': '1', 'dnshelperx': '1'})
        self.asked = []
        self.answers = {}

        def run(agent_id, action, data, extra=None):
            self.asked.append(agent_id)
            self.assertEqual(action, 'has-zone')
            answer = self.answers.get(agent_id)
            if isinstance(answer, Exception):
                raise answer
            return answer or {'exit_code': 0, 'output': {'managed': False, 'zone': None}}

        _agent.tasks.run = run
        _agent.resolve_agent_id = lambda pattern: 'module/dnshelper1'

    def managed(self, module_id, zone='example.com'):
        self.answers['module/' + module_id] = {'exit_code': 0, 'output': {'managed': True, 'zone': zone}}

    def test_lists_every_instance_in_order(self):
        self.assertEqual(ns.dnshelper_modules(self.rdb), ['dnshelper1', 'dnshelper3', 'dnshelper10'])

    def test_finds_an_instance_that_is_not_the_default(self):
        self.managed('dnshelper3')
        self.assertEqual(ns.zone_manager('example.com', self.rdb), 'dnshelper3')

    def test_not_managed_when_no_instance_manages_it(self):
        self.assertIsNone(ns.zone_manager('example.com', self.rdb))
        self.assertEqual(self.asked, ['module/dnshelper1', 'module/dnshelper3', 'module/dnshelper10'])

    def test_a_failing_instance_does_not_lock_the_zone(self):
        self.answers['module/dnshelper1'] = RuntimeError('no route')
        self.answers['module/dnshelper3'] = {'exit_code': 1, 'output': {}}
        self.assertIsNone(ns.zone_manager('example.com', self.rdb))

    def test_a_parent_zone_answer_does_not_count(self):
        self.managed('dnshelper3', zone='com')
        self.assertIsNone(ns.zone_manager('example.com', self.rdb))

    def test_no_dnshelper(self):
        self.assertIsNone(ns.zone_manager('example.com', FakeRedis({'powerdns26': '2'})))

    def test_default_falls_back_to_the_first_instance(self):
        _agent.resolve_agent_id = lambda pattern: None
        self.assertEqual(ns.dnshelper_module(self.rdb), 'dnshelper1')
        self.assertIsNone(ns.dnshelper_module(FakeRedis({})))


if __name__ == '__main__':
    unittest.main()
